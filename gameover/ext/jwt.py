from flask_jwt_extended import JWTManager

jwt = JWTManager()

def configure(app):
    jwt.init_app(app)
