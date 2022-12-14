from cmath import phase
import email
from flask_wtf import FlaskForm
from nbformat import ValidationError
from wtforms import StringField,SubmitField,validators,PasswordField,BooleanField
from wtforms.fields import EmailField
from ..models import user
class FormRegister(FlaskForm):
    # 依照model來建立相對的from
    identity = StringField('身分證字號',validators=[
        validators.DataRequired(),
        validators.Length(10,10)
    ])
    email = EmailField('Email',validators=[
        validators.DataRequired(),
        validators.Length(1,50),
        validators.Email()
    ])
    password = PasswordField('密碼',validators=[
        validators.DataRequired(),
        validators.Length(5,20),
        validators.EqualTo('password2',message='PASSWORD NEED MATCH')
    ])
    # 驗證兩次輸入的密碼是否相同，避免使用者輸入錯誤
    password2 = PasswordField('確認密碼',validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('註冊')

    def validate_email(self,field):
        if user.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register by somebody')
    def validate_identify(self,field):
        if user.query.filter_by(identify=field.data).first():
            raise ValidationError('Identify already register by somebody')

class FormLogin(FlaskForm):
    """
    使用者登入使用
    以email為主要登入帳號，密碼需做解碼驗證
    記住我的部份透過flask-login來實現
    """

    email = EmailField('Email', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])

    password = PasswordField('密碼', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('記住我')

    submit = SubmitField('登入')

class FormUserInfo(FlaskForm):
    UID = StringField('會員編號', render_kw={'readonly': True})
    email = StringField('Email', render_kw={'readonly': True})
    identity = StringField('身分證字號', render_kw={'readonly': True})
    name = StringField('姓名',validators=[
        validators.DataRequired()
    ])
    phone = StringField('電話',validators=[
        validators.Length(8, 10),
    ])
    submit = SubmitField('送出')