import email
from flask_wtf import FlaskForm
from nbformat import ValidationError
from wtforms import StringField,SubmitField,validators,PasswordField
from wtforms.fields import EmailField
from ..model.model import user
class FormRegister(FlaskForm):
    # 依照model來建立相對的from
    identity = StringField('identity',validators=[
        validators.DataRequired(),
        validators.Length(10,10)
    ])
    email = EmailField('Email',validators=[
        validators.DataRequired(),
        validators.Length(1,50),
        validators.Email()
    ])
    password = PasswordField('password',validators=[
        validators.DataRequired(),
        validators.Length(5,20),
        validators.EqualTo('password2',message='PASSWORD NEED MATCH')
    ])
    # 驗證兩次輸入的密碼是否相同，避免使用者輸入錯誤
    password2 = PasswordField('Confirm PassWord',validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('建立新帳戶')

    # def validate_email(self,field):
    #     if user.query.filter_by(email=field.data).first():
    #         raise ValidationError('Email already register by somebody')
    # def validate_identify(self,field):
    #     if user.query.filter_by(identify=field.data).first():
    #         raise ValidationError('Identify already register by somebody')