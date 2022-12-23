import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from doncryweb.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/user_register', methods=('GET', 'POST'))
def user_register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        identity = request.form['identity']
        phone = request.form['phone']
        role = 'user'
        first = True
        ID = 0
        db = get_db()
        error = None

        if not email:
            error = 'email is required.'
        elif not password:
            error = 'Password is required.'
        elif not name:
            error = 'name is required.'
        elif not identity:
            error = 'identity is required.'
        elif not phone:
            error = 'phone is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO account (email, password, role, first) VALUES (?, ?, ?, ?)",
                    (email, generate_password_hash(password), role, first),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            try:
                print(email)
                account = db.execute(
                    "SELECT ID FROM account WHERE email = ?",
                    (email,)
                ).fetchone()
                ID = account['ID']
                db.execute(
                    "INSERT INTO user (name, identity, phone, ID) VALUES (?, ?, ?, ?)",
                    (name, identity, phone, ID),
                )
                db.commit()
                flash("會員註冊成功")
            except db.IntegrityError:
                error = f"ID {ID} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('user_register.html')

@bp.route('/clinic_register', methods=('GET', 'POST'))
def clinic_register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        phone = request.form['phone']
        address = request.form['address']
        emergency = request.form['emergency']
        role = 'clinic'
        first = True
        ID = 0
        db = get_db()
        error = None

        if not email:
            error = 'email is required.'
        elif not password:
            error = 'Password is required.'
        elif not name:
            error = 'name is required.'
        elif not phone:
            error = 'phone is required.'
        elif not address:
            error = 'address is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO account (email, password, role, first) VALUES (?, ?, ?, ?)",
                    (email, generate_password_hash(password), role, first),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {email} is already registered."
            try:
                account = db.execute(
                    "SELECT ID FROM account WHERE email = ?",
                    (email,)
                ).fetchone()
                db.commit()
                db.execute(
                    "INSERT INTO clinic (name, phone, address, emergency, ID) VALUES (?, ?, ?, ?, ?)",
                    (name, phone, address, emergency, account['ID']),
                )
                flash("診所註冊成功")
                db.commit()
            except db.IntegrityError:
                error = f"ID {account['ID']} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('clinic_register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        account = db.execute(
            'SELECT * FROM account WHERE email = ?', (email,)
        ).fetchone()

        if account is None:
            error = 'Incorrect email.'
        elif not check_password_hash(account['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['account_ID'] = account['ID']
            if account['role'] == 'user':
                return redirect(url_for('home'))
            elif account['role'] == 'clinic':
                return redirect(url_for('clinic.home'))

        flash(error)

    return render_template('login.html')

@bp.route('/logout')
def logout():
    session.clear()
    print("bye")
    return redirect(url_for('home'))

@bp.before_app_request
def load_logged_in_user():
    account_ID = session.get('account_ID')

    if account_ID is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM account WHERE id = ?', (account_ID,)
        ).fetchone()

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view