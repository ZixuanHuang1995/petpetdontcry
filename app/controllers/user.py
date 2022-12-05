from ..models import user
from ..database import db

def create_user(email,password,identity):
    newuser = user(email=email,password=password,identity=identity)
    db.session.add(newuser)
    db.session.commit()
    return newuser

def get_user_by_name(name):
    return user.query.filter_by(name=name).first()

def get_user(UID):
    return user.query.get(UID)

def get_all_users():
    return user.query.all()

def get_all_users_json():
    users = user.query.all()
    if not users:
        return []
    users = [user.toJSON() for user in users]
    return users

def update_user_name(id, name):
    user = get_user(id)
    if user:
        user.username = name
        db.session.add(user)
        return db.session.commit()
    return None