import flask_login
from ..models import user
from flask_login import current_user
from flask import render_template

def authenticate(email,password):
    user = user.query.filter_by(email=email).first()
    if user and user.check_password(password):
        return user
    return None

def login_user(user, remember):
    return flask_login.login_user(user, remember=remember)


def logout_user():
    flask_login.logout_user()

# def clinic_or_user(role):
#     if role != current_user.role:
#         if role == 'clinic':
#             return render_template('home.html')
#         else:
#             return render_template('clinic_home.html')