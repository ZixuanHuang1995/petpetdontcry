from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

def create_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
        
def init_db(app):
    db.init_app(app)