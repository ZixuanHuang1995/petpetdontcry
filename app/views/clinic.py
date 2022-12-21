from flask import Blueprint, render_template,abort, jsonify, request, send_from_directory, flash, redirect, url_for
import flask
from flask_login import login_user,current_user,login_required,logout_user
from ..form.clinicForm import FormPet,FormDoctor, FormMedicalRecords,FormFindPet
from ..database import db
from ..config_other import photos
from ..controllers import (
    get_clinic_data
)
# from flask import Flask
# app = Flask(__name__,static_url_path='/static')
clinic_views = Blueprint('clinic_views', __name__, template_folder='../templates')

@clinic_views.route('/clinic/home')
def home():
    return render_template('clinic_home.html')

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
    if form.validate_on_submit():
        file_name = photos.save(form.picture.data)
        Pets = pet(
            PetID=int(form.PetID.data),
            UID=int(form.UID.data),
            name=form.name.data,
            fur=form.fur.data,
            picture=file_name,
            species=form.species.data,
            sex=form.sex.data,
            variety=form.variety.data,
            vaccine=form.vaccine.data,
        )
        db.session.add(Pets)
        db.session.commit()
        flash('新增寵物成功')
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
    form = FormPet()
    if form.validate_on_submit():
        file_name = photos.save(form.picture.data)
        pets.PetID=int(form.PetID.data)
        pets.UID=int(form.UID.data)
        pets.name=form.name.data
        pets.fur=form.fur.data
        pets.picture=file_name
        pets.species=form.species.data
        pets.sex=form.sex.data
        pets.variety=form.variety.data
        pets.vaccine=form.vaccine.data
        db.session.add(pets)
        db.session.commit()
        flash('更新寵物成功')
        return redirect(url_for('clinic_views.pet_info', PetID=PetID))
    form.PetID.data = str(pets.PetID)
    form.species.data = pets.species
    form.fur.data = pets.fur
    form.picture.data = pets.picture
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
        # site_contents(form.PetID.data)
        pets = pet.query.filter_by(PetID=form.PetID.data).all()
        medicalrecords = medicalrecords.query.filter_by(PetID=form.PetID.data).all()
        return redirect(url_for('clinic_views.pet_medicalrecord',PetID=form.PetID.data))
        
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
    print(form.validate_on_submit())
    print(form.type.data)
    print(form.validate())
    print(form.is_submitted())
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
    return render_template('add_records.html', form=form, action="medical",type='add',PetID=PetID)

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
    from ..models.user import medicalrecords
    medicalrecords = medicalrecords.query.filter_by(CID=clinic.CID).all()
    if medicalrecords is None:
        abort(404)
    return render_template('medical_records.html', medicalrecords=medicalrecords, action="manage")

@clinic_views.route('/clinic/medicalrecords/<CID>', methods=['POST'])
@login_required
def medicalrecords_filter(CID):
    from ..models.user import medicalrecords
    doctor_name = request.form['doctor_name']
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    medicalrecords = medicalrecords.query.filter(doctor=doctor_name).all()
    if start_date and end_date:
        medicalrecords = medicalrecords.query.filter(medicalrecords.time < end_date, medicalrecords.time >= start_date).all()
    if medicalrecords is None:
        abort(404)
    return render_template('medical_records.html', medicalrecords=medicalrecords, action="manage")



