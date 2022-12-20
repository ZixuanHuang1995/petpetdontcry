from cmath import phase
import email
from flask_wtf import FlaskForm
from nbformat import ValidationError
from wtforms import StringField,SubmitField,validators,PasswordField,BooleanField
from wtforms.fields import EmailField
from ..models import user,account
class FormRegister(FlaskForm):
    # 依照model來建立相對的from
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
        if account.query.filter_by(email=field.data).first():
            raise ValidationError('Email already register by somebody')
    def validate_identify(self,field):
        if user.query.filter_by(identify=field.data).first():
            raise ValidationError('Identify already register by somebody')

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

class FormAddUserInfo(FlaskForm):
    # email = StringField('Email', render_kw={'readonly': True})
    identity = StringField('身分證字號',validators=[
        validators.DataRequired(),
        validators.Length(10,10),
    ])
    name = StringField('姓名',validators=[
        validators.DataRequired()
    ])
    phone = StringField('電話',validators=[
        validators.Length(8, 10),
    ])
    submit = SubmitField('送出')

class FormChangePWD(FlaskForm):
    """
    使用者變更密碼
    舊密碼、新密碼與新密碼確認
    """
    #  舊密碼
    password_old = PasswordField('舊密碼', validators=[
        validators.DataRequired()
    ])
    #  新密碼
    password_new = PasswordField('新密碼', validators=[
        validators.DataRequired(),
        validators.Length(5, 10),
        validators.EqualTo('password_new_confirm', message='PASSWORD NEED MATCH')
    ])
    #  新密碼確認
    password_new_confirm = PasswordField('確認新密碼', validators=[
        validators.DataRequired()
    ])
    submit = SubmitField('更新密碼')
