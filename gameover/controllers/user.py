from flask import Blueprint, request
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity
)
from gameover.schemas.user import (
    user_schema,
    users_schema
)

from gameover.models.user import User
from faker import Faker

fake = Faker('pt-br')

bp = Blueprint('User', __name__, url_prefix='/api')

@bp.route('/users')
def get_user():
    user = User.query.all()
    print([(fake.user_name(), fake.password()) for _ in range(1)])
    return users_schema.jsonify(user)

@bp.route('/users/auth', methods=['POST'])
def authenticate():
    try:
        (email, password) = (
            request.json.get('email', None),
            request.json.get('password', None)
        )
        if not email and password:
            return {
                'message': 'O e-mail é obrigatório'
            }, 422
        elif not password and email:
            return {
                'message': 'A senha é obrigatória'
            }, 422
        elif not email and not password:
            return {
                'message': 'Os campos são obrigatórios'
            }, 422

        user = User.query.filter_by(email=email).one_or_none()
        if not user or not user.check_password(password):
            return 'E-mail ou senha inválidos', 404
        token = user.generate_access_token()
        return {
            'success': True,
            'message': 'Usuário autenticado com sucesso',
            'data': token
        }, 200
    except Exception as e:
        raise e

@bp.route('/users', methods=['POST'])
def create_user():
    try:
        body = request.get_json()
        if not body:
            return 'Os campos são obrigatórios', 422

        user = User(**body)
        user.encrypt_password()
        user.create()
        user.commit()
        return {
            'success': True,
            'message': 'Usuário criado com sucesso',
            'data': user_schema.jsonify(user).json
        }, 200
    except Exception as e:
        raise e

@bp.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
@jwt_required()
def get_put_delete(user_id):
    try:
        identity = get_jwt_identity()
        user = User.query.filter_by(id=user_id, email=identity).one_or_none()
        if not user:
            return 'Usuário não encontrado', 404

        if request.method == 'GET':
            return user_schema.jsonify(user)
        if request.method == 'PUT':
            username = request.json.get('username')
            user.update(username)
            user.commit()
            return user_schema.jsonify(user)
        if request.method == 'DELETE':
            user.delete()
            user.commit()
            return {
                'success': True,
                'message': 'Usuário deletado com sucesso',
                'data': None
            }, 200
    except Exception as e:
        raise e

@bp.route('/users/<int:id>/change-password', methods=['PATCH'])
@jwt_required()
def patch(id):
    try:
        identity = get_jwt_identity()
        user = User.query.filter_by(id=id, email=identity).one_or_none()
        if not user:
            return 'Usuário não cadrastado', 404

        (current_password, new_password) = (
            request.json.get('current_password', None),
            request.json.get('new_password', None)
        )
        if not user.check_password(current_password):
            return 'Senha atual inválida', 404

        user.change_password(new_password)
        user.encrypt_password()
        user.commit()
        return {
            'success': True,
            'message': 'Senha alterada com sucesso',
            'data': None
        }, 200
    except Exception as e:
        raise e

@bp.route('/users/forget-password', methods=['POST'])
def forget_password():
    try:
        email = request.json.get('email', None)
        user = User.query.filter_by(email=email).one_or_none()
        if not user:
            return 'E-mail não cadastrado'

        # Enviar e-mail de recuperação e senha
        return '', 200
    except Exception as e:
        raise e
