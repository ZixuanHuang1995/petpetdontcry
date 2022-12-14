from flask import Blueprint, render_template,abort, jsonify, request, send_from_directory, flash, redirect, url_for
import flask
from flask_login import login_user,current_user,login_required,logout_user
from ..form.clinicForm import FormLogin,FormPet,FormDoctor
from ..database import db
from ..config_other import photos
# from flask import Flask
# app = Flask(__name__,static_url_path='/static')
clinic_views = Blueprint('clinic_views', __name__, template_folder='../templates')

@clinic_views.route('/testclinic')
@login_required
def test_index():
    flash('flash-1')  
    # flash('flash-2')  
    # flash('flash-3')  
    return render_template('base.html')  

@clinic_views.route('/clinic/login', methods=['GET', 'POST'])
def login(): 
    """
    說明：登入
    :return:
    """
    from ..models import clinic
    form = FormLogin()
    if form.validate_on_submit():
        clinics = clinic.query.filter_by(account=form.account.data).first()
        if clinics:
            if clinics.check_password(form.password.data):
                login_user(clinics,form.remember_me.data)
                next = request.args.get('next')
                if not next_is_valid(next):
                    return 'ERRRRRRRR'
                # return 'Welcome:'+current_user.name
                return redirect(next or url_for('clinic_views.test_index'))
            else:
                flash('Wrong Email or Password')
        else:
            flash('Wrong Email or Password')
    return render_template('login.html',form=form) 

 #  加入function
def next_is_valid(url):
    """
    為了避免被重新定向的url攻擊，必需先確認該名使用者是否有相關的權限，
    舉例來說，如果使用者調用了一個刪除所有資料的uri，那就GG了，是吧 。
    :param url: 重新定向的網址
    :return: boolean
    """
    return True 
  
@clinic_views.route('/clinic/logout')  
@login_required
def logout():  
    """
    說明：登出
    :return:
    """
    logout_user()
    flash('Logout See You')
    return redirect(url_for('clinic_views.login'))
    
@clinic_views.route('/clinic/addpet', methods=['GET', 'POST'])
@login_required
def add_pet():
    """
    說明：新增寵物
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
    return render_template('addpublished.html', form=form)

@clinic_views.route('/clinic/editpet/<int:PetID>/', methods=['GET', 'POST'])
@login_required
def edit_pet(PetID):
    """
    說明：更新寵物資訊
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
        return redirect(url_for('clinic_views.pet_info', PetID=pets.PetID))
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
    return render_template('addpublished.html', form=form, pets=pets, action='edit')

@clinic_views.route('/user/petinfo/<PetID>')
@login_required
def pet_info(PetID):
    """
    說明：寵物資訊呈現
    :param PetID:寵物ID
    :return:
    """
    from ..models.user import pet
    pets = pet.query.filter_by(PetID=PetID).all()
    print(pets)
    if pet is None:
        abort(404)
    return render_template('pet.html', pets=pets)

@clinic_views.route('/clinic/adddoctor', methods=['GET', 'POST'])
@login_required
def add_doctor():
    """
    說明：新增醫生
    :return:
    """
    from ..models.user import clinic_doctor
    form = FormDoctor()
    if form.validate_on_submit():
        doctor = clinic_doctor(
            CID=current_user.CID,
            UID=int(form.UID.data)
        )
        db.session.add(doctor)
        db.session.commit()
        flash('新增寵物成功')
        return redirect(url_for('clinic_views.doctor', CID=current_user.CID))
    return render_template('doctor.html', form=form)
@clinic_views.route('/clinic/doctor/<CID>')
@login_required
def doctor(CID):
    """
    說明：醫生資訊
    :param CID:診所編號
    :return:
    """
    from ..models.user import clinic_doctor
    doctors = clinic_doctor.query.filter_by(CID=CID).all()
    if doctors is None:
        abort(404)
    return render_template('doctor_test.html', doctors=doctors)

# 建立刪除的路徑
@clinic_views.route('/clinic/deletedoctor/<int:CID>/<int:UID>')

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
        return render_template("doctor_test.html", doctors=doctors)
    # 如果無法刪除
    except:
        flash('內容無法刪除，請再試一下！')
        # 我們需要透過class從資料庫抓取文章，通過發布時間排序
        doctors = clinic_doctor.query.filter_by(CID=CID).all()
        return render_template("doctor_test.html", doctors=doctors)
 