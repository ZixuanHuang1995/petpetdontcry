import imp
import bcrypt
from ..database import db
from datetime import datetime
from flask_login import UserMixin
from ..config_other import login_manager
from werkzeug.security import generate_password_hash, check_password_hash
class user(db.Model):
    __tablename__ = 'user'
    UID = db.Column('UID', db.Integer, primary_key = True)
    name = db.Column('name', db.String(20))
    identity = db.Column('identity',db.String(10), nullable=False)
    # email = db.Column('email',db.String(50), nullable=False)
    phone = db.Column('phone',db.String(10)) 
    ID = db.Column('ID',db.Integer,db.ForeignKey('account.ID'),nullable=False)
    # password_hash = db.Column('password',db.String(128), nullable=False)
    # role = db.Column('role', db.String(10), nullable=False)
    published = db.relationship('published', backref='user', lazy='dynamic')
    pet = db.relationship('pet', backref='user', lazy='dynamic')
    clinic_doctor = db.relationship('clinic_doctor', backref='user', lazy='dynamic')
    def __init__(self,identity,ID,name,phone):
        self.name = name
        self.identity = identity
        self.ID = ID
        self.phone = phone
        # self.password = password

    def toJSON(self):
        return{
            'id': self.UID,
            'username': self.name
        }

# 帳號密碼
class account(UserMixin,db.Model):
    __tablename__ = 'account'
    ID = db.Column('ID', db.Integer, primary_key = True)
    email = db.Column('email',db.String(50), nullable=False)
    password_hash = db.Column('password',db.String(128), nullable=False)
    role = db.Column('role', db.String(10), nullable=False)
    first = db.Column('first', db.Boolean, default=False)
    user = db.relationship('user', backref='user', lazy='dynamic')
    clinic = db.relationship('clinic', backref='clinic', lazy='dynamic')
    def __init__(self,email,password,role):
        self.email = email
        self.password = password
        self.role=role
    
    def get_id(self):
        return (self.ID)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self,password):
        return check_password_hash(self.password_hash, password)    
        
    @login_manager.user_loader
    def load_user(ID):
        # 回傳的就是使用者資訊
        try:
            return account.query.get(ID)
        except:
            return None

# 刊登資料
class published(db.Model):
    __tablename__ = 'published'
    PublishedID = db.Column('PublishedID', db.Integer, primary_key = True)
    UID = db.Column('UID',db.Integer,db.ForeignKey('user.UID'),nullable=False)
    title = db.Column('title', db.String(20), nullable=False)
    species = db.Column('species', db.String(10), nullable=False)
    fur = db.Column('fur', db.String(10), nullable=False)
    picture = db.Column('picture', db.String(20), nullable=False)
    area = db.Column('area', db.String(10), nullable=False)
    time = db.Column('time', db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now,default=datetime.now)
    depiction = db.Column('depiction', db.Text)
    activate = db.Column('activate', db.Boolean, default=True)
    variety = db.Column('variety', db.String(10))
    type = db.Column('type',db.Integer, nullable=False)
    sex = db.Column('sex',db.Integer)
    county = db.Column('county', db.String(10), nullable=False)
    district = db.Column('district', db.String(10), nullable=False)
    def __init__(self,UID,title,species,fur,picture,area,depiction,activate,type,variety,sex):  
        self.UID = UID
        self.title = title
        self.species = species
        self.fur = fur
        self.picture = picture
        self.area = area
        self.depiction = depiction
        self.activate = activate
        self.type = type
        self.variety = variety
        self.sex = sex
# 寵物
class pet(db.Model):
    __tablename__ = 'pet'
    PetID = db.Column('PetID', db.Integer, primary_key = True)
    UID = db.Column('UID',db.Integer,db.ForeignKey('user.UID'), nullable=False)
    name = db.Column('name', db.String(20), nullable=False)
    sex = db.Column('sex',db.Integer, nullable=False)
    species = db.Column('species', db.String(10), nullable=False)
    fur = db.Column('fur', db.String(10), nullable=False)
    variety = db.Column('variety', db.String(10), nullable=False)
    vaccine = db.Column('vaccine',db.Boolean,nullable=False)
    medicalrecords = db.relationship('medicalrecords', backref='pet', lazy='dynamic')
    def __init__(self,PetID,UID,name,sex,vaccine,species,fur,variety):
        self.PetID = PetID
        self.UID = UID
        self.name = name
        self.sex = sex
        self.vaccine = vaccine
        self.species = species
        self.fur = fur
        self.variety = variety

# 寵物病歷
class medicalrecords(db.Model):
    __tablename__ = 'medicalrecords'
    MID = db.Column('MID', db.Integer, primary_key = True)
    PetID = db.Column('PetID',db.Integer,db.ForeignKey('pet.PetID'), nullable=False)
    CID = db.Column('CID',db.Integer,db.ForeignKey('clinic.CID'), nullable=False)
    disease = db.Column('disease', db.Text)
    doctor = db.Column('doctor', db.String(10), nullable=False)
    medication = db.Column('medication', db.String(30))
    time = db.Column('time', db.DateTime, default=datetime.now)
    update_time = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now)
    note = db.Column('note', db.Text)
    type = db.Column('type',db.Integer, nullable=False)
    def __init__(self,PetID,CID,disease,doctor,note,type):  
        self.PetID = PetID
        self.CID = CID
        self.disease = disease
        self.doctor = doctor
        # self.medication = medication
        self.note = note
        self.type = type
    def toJSON(self):
        return{
            'clinic': self.CID, # 診所名稱
            'time': self.time, # 就醫日期
            'type': self.type,
            'doctor': self.doctor
        }
    def toJSON1(self):
        return {
            'time':self.time,
            'vaccine':self.disease
        }

# 診所醫生資料
class clinic_doctor(db.Model):
    __tablename__ = 'clinic_doctor'
    CID = db.Column('CID', db.Integer,db.ForeignKey('clinic.CID'),primary_key = True)
    UID = db.Column('UID',db.Integer,db.ForeignKey('user.UID'), primary_key = True)
    # clinic = db.relationship('clinic', backref='clinic_doctor', lazy='dynamic')
    # user = db.relationship('user', backref='clinic_doctor', lazy='dynamic')
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
    emergency = db.Column('emergency', db.Boolean, nullable=False)
    ID = db.Column('ID',db.Integer,db.ForeignKey('account.ID'),nullable=False)
    medicalrecords = db.relationship('medicalrecords', backref='clinic', lazy='dynamic')
    clinic_doctor = db.relationship('clinic_doctor', backref='clinic', lazy='dynamic')
    def __init__(self,CID,name,phone,address,ID,emergency):  
        self.CID = CID
        self.name = name
        self.phone = phone
        self.address = address
        self.ID = ID
        self.emergency = emergency