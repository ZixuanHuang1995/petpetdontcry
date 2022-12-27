import imp
from flask import Blueprint, render_template,abort, jsonify, request, send_from_directory, flash, redirect, url_for
import os
from ..config_other import photos
from APP.models.user import account, published
from .indexView import index_views
from flask_login import login_user,current_user,login_required,logout_user
from werkzeug.utils import secure_filename
from ..controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
    get_user_data,
    get_pet_all_medicalrecords,
    get_pet_all_vaccinerecords
)
from ..form.userForm import FormRegister,FormUserInfo,FormAddUserInfo,FormChangePWD
from ..form.publishedForm import FormPublished, FormeditPublished
from ..database import db

user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/knowledge/food')
def food():
    return render_template('knowledge_food.html')

@user_views.route('/knowledge/medication')
def medication():
    return render_template('knowledge_medication.html')

@user_views.route('/knowledge/shelter')
def shelter():
    return render_template('knowledge_shelter.html')

@user_views.route('/')
@login_required
def home():
    return render_template('home.html')

@user_views.route('/users', methods=['GET'])
def get_user_page():
    users = get_all_users()
    return render_template('users.html', users=users)

@user_views.route('/api/users', methods=['GET'])
def get_users_action():
    users = get_all_users_json()
    return jsonify(users)

@user_views.route('/api/users', methods=['POST'])
def create_user_endpoint():
    data = request.json
    create_user(data['username'], data['password'])
    return jsonify({'message': f"user {data['username']} created"})

@user_views.route('/users', methods=['POST'])
def create_user_action():
    data = request.form
    flash(f"User {data['username']} created!")
    create_user(data['username'], data['password'])
    return redirect(url_for('user_views.get_user_page'))
    
@user_views.route('/static/users', methods=['GET'])
def static_user_page():
  return send_from_directory('static', 'static-user.html')

@user_views.route('/test')  
@login_required 
def test_index():  
    flash('flash-1')  
    # flash('flash-2')  
    # flash('flash-3')  
    return render_template('base.html')  
"""
說明：上面皆是先測試，之後可能用得到
"""  
@user_views.route('/user/register',methods=['GET','POST'])
def user_register():
    """
    說明：註冊使用者
    :return:
    """
    from ..models import account
    form = FormRegister()

    if form.validate_on_submit():
        if account.query.filter_by(email=form.email.data).first():
            flash('Email已經被註冊過了')
            return render_template('test.html',form = form)
        accounts = account(
            email = form.email.data,
            password = form.password.data,
            role = 'user'
        )
        db.session.add(accounts)
        db.session.commit()
        return redirect(url_for('index_views.login'))

    return render_template('test.html',form = form)

@user_views.route('/user/add_userinfo/<ID>', methods=['GET', 'POST'])
def add_userinfo(ID):
    from ..models import user,account
    accounts = account.query.filter_by(ID=ID).first()
    form = FormAddUserInfo()
    if form.validate_on_submit():
        print(current_user)
        user = user(
            name = form.name.data,
            phone = form.phone.data,
            identity = form.identity.data,
            ID = ID
        )
        accounts.first = True
        db.session.add(user,account)
        db.session.commit()
        #  在編輯個人資料完成之後，將使用者引導到使用者資訊觀看結果
        flash('基本資料更新成功')
        return redirect(url_for('user_views.home'))
    return render_template('test_addinfo.html',form = form)

@user_views.route('/user/edit_userinfo/<ID>', methods=['GET', 'POST'])
@login_required
def edit_user_info(ID):
    users = get_user_data(ID)
    """
    說明：更新使用者資訊
    :return:
    """
    form = FormUserInfo()
    form1 = FormChangePWD()
    if form.validate_on_submit():
        users.name = form.name.data
        users.phone = form.phone.data
        db.session.add(users)
        db.session.commit()
        #  在編輯個人資料完成之後，將使用者引導到使用者資訊觀看結果
        flash('基本資料更新成功')
        return redirect(url_for('user_views.edit_user_info',ID=ID))
    if form1.validate_on_submit():
        #  透過current_user來使用密碼認證，確認是否與現在的密碼相同
        if current_user.check_password(form1.password_old.data):
            current_user.password = form1.password_new.data
            db.session.add(current_user)
            db.session.commit()
            flash('你已經改密碼成功，請重新登入')
            return redirect(url_for('index_views.logout'))
        else:
            flash('錯誤的密碼')
    #  預設表單欄位資料為current_user的目前值
    form.UID.data = users.UID
    form.identity.data = users.identity
    form.email.data = current_user.email
    form.name.data = users.name
    form.phone.data = users.phone
    print("errr",users.name)
    return render_template('user_data.html', form=form,form1=form1)

