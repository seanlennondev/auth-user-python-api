from datetime import datetime

from gameover.ext.database import db

class PrimaryKeyMixin(object):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

class DateTimeMixin(object):
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = db.Column(
        db.DateTime,
        onupdate=datetime.utcnow
    )
