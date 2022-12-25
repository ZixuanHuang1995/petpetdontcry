from distutils import core
from distutils.text_file import TextFile
from flask_wtf import FlaskForm
from nbformat import ValidationError
from wtforms import StringField,SubmitField,validators,PasswordField,IntegerField,BooleanField,TextAreaField,SelectField,FileField
from wtforms.fields import EmailField
from ..models import clinic
from flask_wtf.file import FileAllowed, FileRequired
from ..models import pet,user
from ..controllers import (
    get_clinic_data
)
# from wtforms.widgets.core.
# from wtforms.ext.sqlalchemy.fields import QuerySelectField

class FormPet(FlaskForm):
    """
    新增寵物
    """
    PetID = StringField('寵物晶片號碼', validators=[
        validators.DataRequired(),
        validators.Length(6, 10)
    ])
    UID = StringField('飼主編號', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    name = StringField('寵物名稱', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    species = SelectField('寵物類型', validators=[
        validators.DataRequired()
        ], choices=[('dog', '狗'), ('cat', '貓'),('other','其它')]
    )
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
     ], choices=[('1', '母'), ('0', '公'),('2','未知')])
    vaccine = SelectField('是否打疫苗', validators=[
        validators.DataRequired()
    ], choices=[('1', '是'), ('0', '否')])
    submit = SubmitField('送出')
    
    # def validate_PetID(self,field):
    #     if pet.query.filter_by(PetID=field.data).first():
    #         raise ValidationError('寵物晶片已登入過')
    # def validate_UID(self,field):
    #     if user.query.filter_by(UID=field.data).first() is None:
    #         raise ValidationError('請填寫正確的使用者編號')

class FormPetEdit(FlaskForm):
    """
    更新寵物
    """
    PetID = StringField('寵物晶片號碼', render_kw={'readonly': True})
    UID = StringField('飼主編號', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    name = StringField('寵物名稱', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    species = SelectField('寵物類型', validators=[
        validators.DataRequired()
        ], choices=[('dog', '狗'), ('cat', '貓'),('other','其它')]
    )
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
     ], choices=[('1', '母'), ('0', '公'),('2','未知')])
    vaccine = SelectField('是否打疫苗', validators=[
        validators.DataRequired()
    ], choices=[('1', '是'), ('0', '否')])
    submit = SubmitField('送出')

    def validate_UID(self,field):
        if user.query.filter_by(UID=field.data).first() is None:
            raise ValidationError('請填寫正確的使用者編號')
class FormDoctor(FlaskForm):
    UID = StringField('醫師編號', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    submit = SubmitField('新增')

class FormMedicalRecords(FlaskForm):
#     MID = StringField('病歷號碼', render_kw={'readonly': True})
    PetID = StringField('寵物晶片號碼', render_kw={'readonly': True})
    CID = StringField('診所名稱', render_kw={'readonly': True})
    type = SelectField('就醫類型', validators=[
        validators.DataRequired()
    ], choices=[('2', '看診'), ('3', '檢查'), ('1', '疫苗')]
    )

    doctor = SelectField('醫師姓名', validators=[
        validators.DataRequired()
    ], choices=[])
    
    disease = TextAreaField('病症', validators=[
        validators.Length(0, 100)
    ])
    medication = StringField('用藥')

    note = TextAreaField('備註', validators=[
        validators.Length(0, 100)
    ])
    submit = SubmitField('新增')

class FormFindPet(FlaskForm):
    PetID = StringField('寵物晶片編號', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    submit = SubmitField('查詢')