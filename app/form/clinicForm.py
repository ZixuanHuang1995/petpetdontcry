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

class FormMedicalRecords(FlaskForm):
    MID = StringField('病歷號碼', validators=[
    validators.DataRequired(),
    validators.Length(0, 15)
    ])
    PetID = StringField('寵物晶片號碼', validators=[
        validators.DataRequired(),
        validators.Length(0, 15)
    ])
    CID = StringField('診所名稱', validators=[
        validators.DataRequired(),
        validators.Length(0, 10)
    ])
    type = SelectField('就醫類型', validators=[
        validators.DataRequired()
    ], choices=[('0', '看診'), ('1', '檢查'), ('2', '疫苗施打')]
    )
    doctorList = ''
    doctor = SelectField('醫師姓名', validators=[
        validators.DataRequired()
    ], choices= ['doctor A', 'doctor B', 'doctor C'])
    disease = TextAreaField('病症', validators=[
        validators.Length(0, 100)
    ])
    medicationList = ''
    medication = SelectField('用藥', validators=[
        validators.DataRequired()
    ], choices= ['TULASIN INJ.', 'COZYFLOW', "FULICO ORAL SOL'N 20%", 'KANA-PS INJECTION', 'LEFUDUO 20', 'WATER FOR INJECTION "TAI YU"', 'TYLOSIN PHOSPHATE', 'TYLOSIN', 'TYLOSIN TARTRATE', 'BIORAL H120', 'REVOLUTION PLUS 1.0 ML', 'REVOLUTION PLUS 0.5 ML', 'REVOLUTION PLUS 0.25 ML', 'SERA POND OMNISAN F', 'SERA POND OMNIPUR', 'DOXICOR', 'SAMU TYLOSIN INJECTION', 'CERENIA', 'DERFUCOL-10 SOLUTION', 'OXY-22% POWDER', 'FEIYICHING', 'CEFA-SAFE', 'TIPAFAR', 'ENRODING', 'DOXYLIN-20-F', 'AMPROL 25％', 'SUCOGIN 8%', 'WORMCIDE S', 'ALFAXAN MULTIDOSE ANAESTHETIC INJECTION', 'TIACOLIN-100 INJECTION', 'GLEPTOFERRON LABIANA 200MG/ML', 'AVISAN MULTI', 'ANGESOL 50%', 'METABOL INJ.', 'SERA COSTAPUR F', 'SERA MYCOPUR', 'SERA POND CYPRINOPUR', 'SERA BAKTOPUR', 'CEPHASINE-150F', 'DPP INJECTION', 'DIAMICIN-20', 'THIAMPHENICOL-10-F', 'H.K.P. TIAMULIN 200 POWDER-FA', 'AMVET', 'OTOMAX', 'AMOXAL 150MG/ML INJECTABLE SUSPENSION', 'RABISIN', 'NASHER DOX 500', 'OTCAS', 'AMO-50-F', 'ONSIOR TABLETS FOR DOGS', 'RONAXAN 20％', 'TILMICOX SOLUCION', 'FLUMINE (ORAL SOLUTION)', 'TYLORATE SOL 20%', 'COLISOL (ORAL SOLUTION)', 'POLY AD', 'VITACEN AD3E', 'AMPHENOR', 'VIDALTA 15MG RETARDTABLETTEN FUR KATZEN', 'VIDALTA 10MG RETARDTABLETTEN FUR KATZEN', 'MOMETAMAX', 'FLORFENICOL', 'ANTIROBE AQUADROPS', 'KEFLEX-15-F', 'PYRIMETHAMINE-100', 'DOXYTON 7.5% POWDER', 'VENTO-DX', 'IVERMECTIN 0.6% POWDER', 'H.K.P. RELAXYZINE', 'SAMU AMOXY-50 POWDER', 'SAMU AMOXY-20 POWDER', 'PROTECTIER OTIC DROPS', 'LINCOMYCIN400 POWDER', 'PUREVAX RCPCH FELV', 'FORMOSA DOXYCYCLINE 50% WSP', 'OXYTETRACYCLINE500', '', 'COLISTIN ”AVICO”', 'IVM-6', 'TIAMULIN FUMARATE'])
    time = StringField('新增時間', validators=[
        validators.DataRequired(),
        validators.Length(0, 30)
    ])
    supdate_time = StringField('更新時間', validators=[
        validators.DataRequired(),
        validators.Length(0, 30)
    ])
    note = StringField('筆記', validators=[
        validators.Length(0, 100)
    ])
    submit = SubmitField('新增')

    """
    def __init__(self, doctorList, medicationList):
        self.doctorList = doctorList
        self.medicationList = medicationList
    """

class FormFindPet(FlaskForm):
    PetID = StringField('寵物晶片編號', validators=[
        validators.DataRequired(),
        validators.Length(0, 20)
    ])
    submit = SubmitField('查詢')