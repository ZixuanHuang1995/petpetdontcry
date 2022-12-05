from ..database import db
from datetime import datetime

class user(db.Model):
    __tablename__ = 'user'
    UID = db.Column('UID', db.Integer, primary_key = True)
    name = db.Column('name', db.String(20))
    identity = db.Column('identity',db.String(10), nullable=False)
    email = db.Column('email',db.String(50), nullable=False)
    phone = db.Column('phone',db.String(10)) 
    password = db.Column('password',db.String(50), nullable=False)
    def __init__(self,identity,email,password):
        # self.name = name
        self.identity = identity
        self.email = email
        # self.phone = phone
        self.password = password

    def toJSON(self):
        return{
            'id': self.UID,
            'username': self.name
        }

# 查詢表
class information(db.Model):
    __tablename__ = 'information'
    IID = db.Column('IID', db.Integer, primary_key = True)
    name = db.Column('name', db.String(20), nullable=False)
    function = db.Column('function', db.Text)
    type = db.Column('type',db.Integer, nullable=False)
    def __init__(self,name,function,type):
        self.name = name
        self.function = function
        self.type = type
# 刊登資料
class published(db.Model):
    __tablename__ = 'published'
    PublishedID = db.Column('PublishedID', db.Integer, primary_key = True)
    UID = db.Column('UID',db.Integer, nullable=False)
    title = db.Column('title', db.String(20), nullable=False)
    species = db.Column('species', db.String(10), nullable=False)
    fur = db.Column('fur', db.String(10), nullable=False)
    picture = db.Column('picture', db.String(20), nullable=False)
    area = db.Column('area', db.String(10), nullable=False)
    time = db.Column('time', db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now,default=datetime.now)
    depiction = db.Column('depiction', db.Text)
    activate = db.Column('activate', db.Boolean, default=True)
    varitey = db.Column('varitey', db.String(10))
    type = db.Column('type',db.Integer, nullable=False)
    sex = db.Column('sex',db.Integer)
    def __init__(self,UID,title,species,fur,picture,area,depiction,activate,type,varitey,sex):  
        self.UID = UID
        self.title = title
        self.species = species
        self.fur = fur
        self.picture = picture
        self.area = area
        self.depiction = depiction
        self.activate = activate
        self.type = type
        self.varitey = varitey
        self.sex = sex
# 寵物
class pet(db.Model):
    __tablename__ = 'pet'
    PetID = db.Column('PetID', db.Integer, primary_key = True)
    UID = db.Column('UID',db.Integer, nullable=False)
    name = db.Column('name', db.String(20), nullable=False)
    sex = db.Column('sex',db.Integer, nullable=False)
    species = db.Column('species', db.String(10), nullable=False)
    fur = db.Column('fur', db.String(10), nullable=False)
    picture = db.Column('picture', db.String(20), nullable=False)
    variety = db.Column('variety', db.String(10), nullable=False)
    vaccine = db.Column('vaccine',db.Boolean,nullable=False)
    def __init__(self,PetID,UID,name,sex,vaccine,species,fur,picture,variety):
        self.PetID = PetID
        self.UID = UID
        self.name = name
        self.sex = sex
        self.vaccine = vaccine
        self.species = species
        self.fur = fur
        self.picture = picture
        self.variety = variety
# 寵物病歷
class medicalrecords(db.Model):
    __tablename__ = 'medicalrecords'
    MID = db.Column('MID', db.Integer, primary_key = True)
    PetID = db.Column('PetID',db.Integer, nullable=False)
    CID = db.Column('CID',db.Integer, nullable=False)
    disease = db.Column('disease', db.Text)
    doctor = db.Column('doctor', db.String(10), nullable=False)
    medication = db.Column('medication', db.String(30))
    time = db.Column('time', db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
    note = db.Column('note', db.Text)
    type = db.Column('type',db.Integer, nullable=False)
    def __init__(self,PetID,CID,disease,doctor,medication,note,type):  
        self.PetID = PetID
        self.CID = CID
        self.disease = disease
        self.doctor = doctor
        self.medication = medication
        self.note = note
        self.type = type
# 診所醫生資料
class clinic_doctor(db.Model):
    __tablename__ = 'clinic_doctor'
    CID = db.Column('CID', db.Integer, primary_key = True)
    UID = db.Column('UID',db.Integer, primary_key = True)
    def __init__(self,CID,UID):  
        self.CID = CID
        self.UID = UID
        
# 診所
class clinic(db.Model):
    __tablename__ = 'clinic'
    CID = db.Column('CID', db.Integer, primary_key = True)
    name = db.Column('name', db.String(20), nullable=False)
    phone = db.Column('phone', db.String(10), nullable=False)
    address = db.Column('address', db.String(30), nullable=False)
    account = db.Column('account', db.String(30), nullable=False)
    password = db.Column('password', db.String(50), nullable=False)
    emergency = db.Column('emergency', db.Boolean, nullable=False)
    def __init__(self,CID,name,phone,address,account,password,emergency):  
        self.CID = CID
        self.name = name
        self.phone = phone
        self.address = address
        self.account = account
        self.password = password
        self.emergency = emergency
