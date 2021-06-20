from gameover.ext.database import db
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from flask_jwt_extended import create_access_token

from .mixins import PrimaryKeyMixin, DateTimeMixin

class User(PrimaryKeyMixin, DateTimeMixin, db.Model):
    __tablename__ = 'users'

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
        index=True
    )

    password_hash = db.Column(
        db.String,
        nullable=False
    )

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = password

    def __repr__(self):
        return '<User(username={username}, email={email})>'.format(
            username=self.username,
            email=self.email
        )

    def encrypt_password(self):
        self.password_hash = generate_password_hash(self.password_hash)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_access_token(self):
        return create_access_token(self.email)

    def change_password(self, new_password):
        self.password_hash = new_password

    def create(self):
        db.session.add(self)

    def update(self, username):
        self.username = username

    def delete(self):
        db.session.delete(self)

    def commit(self):
        db.session.commit()
