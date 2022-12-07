from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
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

@user_views.route('/register',methods=['GET','POST'])
def register():
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

@user_views.route('/test')  
@login_required 
def test_index():  
    flash('flash-1')  
    # flash('flash-2')  
    # flash('flash-3')  
    return render_template('base.html')  
  
  
@user_views.route('/login', methods=['GET', 'POST'])
def login():  
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
    logout_user()
    flash('Logout See You')
    return redirect(url_for('user_views.login'))

@user_views.route('/edituserinfo', methods=['GET', 'POST'])
@login_required
def edituserinfo():
    form = FormUserInfo()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.phone = form.phone.data
        db.session.add(current_user)
        db.session.commit()
        #  在編輯個人資料完成之後，將使用者引導到使用者資訊觀看結果
        flash('You Have Already Edit Your Info')
        return redirect(url_for('user_views.userinfo', name=current_user.name))
    #  預設表單欄位資料為current_user的目前值
    form.UID.data = current_user.UID
    form.identity.data = current_user.identity
    form.email.data = current_user.email
    form.name.data = current_user.name
    form.phone.data = current_user.phone
    return render_template('userInfo.html', form=form)
#  先加入一個route來做引導，確認是否正常
@user_views.route('/userinfo/<name>')
@login_required
def userinfo(name):
    return 'Hello %s' % current_user.name

@user_views.route('/published', methods=['GET', 'POST'])
@login_required
def add_publshed_missing():
    from ..models import published
    form = FormPublished()
    if form.validate_on_submit():
        print(form.picture.data)
        file_name = photos.save(form.picture.data)
        print(file_name)
        Publishing = published(
            title=form.title.data,
            species=form.species.data,
            fur=form.fur.data,
            picture=file_name,
            area=form.area.data,
            depiction=form.depiction.data,
            sex=form.sex.data,
            variety=form.variety.data,
            type=1,
            UID=current_user.UID,
            activate=True
        )
        db.session.add(Publishing)
        db.session.commit()
        flash('Create New Blog Success')
        return f'Picurl:{file_name}s'
    return render_template('addpublished.html', form=form)

