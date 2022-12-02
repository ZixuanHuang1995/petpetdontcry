# 引用 Flask 套件
from flask import Flask, abort, render_template, request, jsonify, session, Blueprint
# 引用 SQL 相關模組
from flask_sqlalchemy import SQLAlchemy
# 引用其他相關模組
from .config.config import config 
from .view.signupForm import FormRegister
from flask_bootstrap import Bootstrap

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    # 設定config
    app.config.from_object(config['default'])
    
    bootstrap = Bootstrap(app)
    register_extensions(app)
    # register_blueprints(app)
    @app.route('/')
    def index():
        return 'success'
    @app.route('/register',methods=['GET','POST'])
    def register():
        print(db)
        from .model.model import user
        form = FormRegister()
        if form.validate_on_submit():
            user = user(
                identity = form.identity.data,
                email = form.email.data,
                password = form.password.data
            )
            db.session.add(user)
            db.session.commit()
            return 'Success!'
        return render_template('test.html',form = form)
    @app.route('/create_all')
    def create_db():
        db.create_all()
        return 'success'
        
    return app
def register_extensions(app):
    """Register extensions with the Flask application."""
    db.init_app(app)


# def register_blueprints(app):
#     """Register blueprints with the Flask application."""
#     from .view.auth import auth
#     app.register_blueprint(auth, url_prefix='/auth')