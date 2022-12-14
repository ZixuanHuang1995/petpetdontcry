from distutils.text_file import TextFile
from flask_wtf import FlaskForm
from nbformat import ValidationError
from wtforms import StringField,SubmitField,validators,PasswordField,IntegerField,BooleanField,TextAreaField,SelectField,FileField
from wtforms.fields import EmailField
from ..models import clinic
from ..config_other import photos
from flask_wtf.file import FileAllowed, FileRequired
# from wtforms.widgets.core.
# from wtforms.ext.sqlalchemy.fields import QuerySelectField

class FormLogin(FlaskForm):
    """
    使用者登入使用
    以email為主要登入帳號，密碼需做解碼驗證
    記住我的部份透過flask-login來實現
    """

    account = EmailField('帳號', validators=[
        validators.DataRequired(),
        validators.Length(5, 30),
        validators.Email()
    ])

    password = PasswordField('密碼', validators=[
        validators.DataRequired()
    ])

    remember_me = BooleanField('記住我')

    submit = SubmitField('Login')

class FormPet(FlaskForm):
    """
    新增寵物
    """
    PetID = StringField('寵物晶片號碼', validators=[
        validators.DataRequired(),
        validators.Length(0, 15)
    ])
    UID = StringField('飼主編號', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    name = StringField('寵物名稱', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    species = StringField('寵物類型', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    fur = StringField('寵物毛色', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    variety = StringField('寵物品種', validators=[
        validators.Length(0, 10)
    ])
    #  使用下拉選單來選擇性別
    sex = SelectField('寵物性別', validators=[
        validators.DataRequired()
     ], choices=[('1', '女'), ('0', '男')])
    picture = FileField('上傳照片', validators=[
        FileAllowed(photos, 'IMAGE ONLY'),
        FileRequired('IMAGE REQUIRED PLEASE')
    ])
    vaccine = SelectField('是否打疫苗', validators=[
        validators.DataRequired()
    ], choices=[('True', '是'), ('False', '否')])
    submit = SubmitField('送出')

class FormDoctor(FlaskForm):
    UID = StringField('醫師編號', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    submit = SubmitField('新增')