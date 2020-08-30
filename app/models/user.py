from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db


class User(db.Model, UserMixin):
    """Basic user model
    """

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def __init__(self, password: str = None, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_password(password)

    def verify_password(self, pw_hash) -> bool:
        return check_password_hash(self.password_hash, pw_hash)

    def set_password(self, pw: str) -> None:
        self.password_hash = generate_password_hash(pw)

    def __repr__(self):
        return "<User %s>" % self.username
