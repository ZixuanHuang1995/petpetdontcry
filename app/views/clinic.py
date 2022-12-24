from flask import Blueprint, render_template,abort, jsonify, request, send_from_directory, flash, redirect, url_for
import flask,os
from flask_login import login_user,current_user,login_required,logout_user
from ..form.clinicForm import FormPet,FormDoctor, FormMedicalRecords,FormFindPet,FormPetEdit
from ..database import db
from werkzeug.utils import secure_filename
# from werkzeug import secure_filename, FileStorage
from werkzeug.datastructures import FileStorage
from ..controllers import (
    get_clinic_data
)
# from flask import Flask
# app = Flask(__name__,static_url_path='/static')
clinic_views = Blueprint('clinic_views', __name__, template_folder='../templates')

@clinic_views.route('/clinic/home')
def home():
    clinic = get_clinic_data(current_user.ID)
    return render_template('clinic_home.html',name=clinic.name)

@clinic_views.route('/test_clinic')
@login_required
def test_index():
    flash('flash-1')  
    # flash('flash-2')  
    # flash('flash-3')  
    return render_template('base.html')  

@clinic_views.route('/clinic/add_pet', methods=['GET', 'POST'])
@login_required
def add_pet():
    """
    說明：新增寵物晶片
    :return:
    """
    from ..models import pet
    form = FormPet()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        Pets = pet(
            PetID=int(form.PetID.data),
            UID=int(form.UID.data),
            name=form.name.data,
            fur=form.fur.data,
            species=form.species.data,
            sex=int(form.sex.data),
            variety=form.variety.data,
            vaccine=int(form.vaccine.data)
        )
        db.session.add(Pets)
        db.session.commit()
        flash('新增寵物成功')
        return redirect(url_for('clinic_views.find_pet'))
    return render_template('chip_add.html', form=form)

@clinic_views.route('/clinic/edit_pet/<int:PetID>', methods=['GET', 'POST'])
@login_required
def edit_pet(PetID):
    """
    說明：更新寵物晶片資訊
    :param PetID:
    :return:
    """
    from ..models import pet
    pets = pet.query.filter_by(PetID=PetID).first_or_404()
    form = FormPetEdit()
    if form.validate_on_submit():
        pets.PetID=int(form.PetID.data)
        pets.UID=int(form.UID.data)
        pets.name=form.name.data
        pets.fur=form.fur.data
        pets.species=form.species.data
        pets.sex=int(form.sex.data)
        pets.variety=form.variety.data
        pets.vaccine=int(form.vaccine.data)
        db.session.add(pets)
        db.session.commit()
        flash('更新寵物成功')
        return redirect(url_for('clinic_views.pet_medicalrecord', PetID=PetID))
    form.PetID.data = str(pets.PetID)
    form.species.data = pets.species
    form.fur.data = pets.fur
    form.UID.data = str(pets.UID)
    form.name.data = pets.name
    form.sex.data = pets.sex
    form.variety.data = pets.variety
    form.vaccine.data = pets.vaccine
    # 利用參數action來做條件，判斷目前是新增還是編輯
    return render_template('chip_add.html', form=form, pets=pets, type='edit',PetID=PetID)

# @clinic_views.route('/user/petinfo/<PetID>')
# @login_required
# def pet_info(PetID):
#     """
#     說明：寵物資訊呈現
#     :param PetID:寵物ID
#     :return:
#     """
#     from ..models.user import pet
#     pets = pet.query.filter_by(PetID=PetID).all()
#     print(pets)
#     if pet is None:
#         abort(404)
#     return render_template('pet.html', pets=pets, action="medical")

@clinic_views.route('/clinic/find_pet', methods=['GET', 'POST'])
@login_required
def find_pet():
    """
    說明：查詢寵物
    :return:
    """
    from ..models.user import pet,medicalrecords
    form = FormFindPet()
    if form.validate_on_submit():
        pets = pet.query.filter_by(PetID=form.PetID.data).first()
        if pets:
            medicalrecords = medicalrecords.query.filter_by(PetID=form.PetID.data).all()
            return render_template('clinic_records.html', pets=pets, medicalrecords=medicalrecords, action="medical",PetID=form.PetID.data)
        flash('請確認輸入正確寵物晶片')
    return render_template('chip_query.html', form=form)

