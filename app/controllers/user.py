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

def get_user_data(ID):
    return user.query.filter_by(ID=ID).first()

def get_pet_all_medicalrecords(PetID):
    from ..models.user import medicalrecords
    pets_medicalrecords = medicalrecords.query.filter_by(PetID=PetID).all()
    if not pets_medicalrecords:
        return []
    pets_medicalrecords = [medicalrecords.toJSON() for  medicalrecords in pets_medicalrecords]
    print(pets_medicalrecords)
    return pets_medicalrecords
    
def get_pet_all_vaccinerecords(PetID):
    from ..models.user import medicalrecords
    pets_vaccinerecords = medicalrecords.query.filter_by(PetID=PetID, type=1).all()
    if not pets_vaccinerecords:
        return []
    pets_vaccinerecords = [medicalrecords.toJSON1() for  medicalrecords in pets_vaccinerecords]
    print(pets_vaccinerecords)
    return pets_vaccinerecords