from flask_login import current_user
from wtforms import Form, validators, PasswordField
from wtforms import StringField

from app.extensions import db
from app.models.user import User


class LoginForm(Form):
    username = StringField(
        validators=[
            validators.required()
        ]
    )
    password = PasswordField(validators=[validators.required()])

    def validate_username(self, field):
        user = self.get_user()
        if user is None or not user.verify_password(self.password.data):
            raise validators.ValidationError('Invalid credentials')

    def get_user(self) -> User:
        return db.session.query(User).filter_by(username=self.username.data).first()


class ChangePasswordForm(Form):
    old_password = PasswordField(
        validators=[
            validators.required()
        ]
    )
    new_password = PasswordField(
        "New Password",
        validators=[
            validators.required(),
            validators.Length(min=8, message="You need at least 8 characters"),
            validators.EqualTo('new_password_confirmation', message='Passwords must match')
        ]
    )
    new_password_confirmation = PasswordField("Confirm Password")

    def validate_old_password(self, field):
        if not current_user.verify_password(field.data):
            raise validators.ValidationError('Password is wrong')
