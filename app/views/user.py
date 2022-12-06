from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from.index import index_views
from flask_login import login_user,current_user,login_required,logout_user
from ..controllers import (
    create_user, 
    get_all_users,
    get_all_users_json,
)
from ..form.signupForm import FormRegister,FormLogin
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
    test = db.session.execute(db.select(user)).scalars()
    print(test)
    if form.validate_on_submit():
        user = user(
            identity = form.identity.data,
            email = form.email.data,
            password = form.password.data
        )
        db.session.add(user)
        db.session.commit()
        return 'Success!'
    return render_template('test.html',form = form)

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