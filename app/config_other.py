from flask_login import LoginManager
from flask_bcrypt import Bcrypt
login_manager = LoginManager()
bcrypt = Bcrypt()
def init(app):
    login_manager.init_app(app)
    login_manager.login_view = 'user_views.login'
    bcrypt.init_app(app)

