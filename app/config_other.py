from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_uploads import IMAGES, UploadSet, configure_uploads
login_manager = LoginManager()
bcrypt = Bcrypt()
photos = UploadSet("photos", IMAGES)
def init(app):
    login_manager.init_app(app)
    login_manager.login_view = 'index_views.login'
    bcrypt.init_app(app)
    configure_uploads(app, photos)