from gameover.ext.database import db

from flask_migrate import Migrate

mg = Migrate()

def configure(app):
    mg.init_app(app, db)
    # Migrate(app, db)