@clinic_views.route('/clinic/add_doctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    """
    說明：新增醫生
    :return:
    """
    clinic = get_clinic_data(current_user.ID)
    from ..models.user import clinic_doctor,user
    form = FormDoctor()
    clinic = clinic.query.filter_by(ID=current_user.ID).first()
    if form.validate_on_submit():
        doctors = clinic_doctor.query.filter_by(UID=form.UID.data,CID=clinic.CID).first()
        if doctors:
            flash('此會員已是該診所醫生')
            return render_template('add_doctor.html', form=form, action="manage")
        user = user.query.filter_by(UID=form.UID.data).first()
        if user:
            doctor = clinic_doctor(
                CID = clinic.CID,
                UID = int(form.UID.data)
            )
            db.session.add(doctor)
            db.session.commit()
            flash('新增成功')
            return redirect(url_for('clinic_views.doctor',ID=current_user.ID))
        flash('請輸入正確的會員編號')
        return render_template('add_doctor.html', form=form, action="manage")
    return render_template('add_doctor.html', form=form, action="manage")

@clinic_views.route('/clinic/doctor/<ID>')
@login_required
def doctor(ID):
    """
    說明：醫生資訊
    :param CID:診所編號
    :return:
    """
    clinic = get_clinic_data(ID)
    from ..models.user import clinic_doctor
    doctors = clinic_doctor.query.filter_by(CID=clinic.CID).all()
    if doctors is None:
        abort(404)
    return render_template('clinic_doctor.html', doctors=doctors, action="manage")


# 建立刪除的路徑
@clinic_views.route('/clinic/delete_doctor/<int:CID>/<int:UID>')
def delete_doctor(CID,UID):
    
    from ..models.user import clinic_doctor
    doctor_to_delete = clinic_doctor.query.filter_by(CID=CID,UID=UID).first()
    # 對查詢的id進行刪除
    try:
        db.session.delete(doctor_to_delete)
        db.session.commit()
        # 提示已刪除
        flash('內容已被刪除!')
        # 我們需要透過class從資料庫抓取文章，通過發布時間排序
        doctors = doctor_to_delete.query.filter_by(CID=CID).all()
        return render_template("clinic_doctor.html", doctors=doctors, action="manage")
    # 如果無法刪除
    except:
        flash('內容無法刪除，請再試一下！')
        # 我們需要透過class從資料庫抓取文章，通過發布時間排序
        doctors = clinic_doctor.query.filter_by(CID=CID).all()
        return render_template("clinic_doctor.html", doctors=doctors, action="manage")
 
@clinic_views.route('/clinic/add_medicalrecords/<PetID>', methods=['GET', 'POST'])
@login_required
def add_medicalrecord(PetID):
    """
    說明：新增病歷
    :return:
    """
    from ..models import medicalrecords
    #form = FormMedicalRecords(doctorList, medicationList)
    form = FormMedicalRecords()
    clinic = get_clinic_data(current_user.ID)
    if form.validate_on_submit():
        medicalrecord = medicalrecords(
            PetID=int(form.PetID.data),
            CID=int(clinic.CID),
            type=int(form.type.data),
            doctor=form.doctor.data,
            disease=form.disease.data,
            # medication=form.medication.data,
            note=form.note.data
        )
        db.session.add(medicalrecord)
        db.session.commit()
        flash('新增病歷成功')
    form.PetID.data = PetID
    form.CID.data = clinic.name

    medicationList = ['TULASIN INJ.', 'COZYFLOW', "FULICO ORAL SOL'N 20%", 'KANA-PS INJECTION', 'LEFUDUO 20', 'WATER FOR INJECTION "TAI YU"', 'TYLOSIN PHOSPHATE', 'TYLOSIN', 'TYLOSIN TARTRATE', 'BIORAL H120', 'REVOLUTION PLUS 1.0 ML', 'REVOLUTION PLUS 0.5 ML', 'REVOLUTION PLUS 0.25 ML', 'SERA POND OMNISAN F', 'SERA POND OMNIPUR', 'DOXICOR', 'SAMU TYLOSIN INJECTION', 'CERENIA', 'DERFUCOL-10 SOLUTION', 'OXY-22% POWDER', 'FEIYICHING', 'CEFA-SAFE', 'TIPAFAR', 'ENRODING', 'DOXYLIN-20-F', 'AMPROL 25％', 'SUCOGIN 8%', 'WORMCIDE S', 'ALFAXAN MULTIDOSE ANAESTHETIC INJECTION', 'TIACOLIN-100 INJECTION', 'GLEPTOFERRON LABIANA 200MG/ML', 'AVISAN MULTI', 'ANGESOL 50%', 'METABOL INJ.', 'SERA COSTAPUR F', 'SERA MYCOPUR', 'SERA POND CYPRINOPUR', 'SERA BAKTOPUR', 'CEPHASINE-150F', 'DPP INJECTION', 'DIAMICIN-20', 'THIAMPHENICOL-10-F', 'H.K.P. TIAMULIN 200 POWDER-FA', 'AMVET', 'OTOMAX', 'AMOXAL 150MG/ML INJECTABLE SUSPENSION', 'RABISIN', 'NASHER DOX 500', 'OTCAS', 'AMO-50-F', 'ONSIOR TABLETS FOR DOGS', 'RONAXAN 20％', 'TILMICOX SOLUCION', 'FLUMINE (ORAL SOLUTION)', 'TYLORATE SOL 20%', 'COLISOL (ORAL SOLUTION)', 'POLY AD', 'VITACEN AD3E', 'AMPHENOR', 'VIDALTA 15MG RETARDTABLETTEN FUR KATZEN', 'VIDALTA 10MG RETARDTABLETTEN FUR KATZEN', 'MOMETAMAX', 'FLORFENICOL', 'ANTIROBE AQUADROPS', 'KEFLEX-15-F', 'PYRIMETHAMINE-100', 'DOXYTON 7.5% POWDER', 'VENTO-DX', 'IVERMECTIN 0.6% POWDER', 'H.K.P. RELAXYZINE', 'SAMU AMOXY-50 POWDER', 'SAMU AMOXY-20 POWDER', 'PROTECTIER OTIC DROPS', 'LINCOMYCIN400 POWDER', 'PUREVAX RCPCH FELV', 'FORMOSA DOXYCYCLINE 50% WSP', 'OXYTETRACYCLINE500', '', 'COLISTIN ”AVICO”', 'IVM-6', 'TIAMULIN FUMARATE', 'MILBEMAX TABLETS FOR SMALL DOGS AND PUPPIES', 'MILBEMAX TABLETS FOR DOGS', 'QIUMIELIN S.A.', 'CHLORTETRACYCLINE S-55.5', 'ZHISOULING A.T.', 'COCCIAN S.A.', 'SULININ S.A.', 'AMOXICILLIN-500C A.T.', 'CORSINA', 'SHOTCOX', 'BACITRACIN METHYLENE DISALICYLATE', 'FORMOSA FLORCOM 20% ORAL SOLUTION', 'CARFLAM', 'CEPHASIN', 'COXIPOL 25%', 'COXIPOL 25%', 'CARFLAM', 'CARFLAM', 'PULMODOX DOXYCYCLINE 50 PORC', 'EFFITIX 26.8MG/240MG SPOT ON FOR VERY SMALL DOGS', 'FORMOSA AMOXICILLIN 50% ORAL POWDER', 'CORAZURIL-50 SOLUTION', '"KYOTO BIKEN" NEWCASTLE DISEASE-INFECTIOUS BRONCHITIS VACCINE', 'LINCOSPECTIN 110', 'DERFUCOL-10', 'TULATHROMYCIN SOLUTION FOR INJECTION', 'CLON 20% INJECTION', 'CYTOPOINT', 'VIME-FLUXIN', 'MILBEMAX FILM-COATED TABLETS FOR SMALL CATS AND KITTENS', 'PRRSII PRRS SUBUNIT VACCINE', 'COLISTIN SULFATE', 'IMIZOL INJECTION', 'PREVICOX', 'PREVICOX', 'TEVETSIN', 'NEOSTRUM 220', 'SULFA-LYLING', 'TECFLU', 'NASHER VLO 625', 'FLAVO 40 MICROFLORA MANAGEMENT SUPPLEMENT', 'FLAVO 80 MICROFLORA MANAGEMENT SUPPLEMENT', 'AVINEW', 'DOXYCYCLINE 20%ORAL SOLUTION', 'AMKILL', 'FORMOSA IVERMECTIN 0.6% ORAL POWDER', 'ONSIOR 20MG/ML SOLUTION FOR INJECTION FOR CATS AND DOGS', 'FORTEKOR 2.5', 'HUSHUKANG', 'FORMOSA IVERMECTIN SOLUTION 0.5%', 'FERTIPIG', 'CLOSTRISTOP', 'JINEAR', 'SABA', 'ENRODING', 'BEXEPRIL 20MG FILM-COATED TABLET FOR DOGS', 'BEXEPRIL 5MG FILM-COATED TABLET FOR DOGS', 'BEXEPRIL 2.5MG FILM-COATED TABLET FOR DOGS', 'FORMOSA DOXYCYCLINE 20% WSP', 'TYLOSIN', 'LT-BLEN', 'NASHER GENTA POWDER', 'H.K.P. COOL FREE', 'NEOXYFAC-176 S.A.', 'H.K.P.COLISTIN 11-FA', 'H.K.P. FLUMEQUINE 500', 'CORAZURIL-25 SOLUTION', 'DOXI 500', 'REEFCOX 5%', 'BICLOX SECADO', 'TONAVET', 'AMO-20-F', 'ENRODING', 'CYC NYSTACIDE 110', 'BIO-L CLONE IB', 'BUTOMIDOR 10MG/ML SOLUTION FOR INJECTION FOR DOGS AND CATS', 'DOXYCEN 200MG/ML', 'LIMIJIN S.A.', 'CYC TYLVALOCIDE-50', 'CLOSTRICOL', 'MILPRO 4 MG/10 MG COMPRIMES PELLICULES POUR PETITS CHATS ET CHATONS', 'MILPRO 16 MG/40 MG COMPRIMES PELLICULES POUR CHATS', 'MILPRO 2.5 MG/25 MG COMPRIMES PELLICULES POUR PETITS CHIENS ET CHIOTS', 'MILPRO 12.5 MG/125 MG COMPRIMES PELLICULES POUR CHIENS', 'DOX-20-F', 'CYC NYSTACIDE245', 'PRIMADOX500', 'BAYOVAC MHYO AND MHR BIVALENT INACTIVATED BACTERIN', 'FORMOSA AMOXICILLIN POWDER FOR INJECTABLE SUSPENSION', 'EFFIPRO DUO SPOT-ON SOLUTION FOR VERY LARGE CATS', 'EFFIPRO DUO SPOT-ON SOLUTION FOR CATS', 'H.K.P. TYLOSIN 667', 'FLEA-AWAY', 'NASHER ERY 500 POWDER', 'COLITIN-200 ORAL SOLUTION', 'AMOXILIN INJ.', 'TRICHO PLUS', 'TRICHOCURE', 'COXI PLUS', 'AVICAS', 'EMBOBATE-254', 'COLINJIN S.A.', 'H.K.P. CARBADOX 10%', 'PUREVAX RABIES', 'O TOTAL HEAL', 'VOLVAC ND+IB+EDS KV', 'INGELVAC H', 'VOLVAC ND CONC. KV', 'DOXY 200 ORAL', 'DRAXXIN 100 MG/ML SOLUTION FOR INJECTION', 'TENAMOXCIN 500 WSP', 'BUR 706', 'T. M. LIN POWER-20％', 'DECOQUINATE 6%', 'RONI-LYLING', 'H.K.P. OQAA-FA', 'H.K.P. CEPHALEXIN 150', 'ARSANOXYTEC 210P', 'KITASAFAC-500S', 'FORMOSA POVIDONE IODINE 5% TOPICAL SOLUTION', 'BAYTRIL 100 INJ.', 'BAYTRIL 50 INJ.', 'BAYTRIL 25 INJ.', 'SERESTO 4.50G+2.03G COLLAR FOR DOGS>8KG', 'PROCOX 0.9 MG/ML+18 MG/ML ORAL SUSPENSION FOR DOGS', 'BIOFORS APP SUB', 'FRONTLINE TRI-ACT DOG 40-60KG', 'FRONTLINE TRI-ACT DOG 20-40KG', 'FRONTLINE TRI-ACT DOG 10-20KG', 'FRONTLINE TRI-ACT DOG 5-10KG', 'FRONTLINE TRI-ACT DOG 2-5KG', 'EXZOLT 10MG/ML SOLUTION FOR USE IN DRINKING WATER FOR CHICKENS', 'ACETYLISOVALERYLTYLOSIN TARTRATE (TYLVALOSIN TARTRATE)', 'BIGOPEST', 'H.K.P. ERYTHROMYCIN 200', 'H.K.P. OXY 500', 'PNEUMODOG', 'PRIME IODINE', 'TOLTRAZURIL 5％', 'H.K.P. AMOXICILLIN 20', 'CHEIL TYLOSIN 220', 'ZURITOL 50MG/ML', '“SH” LINCOMYCIN 110 POWDER', 'SELAMAX 6％', 'AMOCIN POWDER-30%', 'HEXAMOR', 'CYROMAZINE 10', 'AVIFLOR-10', 'CYROMAZINE 100', '“SH” LINCOMYCIN 220 POWDER', 'HYOGEN', 'CEFALESIN-15-F', 'FLOROTECH PREMIX Y-10 “SGB”', 'AMOCIN Y-30 “SGB”', 'HIPRAVIAR-S', 'ONSIOR 6MG TABLETS FOR CATS', 'CIRCOQ PCV2 SUBUNIT VACCINE', 'HEART-SHIELD', 'NASHER LIN-SPEC INJ', 'BAYCOX IRON ORAL SUSPENSION', 'NEOMYCIN SULFATE', '“SH” AMOXICILLIN 300 POWDER', 'CLINACIN ORAL SOLUTION', 'TRI-LYLING', 'FLOR 10%', 'TYLOSIN PHOSPHATE', 'TYLOSIN TARTRATE', 'SELACIDE', 'TELAZOL', 'SERESTO 1.25G+0.56G COLLAR FOR CATS AND DOGS≦8KG', 'PORCILIS M HYO ID ONCE', 'SELACIDE', 'FULICO POWDER 10%', 'MEGANYL', 'MITEX EAR DROPS AND CUTANEOUS SUSPENSION FOR DOGS AND CATS', 'NOSIHEPTIDE', 'BAYCOX MULTI 50MG/ML ORAL SUSPENSION', 'BIOSON', 'CYC TIAMUNFAC 200', 'AMOXICILLIN 300', 'FORMOSA LINCOMYCIN INJECTION', 'FUMIZIN-50 SOLUTION', 'MYCOSTATIN 20', 'AMPROBAT-S', 'FORMOSA FLORCOM 10% ORAL SOLUTION', 'FLOCOL-200 SOL.', 'BIOX', 'TIAMULIN 45%', 'DOTTCYCLINE-500 S.A.', 'FLORFENICOL 10%', 'SEMINTRA 4MG/ML ORAL SOLUTION FOR CATS', 'HEMATICEN 200MG/ML', 'C.S. TRICHLORFON', 'FORMOSA FLORCOM 2% POWDER', 'TecEnro', 'FLORFENIS', 'CEFTIOFUR H INJ.', 'DOTTCYCLINE-200 A.T.', 'CEPHASIN 600', 'YUMAMYCIN 1% MICROGRANULATE', 'IVERMEC PI-272', 'IVERMEC PI-136', 'IVERMEC PI-68', 'IVERMEC PI-34', 'FLORFENIDEM 10%', 'DERMCARE PYOHEX MEDICATED SHAMPOO', 'BIO-L ND WON', 'FLUBENOL 5%', 'FLORFENICOL-100', 'ANFLOSYL INJ.', 'CETIFU-5 INJ.', 'TYLAN SOLUBLE 66.7%', 'APRALAN SOLUBLE 44.44%', 'BIOFORS IC GEL 0.25', 'HIPRASUIS AD', 'AMOXICILLIN 30%', 'VIRBAGEN OMEGA', 'EMECTIN', 'PORCILIS PCV M HYO', 'FOSTERA PCV METASTIM', 'AMOXICILLIN-300 S.A.', 'TIAMULIN 200', 'FOLORDOX S-200', 'KOLISTIN-20 SOLUTION', 'OXYTESTRUM 500', 'MILBEMAX FILM-COATED TABLETS FOR CATS', 'ENRAMYCIN-4%"SGB"', '', 'LINCOMYCIN HYDROCHLORIDE', 'ENRAMYCIN 80 S.A.', 'MEGLUXIN', 'GALLIVAC IB88 NEO', '', 'FOSTERA PCV MH', 'PRISOLON INJECTION "SGB"', 'MEDIFLUM WATER SOLUBLE POWDER', 'PREVIRON', 'BIORAL H120 NEO', 'SELAMECTIN 12％', 'ZENOVITAN AD3E INJECTION', 'K. T. ANTI TRICHOMONAS POWDER', 'POULVAC BURSAPLEX', 'IVERMECTIN', 'FUNGLCIDINE-80', 'MOMETAMAX', 'COFAMOX 50', 'SIMPARICA 120 MG', 'SIMPARICA 80 MG', 'SIMPARICA 20 MG', 'SIMPARICA 10 MG', 'SIMPARICA 5 MG', 'SIMPARICA 40 MG', 'FULETIN 20', 'GESTAVET HCG 1000/ PMSG 2000', 'TRISOL ORAL POWDER', 'PHARMASIN 250MG/G PREMIX FOR MEDICATED FEEDING STUFF', 'DECLEAN S.A.', 'ENRAMYCIN S.A.', 'PORCEPTAL 4 MICROGRAM/ML INJECTABLE SOLUTION FOR PIGS', 'H.K.P. FLORFENICOL 20%', 'AMITAS', 'NEOMYCIN 220 A.T.', 'EREI-CFA', 'NEMUTIN 10% PREMIX', 'VETMEDIN 5.0MG CHEWABLE TABLETS', 'TONKEY 200', 'CLOPIDOL', 'STAT-CLEAN', "TILMICOSIN ''AVICO''", 'PRAC-TIC 56.25MG SPOT-ON SOLUTION FOR VERY SMALL DOGS', 'TYLOLISTIN', 'MEDICOL', 'PRAC-TIC 275MG SPOT-ON SOLUTION FOR MEDIUM DOGS', 'PRAC-TIC 137.5MG SPOT-ON SOLUTION FOR SMALL DOGS', 'PRAC-TIC 625MG SPOT-ON SOLUTION FOR LARGE DOGS', 'EASY WASH', 'DEPASS', 'TERRAMICINA L.A 200MG/ML SOLUCION INYECTABLE', 'NOBILIS RT+IBMULTI+ND+EDS', 'INVEMOX 15％ L.A.', 'FLEA-AWAY SPRAY', 'IVERMECTIN PLUS TABLETS-M', 'LEAVEWORM TABLETS', 'APOQUEL 16MG', 'ARMOLIN-15 INJ.', 'DRONTAL PLUS TASTY 150/144/50 MG TABLETS FOR DOGS', 'INSECTICIDAL ACARICIDAL DROPS（BARS） FOR DOG', 'PAO TAO LINCOMYCIN 400', 'APOQUEL 3.6MG', 'SU LI CHIEN', 'CYC ANTI-DIARRHEA', 'NASHER COUGH INJECTION', 'CEVAC IBIRD', 'MILBEEXPEL 2.5', 'MILBEEXPEL 1.25', 'IVERMECTIN PLUS TABLETS-S', 'CEFLIN/LA', 'NEXGARD SPECTRA', 'NEXGARD SPECTRA', 'NEXGARD SPECTRA', 'NEXGARD SPECTRA', 'NEXGARD SPECTRA', 'IVERMECTIN PLUS TABLETS-L', 'APOQUEL 5.4MG', 'CEFURO OINTMENT', 'FLUBENDAZOLE 5%', 'NORVAX STREP SI', 'RADIN PLUS', 'RADINCURE', 'TOLTRARIL 50', 'CHLORTETRACYCLINE HYDROCHLORIDE', 'CEFLIN INJ.', 'CEVAXEL-RTU 50MG/ML', 'VIME-ATP', 'UNISTRAIN PRRS', 'EFFITIX 67MG/ 600MG SPOT ON FOR SMALL DOGS', 'EFFITIX 268MG/ 2400MG SPOT ON FOR LARGE DOGS', 'EFFITIX 134MG/1200MG SPOT ON FOR MEDIUM DOGS', 'PAO TAO FU LE TE-30 INJECTION', 'FOSTERA PRRS', 'CHEIL ENRAMYCIN-80', 'LUPICK OINT', 'NOSIHEPTIDE', 'HIPRASUIS AD BK', 'CEFPULMON', 'TA-FOONG SWINE PSEUDORABIES GENE-DELETED AND ATROPHIC RHINTIS RECOMBINANT TOXIN INACTIVATED COMBINED BACTERIN(OIL ADJUVANT)', 'CRYOMAREX RISPENS', 'AMOLIN 50', 'FOLORDOX S-100', 'BIOFORS ND-IB-IC-EDS 0.25', 'ERYSENG', 'ERYSENG PARVO', 'POULVAC IN+B', 'TYLOSIN TARTRATE', 'METAMIZOLE SODIUM', 'CARNIDAZOL TABLETS 10MG "C.C.P.C"', 'DOXYCYCLINE HYCLATE', 'BREATHBEST', 'TIAMULIN 450', 'TIAMULIN 200', 'TRIPRIM', 'KOBI PLUS', 'PCCOM PCV2 AND PRRS SUBUNIT VACCINE', 'BAYTRIL MAX', 'CEVAC TRANSMUNE', 'YUZHUAZ S.A.', 'LIKETONG S.A.', 'BRAVECTO 1400MG', 'BRAVECTO 250MG', 'BRAVECTO 1000MG', 'BRAVECTO 500MG', 'BRAVECTO 112.5MG', 'TOLTRACOX ORAL SUSPENSION 5%', 'TOLTRACOX SOLUTION 2.5%', 'COCCI PRO', 'SUIVET']
    # 取得該診所的醫生清單
    # doctors = session.query(subq.c.name, Address.address).join(subq, subq.c.id == Address.user_id)
    doctors = ['A', 'B', 'C']
    
    return render_template('add_records.html', form=form, medicationList=medicationList, doctors=doctors, action="medical",type='add',PetID=PetID)

@clinic_views.route('/clinic/edit_medicalrecord/<int:MID>', methods=['GET', 'POST'])
@login_required
def edit_medicalrecord(MID):
    """
    說明：更新病歷資訊
    :param PetID:
    :return:
    """
    from ..models import medicalrecords
    medicalrecord = medicalrecords.query.filter_by(MID=MID).first_or_404()
    form = FormMedicalRecords()
    if form.validate_on_submit():
        # medicalrecord.MID=int(form.MID.data)
        medicalrecord.PetID=int(form.PetID.data)
        medicalrecord.CID=form.CID.data
        medicalrecord.type=form.type.data
        medicalrecord.doctor=form.doctor.data
        medicalrecord.disease=form.disease.data
        # medicalrecord.medication=form.medication.data
        medicalrecord.note=form.note.data

        db.session.add(medicalrecord)
        db.session.commit()
        flash('更新病歷成功')
        return redirect(url_for('clinic_views.pet_singlemedicalrecord',MID=MID))
        # return redirect(url_for('clinic_views.pet_info', MID=medicalrecord.MID , medicalrecords=medicalrecord, action="medical",PetID=form.PetID.data))

    # form.MID.data = str(medicalrecord.MID)
    form.PetID.data = str(medicalrecord.PetID)
    form.CID.data = medicalrecord.CID
    form.type.data = medicalrecord.type
    form.doctor.data = medicalrecord.doctor
    form.disease.data = medicalrecord.disease
    # form.medication.data = medicalrecord.medication
    form.note.data = medicalrecord.note

    # 利用參數action來做條件，判斷目前是新增還是編輯
    return render_template('add_records.html', form=form,MID=MID, medicalrecords=medicalrecord, action='edit', action1="medical",PetID=form.PetID.data)


@clinic_views.route('/clinic/pet_medicalrecord/<PetID>', methods=['GET', 'POST'])
@login_required
def pet_medicalrecord(PetID):
    """
    說明：寵物所有病歷資料
    :param NID:病歷編號
    :return:
    """
    from ..models.user import medicalrecords
    medicalrecords = medicalrecords.query.filter_by(PetID=PetID).all()
    if medicalrecords is None:
        abort(404)
    return render_template('clinic_records.html', medicalrecords=medicalrecords, action="medical",PetID=PetID)

@clinic_views.route('/clinic/pet_siglemedicalrecord/<MID>', methods=['GET', 'POST'])
@login_required
def pet_singlemedicalrecord(MID):
    """
    說明：寵物單一病歷資料
    :param NID:病歷編號
    :return:
    """
    from ..models.user import medicalrecords
    medicalrecords = medicalrecords.query.filter_by(MID=MID).first()
    if medicalrecords is None:
        abort(404)
    return render_template('detailed_records.html', medicalrecords=medicalrecords , action="medical",MID=MID,PetID=medicalrecords.PetID)

# @clinic_views.route('/clinic/pet_all_medicalrecords/<PetID>', methods=['GET', 'POST'])
# @login_required
# def pet_all_medicalrecord(PetID):
#     """
#     說明：寵物近期病歷資料
#     :param PetID:病歷編號
#     :return:
#     """
#     from ..models.user import medicalrecords
#     medicalrecords = medicalrecords.query.filter_by(PetID=PetID).all()
#     if medicalrecords is None:
#         abort(404)
#     return render_template('medical_records.html', medicalrecords=medicalrecords)


@clinic_views.route('/clinic/medicalrecords/<ID>', methods=['GET', 'POST'])
@login_required
def medicalrecords(ID):
    """
    說明：所有病歷資料
    :param CID:診所編號
    :return:
    """
    clinic = get_clinic_data(ID)
    CID=clinic.CID
    doctors = []
    from ..models.user import medicalrecords
    medicalrecords = medicalrecords.query.filter_by(CID=CID).all()
    print("++++++++")
    for record in medicalrecords:
        print(record.time)

    if medicalrecords is None:
        abort(404)
    # 依據使用者自訂條件篩選 medicalrecords 資料
    if request.method == 'POST':
        doctor_name = request.form['doctor_name']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        print("=========")
        print(start_date)
        print(end_date)
        from ..models.user import medicalrecords
        medicalrecords = medicalrecords.query.filter(
            medicalrecords.CID == CID,
            medicalrecords.doctor == doctor_name,
            medicalrecords.time >= start_date,
            medicalrecords.time <= end_date
            ).all()
        if medicalrecords is None:
            medicalrecords = []

    # 取得 doctors list
    doctors = []
    for medicalrecord in medicalrecords:
        doctor = medicalrecord.doctor
        if doctor not in doctors: 
            doctors.append(doctor)
    return render_template('medical_records.html', medicalrecords=medicalrecords , doctors = doctors, action="manage")




