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
    species = SelectField('寵物類型', validators=[
        validators.DataRequired()
        ], choices=[('dog', '狗'), ('cat', '貓'),('other','其它')]
    )
    fur = StringField('毛色', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    county = SelectField('縣市', choices=[],  validate_choice=False
    )
    district = SelectField('區域',choices=[],  validate_choice=False
    )
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
    photo = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('送出')

class FormeditPublished(FlaskForm):
    type = RadioField('刊登類型', 
    choices=[('1','協尋'),('2','拾獲'),('3','領養')],
    validators=[InputRequired()])
    title = StringField('刊登標題', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    species = SelectField('寵物類型', validators=[
        validators.DataRequired()
        ], choices=[('dog', '狗'), ('cat', '貓'),('other','其它')]
    )
    fur = StringField('毛色', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    county = SelectField('縣市', validate_choice=False, choices=[]
    )
    district = SelectField('區域', validate_choice=False, choices=[]
    )
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

