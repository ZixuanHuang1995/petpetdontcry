from flask import Blueprint, render_template,abort, jsonify, request, send_from_directory, flash, redirect, url_for
import flask
from ..config_other import photos
from APP.models.user import published
from .index import index_views
from flask_login import login_user,current_user,login_required,logout_user
from werkzeug.utils import secure_filename
from ..controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
)
from ..form.userForm import FormRegister,FormLogin,FormUserInfo
from ..form.publishedForm import FormPublished
from ..database import db
user_views = Blueprint('user_views', __name__, template_folder='../templates')

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
@user_views.route('/register',methods=['GET','POST'])
def register():
    """
    說明：註冊使用者
    :return:
    """
    print(db)
    from ..models import user
    form = FormRegister()
    if form.validate_on_submit():
        user = user(
            identity = form.identity.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return 'Success!'
    return render_template('register.html',form = form)

@user_views.route('/login', methods=['GET', 'POST'])
def login(): 
    """
    說明：登入
    :return:
    """
    from ..models import user
    form = FormLogin()
    if form.validate_on_submit():
        users = user.query.filter_by(email=form.email.data).first()
        if users:
            if users.check_password(form.password.data):
                login_user(users,form.remember_me.data)
                next = request.args.get('next')
                if not next_is_valid(next):
                    return 'ERRRRRRRR'
                # return 'Welcome:'+current_user.name
                return redirect(next or url_for('user_views.test_index'))
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
  
@user_views.route('/logout')  
@login_required
def logout():  
    """
    說明：登出
    :return:
    """
    logout_user()
    flash('Logout See You')
    return redirect(url_for('user_views.login'))

@user_views.route('/edituserinfo', methods=['GET', 'POST'])
@login_required
def edituserinfo():
    """
    說明：更新使用者資訊
    :return:
    """
    form = FormUserInfo()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        db.session.add(current_user)
        db.session.commit()
        #  在編輯個人資料完成之後，將使用者引導到使用者資訊觀看結果
        flash('You Have Already Edit Your Info')
        return redirect(url_for('user_views.userinfo', UID=current_user.UID))
    #  預設表單欄位資料為current_user的目前值
    form.UID.data = current_user.UID
    form.identity.data = current_user.identity
    form.email.data = current_user.email
    form.name.data = current_user.name
    form.phone.data = current_user.phone
    return render_template('edituserInfo.html', form=form)

@user_views.route('/userinfo/<UID>')
@login_required
def userinfo(UID):
    """
    說明：使用者資訊呈現
    :param UID:使用者UID
    :return:
    """
    from ..models.user import user
    user = user.query.filter_by(UID=UID).first()
    if user is None:
        abort(404)
    return render_template('userInfo.html', user=user)

@user_views.route('/published', methods=['GET', 'POST'])
@login_required
def add_publshed():
    """
    說明：刊登遺失寵物資訊
    :return:
    """
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
    return render_template('addpublished.html', form=form)

@user_views.route('/mypublished/<UID>')
@login_required
def publishinfo(UID):
    """
    說明：我的刊登資訊呈現
    :param UID:使用者UID
    :return:
    """
    from ..models.user import published
    published = published.query.filter_by(UID=UID).all()
    if published is None:
        abort(404)
    return render_template('published.html', published=published)


@user_views.route('/mypet/<UID>')
@login_required
def petinfo(UID):
    """
    說明：我的寵物資訊呈現
    :param UID:使用者UID
    :return:
    """
    from ..models.user import pet
    pets = pet.query.filter_by(UID=UID).all()
    if pets is None:
        abort(404)
    return render_template('pet.html', pets=pets)

@user_views.route('/published/<int:PublishedID>/', methods=['GET', 'POST'])
@login_required
def update_publshed(PublishedID):
    """
    更新publshed
    :param PublishedID:
    :return:
    """
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
        return redirect(url_for('user_views.publishinfo', UID=Publishing.UID))
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
    # 利用參數action來做條件，判斷目前是新增還是編輯
    return render_template('addpublished.html', form=form, Publishing=Publishing, action='edit')