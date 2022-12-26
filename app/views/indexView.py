from flask import Blueprint, redirect, render_template, request, send_from_directory,flash,url_for
from ..form.loginForm import FormLogin
from flask_login import login_user,current_user,login_required,logout_user

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')
    
@index_views.route('/login', methods=['GET', 'POST'])
def login(): 
    """
    說明：登入
    :return:
    """
    from ..models import account
    form = FormLogin()
    if form.validate_on_submit():
        accounts = account.query.filter_by(email=form.account.data).first()
        if accounts:
            if accounts.check_password(form.password.data):
                login_user(accounts,form.remember_me.data)
                next = request.args.get('next')
                print(accounts.ID)
                if not next_is_valid(next):
                    return 'ERRRRRRRR'
                if accounts.first == False:
                    return redirect(next or url_for('user_views.add_userinfo',ID = accounts.ID))
                elif accounts.role == 'clinic':
                    return redirect(next or url_for('clinic_views.home'))
                elif accounts.role == 'user':
                    return redirect(next or url_for('user_views.home'))
            else:
                flash('錯誤的 Email 或 Password')
        else:
                flash('錯誤的 Email 或 Password')
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
  
@index_views.route('/logout')  
@login_required
def logout():  
    """
    說明：登出
    :return:
    """
    logout_user()
    flash('登出成功')
    return redirect(url_for('index_views.login'))