@user_views.route('/user/addpublished', methods=['GET', 'POST'])
@login_required
def add_publshed():
    """
    說明：刊登遺失寵物資訊
    :return:
    """
    form_type = 'add'
    if request.method == 'POST':
        form_type = 'add'
        users = get_user_data(current_user.ID)
        post_type = request.form['post_type']
        title = request.form['title']
        pets_type = request.form['pets_type']
        fur = request.form['fur']
        depiction = request.form['depiction']
        sex = request.form['pet_sex']
        variety = request.form['variety']
        county= request.form['county']
        district= request.form['district']
        photo = request.files['file']

        # 照片上傳
        filename = ''
        UPLOAD_FOLDER = 'APP/static/uploads/'
        ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

        def allowed_file(filename):
            return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

        if photo.filename == '':
            flash('尚未上傳照片')
            return redirect(request.url)
        if photo and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            photo.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            flash('請上傳照片格式')
            return redirect(request.url)

        from ..models import published
        form = FormPublished()
        Publishing = published(
            title=title,
            species=pets_type,
            fur=fur,
            picture=filename,
            depiction=depiction,
            sex = int(sex),
            variety = variety,
            type= int(post_type),
            UID = int(users.UID),
            activate=True,
            county=county,
            district=district
        )
        db.session.add(Publishing)
        db.session.commit()
        flash("刊登成功")
    return render_template('user_postlist.html', type=form_type)

@user_views.route('/user/mypublished')
@login_required
def published_info():
    """
    說明：我的刊登資訊呈現
    :return:
    """
    users = get_user_data(current_user.ID)
    from ..models.user import published
    publisheds = published.query.filter_by(UID=users.UID).all()
    if publisheds is None:
        abort(404)
    return render_template('user_list.html', publisheds=publisheds)


@user_views.route('/user/mypet')
@login_required
def pet_info():
    """
    說明：我的寵物資訊呈現
    :param UID:使用者UID
    :return:
    """
    users = get_user_data(current_user.ID)
    print(users)
    from ..models.user import pet
    pets = pet.query.filter_by(UID=users.UID).all()
    print(pets)
    # pets_medicalrecords = medicalrecords.query.filter_by(PetID=pets.PetID).all()
    if pets is None:
        abort(404)
    return render_template('user_pet.html', pets=pets)

@user_views.route('/user/petrecord/<PetID>', methods=['GET', 'POST'])
def pet_record(PetID):
    from ..models.user import medicalrecords 
    medicalrecords = medicalrecords.query.filter_by(PetID=PetID).all()
    if medicalrecords is None:
        abort(404)
    print("test",medicalrecords)
    return render_template('user_pet.html', medicalrecords=medicalrecords)


@user_views.route('/user/petssss')
@login_required
def pet_medicalrecords():
    """
    說明：我的寵物資訊呈現
    :param UID:使用者UID
    :return:
    """
    # def submit():
    #由于POST、GET獲取資料的方式不同，需要使用if陳述句進行判斷
    if request.method == "POST":
        # 從前端拿數據
        PetID = request.form.get("PetID")
    if request.method == "GET":
        PetID = request.args.get("PetID")
    print(PetID)
    print(get_pet_all_medicalrecords(PetID))
    #如果獲取的資料為空
    if len(PetID) == 0:
        # 回傳的形式為 json
        return {'message':"error!"}
    else:
        return {'message':"success!",'pets_medicalrecords':get_pet_all_medicalrecords(PetID)}
    
@user_views.route('/user/petrrrr')
@login_required
def pet_vaccinerecords():
    """
    說明：我的寵物資訊呈現(疫苗)
    :param UID:使用者UID
    :return:
    """
    #由于POST、GET獲取資料的方式不同，需要使用if陳述句進行判斷
    if request.method == "POST":
        # 從前端拿數據
        PetID = request.form.get("PetID")
    if request.method == "GET":
        PetID = request.args.get("PetID")
    print(PetID)
    print(get_pet_all_vaccinerecords(PetID))
    #如果獲取的資料為空
    if len(PetID) == 0:
        # 回傳的形式為 json
        return {'message':"error!"}
    else:
        return {'message':"success!",'pets_vaccinerecords':get_pet_all_vaccinerecords(PetID)}


