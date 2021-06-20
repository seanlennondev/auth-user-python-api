import pytest
# from faker import Faker
from httpx import post, delete, put, get, patch

@pytest.mark.parametrize(('username', 'email' ,'password', 'message', 'status_code'), (
    # (None, None, None, 'Usuário criado com sucesso', 200),
    # ('sean_ono', None, 'Usuário criado com sucesso', None, 200),
    # (None, 'sean@gmail.com', 'Usuário criado com sucesso', None, 200),
    # (None, None, '12345', 'Usuário criado com sucesso', 200),
    ('sean_ono', 'sean@gmail.com', '12345', 'Usuário criado com sucesso', 200),
))
def test_deve_criar_o_usuario(username, email, password, message, status_code):
    res = post('http://localhost:5000/api/users', json={
        'username': username,
        'email': email,
        'password': password
    })
    assert status_code == res.status_code and message in res.json()['message']

@pytest.mark.parametrize(('email', 'password', 'message', 'status_code'), (
    # (None, '12345', 'Usuário autenticado com sucesso', 200),
    # ('sean@gmail.com', None, 'Usuário autenticado com sucesso', 200),
    # (None, None, 'Usuário autenticado com sucesso', 200),
    ('sean@gmail.com', '12345', 'Usuário autenticado com sucesso', 200),
))
def test_deve_autenticar_o_usuario(email, password, message, status_code):
    res = post('http://localhost:5000/api/users/auth', json={
        'email': email,
        'password': password
    }, headers={
        'Content-Type': 'application/json'
    })
    assert res.status_code == status_code and message in res.json()['message']

@pytest.mark.parametrize(('user_id', 'status_code'), (
    # (0, 200),
    # (2, 200),
    (1, 200),
))
def test_deve_obter_o_usuario_de_id_1(get_token, user_id, status_code):
    res = get(f'http://localhost:5000/api/users/{user_id}', headers={
        'Authorization': f'Bearer {get_token}'
    })
    assert status_code == res.status_code and user_id == res.json()['id']

@pytest.mark.parametrize(('username', 'status_code'), (
    ('lennon_ono', 200),
))
def test_update(get_token, username, status_code):
    res = put('http://localhost:5000/api/users/1', json={
        'username': username
    }, headers={
        'Authorization': f'Bearer {get_token}'
    })
    assert status_code == res.status_code and username in res.json()['username']

@pytest.mark.parametrize(('current_password', 'new_password', 'message', 'status_code'), (
    # ('', None, 'Senha alterada com sucesso', 200),
    # ('123', None, 'Senha alterada com sucesso', 200),
    # (None, '123', 'Senha alterada com sucesso', 200),
    # ('123', '123', 'Senha alterada com sucesso', 200),
    ('12345', '123', 'Senha alterada com sucesso', 200),
))
def test_deve_alterar_a_senha_do_usuario(get_token, current_password, new_password, message, status_code):
    res = patch('http://localhost:5000/api/users/1/change-password', json={
        'current_password': current_password,
        'new_password': new_password
    }, headers={
        'Authorization': f'Bearer {get_token}'
    })
    assert status_code == res.status_code and message in res.json()['message']

@pytest.mark.parametrize(('user_id', 'message', 'status_code'), (
    # (0, 'Usuário deletado com sucesso', 200),
    # (2, 'Usuário deletado com sucesso', 200),
    (1, 'Usuário deletado com sucesso', 200),
))
def test_delete(get_token, user_id, message, status_code):
    res = delete(f'http://localhost:5000/api/users/{user_id}', headers={
       'Authorization': f'Bearer {get_token}'
    })
    assert status_code == res.status_code and message in res.json()['message']
