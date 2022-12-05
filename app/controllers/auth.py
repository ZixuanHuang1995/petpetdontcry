import flask_login
from ..models import user

def authenticate(email,password):
    user = user.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None

def login_user(user, remember):
    return flask_login.login_user(user, remember=remember)


def logout_user():
    flask_login.logout_user()