@user_views.route('/user/edit_published/<int:PublishedID>', methods=['GET', 'POST'])
@login_required
def edit_publshed(PublishedID):
    """
    更新publshed
    :param PublishedID:
    :return:
    """
    users = get_user_data(current_user.ID)
    from ..models import published
    Publishing = published.query.filter_by(PublishedID=PublishedID).first_or_404()
    form = FormeditPublished()

    print( form.validate_on_submit())
    print( form.validate())
    print( form.is_submitted())

    if form.validate_on_submit():
        Publishing.PublishedID = PublishedID
        Publishing.title=form.title.data
        Publishing.species=form.species.data
        Publishing.fur=form.fur.data
        Publishing.depiction=form.depiction.data
        Publishing.sex=form.sex.data
        Publishing.variety=form.variety.data
        Publishing.type=int(form.type.data)
        Publishing.UID=users.UID
        Publishing.activate=True
        Publishing.county=form.county.data
        Publishing.district=form.district.data
        db.session.add(Publishing)
        db.session.commit()
        flash('刊登資料更新成功')
        return redirect(url_for('user_views.published_info', UID=Publishing.UID))
        
    form.title.data = Publishing.title
    form.species.data = Publishing.species
    form.fur.data = Publishing.fur
    form.depiction.data = Publishing.depiction
    form.sex.data = str(Publishing.sex)
    form.county.data=Publishing.county
    form.district.data=Publishing.district
    form.variety.data = Publishing.variety
    # 單選預設是str，但資料庫是int，所以要改型態才會顯示
    form.type.data = str(Publishing.type)

    # 利用參數action來做條件，判斷目前是新增還是編輯
    return render_template('user_postlist.html', form=form, type='edit',PublishedID=PublishedID)

@user_views.route('/miss', methods=['GET', 'POST'])
def miss_data():
    """
    說明：所有刊登資訊呈現
    :return:
    """
    from ..models.user import published
    publisheds = published.query.filter(published.activate == 1).filter(published.type.in_([1, 2]))
    if publisheds is None:
        abort(404)

    # 依據使用者自訂條件篩選 published 資料
    if request.method == 'POST':
        county = request.form['county']
        district = request.form['district']
        post_type = request.form['post_type']
        pets_type = request.form['pets_type']
        sex = request.form['pet_sex']
        
        publisheds = published.query.filter(published.activate == 1)
        if county:
            publisheds = publisheds.filter(published.county == county)
        if district:
            publisheds = publisheds.filter(published.district == district)
        if pets_type:
            publisheds = publisheds.filter(published.species == pets_type)    
        if sex:
            publisheds = publisheds.filter(published.sex == sex)
        if post_type:
            publisheds = publisheds.filter(published.type == post_type)  
        else :
            publisheds = publisheds.filter(published.type.in_([1, 2])) 

        if publisheds is None:
            publisheds = []

    return render_template('miss.html', publisheds=publisheds,action="miss")

@user_views.route('/adoption', methods=['GET', 'POST'])
def adoption_data():
    """
    說明：所有刊登資訊呈現
    :return:
    """
    from ..models.user import published
    publisheds = published.query.filter_by(type=3,activate=1).all()
    if publisheds is None:
        abort(404)
    # 依據使用者自訂條件篩選 published 資料
    if request.method == 'POST':
        county = request.form['county']
        district = request.form['district']
        pets_type = request.form['pets_type']
        sex = request.form['pet_sex']
        from ..models.user import published
        publisheds = published.query.filter(published.activate == 1).filter(published.type == 3)
        if county:
            publisheds = publisheds.filter(published.county == county)
        if district:
            publisheds = publisheds.filter(published.district == district)
        if pets_type:
            publisheds = publisheds.filter(published.species == pets_type)    
        if sex:
            publisheds = publisheds.filter(published.sex == sex)    

        if publisheds is None:
            publisheds = []
    return render_template('miss.html', publisheds=publisheds)


@login_required
def mypet_medicalrecord(MID):
    """
    說明：我寵物病歷
    :return:
    """
    from ..models.user import medicalrecords, clinic
    medicalrecords = medicalrecords.query.filter_by(MID=MID).all()
    if medicalrecords is None:
        abort(404)
    return render_template('user_detailedrecords.html', medicalrecords=medicalrecords)
    
@user_views.route('/miss/<publishedID>')
def miss_detailed(publishedID):
    """
    說明：單一刊登資料
    :return:
    """
    from ..models.user import published,user,account
    published = published.query.filter_by(PublishedID=publishedID).first()
    user = user.query.filter_by(UID=published.UID).first()
    account = account.query.filter_by(ID=user.ID).first()
    if published is None or user is None:
        abort(404)
    print(user)
    return render_template('miss_detailed.html', published=published,account=account,user=user)

@user_views.route('/editstatus/<PublishedID>')
@login_required
def edit_status(PublishedID):
    """
    說明：更改刊登狀態
    :return:
    """
    from ..models.user import published
    published = published.query.filter_by(PublishedID=PublishedID).first()
    print("TEST",published.activate)
    if published.activate == True:
        published.activate = False
    else:
        published.activate = True
    db.session.add(published)
    db.session.commit()
    return redirect(url_for('user_views.published_info'))

