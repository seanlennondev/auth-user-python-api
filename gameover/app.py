from datetime import timedelta
from flask import Flask

from gameover.ext.database import db, configure as DATABASE
from gameover.ext.migrate import configure as MIGRATE
from gameover.ext.jwt import configure as JWT

def create_app():
    app = Flask(__name__)

    app.config['DEBUG'] = True
    app.config['FLASK_ENV'] = 'Development'
    app.config['FLASK_APP'] = 'app'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///dev.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config['JWT_SECRET_KEY'] = 'SECRET'
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=30)
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=60)

    DATABASE(app)
    MIGRATE(app)
    JWT(app)

    @app.cli.command()
    def init_db():
        db.drop_all()
        db.create_all()

    from gameover.controllers.user import bp as bp_user

    app.register_blueprint(bp_user)

    if __name__ == '__main__':
        app.run(debug=True)

    return app
