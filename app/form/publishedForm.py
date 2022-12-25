from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,validators,FileField,SelectField,TextAreaField,RadioField
from wtforms.validators import InputRequired
from ..models import user
from ..config_other import photos
from flask_wtf.file import FileAllowed, FileRequired
class FormPublished(FlaskForm):
    type = RadioField('刊登類型', 
    choices=[('1','協尋'),('2','拾獲'),('3','領養')],
    validators=[InputRequired()])
    title = StringField('刊登標題', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    species = StringField('寵物類型', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    fur = StringField('毛色', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    area = StringField('發現地區', validators=[
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
    
    depiction = TextAreaField('敘述', validators=[
        validators.Length(0, 300)
    ])
    picture = FileField('上傳照片', validators=[
        FileAllowed(photos, 'IMAGE ONLY'),
        FileRequired('IMAGE REQUIRED PLEASE')
    ])
    # picture = TextAreaField('上傳照片', validators=[
    #     validators.Length(0, 300)
    # ])
    submit = SubmitField('送出')

class FormeditPublished(FlaskForm):
    type = RadioField('刊登類型', 
    choices=[('1','協尋'),('2','拾獲'),('3','領養')],
    validators=[InputRequired()])
    title = StringField('刊登標題', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    species = StringField('寵物類型', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    fur = StringField('毛色', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    area = StringField('發現地區', validators=[
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
    
    depiction = TextAreaField('敘述', validators=[
        validators.Length(0, 300)
    ])

    submit = SubmitField('送出')

