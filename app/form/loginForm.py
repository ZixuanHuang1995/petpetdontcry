from flask_wtf import FlaskForm
from wtforms import SubmitField,validators,PasswordField,BooleanField,RadioField
from wtforms.validators import InputRequired
from wtforms.fields import EmailField
class FormLogin(FlaskForm):
    """
    使用者登入使用
    以email為主要登入帳號，密碼需做解碼驗證
    記住我的部份透過flask-login來實現
    """
    # type = RadioField('登入類別', 
    #     choices=[
    #         ('clinic','診所'),
    #         ('user','會員')
    #     ],
    #     validators=[
    #         InputRequired()
    #     ]
    # )

    account = EmailField('帳號', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])

    password = PasswordField('密碼', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('記住我')

    submit = SubmitField('登入')