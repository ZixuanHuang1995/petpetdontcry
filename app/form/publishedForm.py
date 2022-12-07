from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,validators,FileField,SelectField,TextAreaField,RadioField
from wtforms.validators import InputRequired
from ..models import user
from ..config_other import photos
from flask_wtf.file import FileAllowed, FileRequired
class FormPublished(FlaskForm):
    type = RadioField('type', 
    choices=[('1','協尋'),('2','拾獲'),('3','領養')],
    validators=[InputRequired()])
    title = StringField('title', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    species = StringField('species', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    fur = StringField('fur', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    area = StringField('area', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    variety = StringField('variety', validators=[
        validators.Length(0, 10)
    ])
    #  使用下拉選單來選擇性別
    sex = SelectField('sex', validators=[
        validators.DataRequired()
     ], choices=[('1', '女'), ('0', '男')])
    
    depiction = TextAreaField('depiction', validators=[
        validators.Length(0, 300)
    ])
    picture = FileField('picture', validators=[
        FileAllowed(photos, 'IMAGE ONLY'),
        FileRequired('IMAGE REQUIRED PLEASE')
    ])
    submit = SubmitField('Create Blog')
