import imp
from flask import Blueprint, render_template,abort, jsonify, request, send_from_directory, flash, redirect, url_for
import flask
from ..config_other import photos
from APP.models.user import published
from .index import index_views
from flask_login import login_user,current_user,login_required,logout_user
from werkzeug.utils import secure_filename
from ..controllers.auth import clinic_or_user
from ..controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
    get_user_data
)
from ..form.userForm import FormRegister,FormUserInfo,FormAddUserInfo
from ..form.publishedForm import FormPublished
from ..database import db
user_views = Blueprint('user_views', __name__, template_folder='../templates')

@user_views.route('/test')
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
        accounts = account(
            email = form.email.data,
            password = form.password.data,
            role = 'user'
        )
        db.session.add(accounts)
        db.session.commit()
        # return 'Success!', current_user.ID
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
            account = ID
        )
        accounts.first = True
        db.session.add(user,account)
        db.session.commit()
        #  在編輯個人資料完成之後，將使用者引導到使用者資訊觀看結果
        flash('You Have Already Edit Your Info')
        return 'ok'
    return render_template('test.html',form = form)


# ******

@user_views.route('/user/edit_userinfo/<ID>', methods=['GET', 'POST'])
@login_required
def edit_user_info(ID):
    from ..models import user,account
    users = user.query.filter_by(account=ID).first()
    """
    說明：更新使用者資訊
    :return:
    """
    form = FormUserInfo()
    if form.validate_on_submit():
        users.name = form.name.data
        users.phone = form.phone.data
        db.session.add(current_user)
        db.session.commit()
        #  在編輯個人資料完成之後，將使用者引導到使用者資訊觀看結果
        flash('You Have Already Edit Your Info')
        return redirect(url_for('user_views.user_info', UID=users.UID))
    #  預設表單欄位資料為current_user的目前值
    form.UID.data = users.UID
    form.identity.data = users.identity
    form.email.data = current_user.email
    form.name.data = users.name
    form.phone.data = users.phone
    return render_template('user_data.html', form=form)

# @user_views.route('/user/userinfo/<ID>')
# @login_required
# def user_info(ID):
#     """
#     說明：使用者資訊呈現
#     :param UID:使用者UID
#     :return:
#     """
#     user = get_user_data(ID)
#     if user is None:
#         abort(404)
#     return render_template('user_data.html', user=user)

@user_views.route('/user/addpublished', methods=['GET', 'POST'])
@login_required
def add_publshed():
    """
    說明：刊登遺失寵物資訊
    :return:
    """
    clinic_or_user('user')
    from ..models import published
    form = FormPublished()
    if form.validate_on_submit():
        file_name = photos.save(form.picture.data)
        Publishing = published(
            title=form.title.data,
            species=form.species.data,
            fur=form.fur.data,
            picture=file_name,
            area=form.area.data,
            depiction=form.depiction.data,
            sex=form.sex.data,
            variety=form.variety.data,
            type=int(form.type.data),
            UID=current_user.UID,
            activate=True
        )
        db.session.add(Publishing)
        db.session.commit()
        flash('Create New Blog Success')
    return render_template('user_postlist.html', form=form)

@user_views.route('/user/mypublished/<UID>')
@login_required
def published_info(UID):
    """
    說明：我的刊登資訊呈現
    :param UID:使用者UID
    :return:
    """
    clinic_or_user('user')
    from ..models.user import published
    published = published.query.filter_by(UID=UID).all()
    if published is None:
        abort(404)
    return render_template('user_list.html', published=published)


@user_views.route('/user/mypet/<UID>')
@login_required
def pet_info(UID):
    """
    說明：我的寵物資訊呈現
    :param UID:使用者UID
    :return:
    """
    clinic_or_user('user')
    from ..models.user import pet
    pets = pet.query.filter_by(UID=UID).all()
    if pets is None:
        abort(404)
    return render_template('user_pet.html', pets=pets)

@user_views.route('/user/edit_published/<int:PublishedID>', methods=['GET', 'POST'])
@login_required
def edit_publshed(PublishedID):
    """
    更新publshed
    :param PublishedID:
    :return:
    """
    clinic_or_user('user')
    from ..models import published
    Publishing = published.query.filter_by(PublishedID=PublishedID).first_or_404()
    form = FormPublished()
    if form.validate_on_submit():
        file_name = photos.save(form.picture.data)
        Publishing.PublishedID = PublishedID
        Publishing.title=form.title.data
        Publishing.species=form.species.data
        Publishing.fur=form.fur.data
        Publishing.picture=file_name
        Publishing.area=form.area.data
        Publishing.depiction=form.depiction.data
        Publishing.sex=form.sex.data
        Publishing.variety=form.variety.data
        Publishing.type=int(form.type.data)
        Publishing.UID=current_user.UID
        Publishing.activate=True
        db.session.add(Publishing)
        db.session.commit()
        flash('Edit Your Post Success')
        return redirect(url_for('user_views.published_info', UID=Publishing.UID))
    form.title.data = Publishing.title
    form.species.data = Publishing.species
    form.fur.data = Publishing.fur
    form.picture.data = Publishing.picture
    form.area.data = Publishing.area
    form.depiction.data = Publishing.depiction
    form.sex.data = Publishing.sex
    form.variety.data = Publishing.variety
    # 單選預設是str，但資料庫是int，所以要改型態才會顯示
    form.type.data = str(Publishing.type)
    print(form.picture.data)
    # 利用參數action來做條件，判斷目前是新增還是編輯
    return render_template('user_postlist.html', form=form, Publishing=Publishing, action='edit')

@user_views.route('/miss')
def miss_data():
    """
    說明：所有刊登資訊呈現
    :return:
    """
    from ..models.user import published
    published = published.query.filter(
        published.type.in_([1, 2])
    ).all()
    if published is None:
        abort(404)
    return render_template('miss.html', published=published)

@user_views.route('/adoption')
def adoption_data():
    """
    說明：所有刊登資訊呈現
    :return:
    """
    from ..models.user import published
    published = published.query.filter_by(type=3).all()
    if published is None:
        abort(404)
    return render_template('adoption.html', published=published)


@user_views.route('/user/pet_medicalrecord/<int:PetID>')
@login_required
def mypet_medicalrecord(PetID):
    """
    說明：我寵物病歷
    :return:
    """
    clinic_or_user('user')
    from ..models.user import medicalrecords
    medicalrecords = medicalrecords.query.filter_by(PetID=PetID).all()
    if medicalrecords is None:
        abort(404)
    return render_template('user_detailedrecords.html',medicalrecords=medicalrecords)