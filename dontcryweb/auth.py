import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from dontcryweb.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        identity = request.form['identity']
        email = request.form['email']
        phone = request.form['phone']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (u_name, u_password, u_identity, email, phone) VALUES (?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), identity, email, phone),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/register_clinic', methods=('GET', 'POST'))
def register_clinic():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        clinic_name = request.form['clinic_name']
        phone = request.form['phone']
        address = request.form['address']
        city = request.form['city']
        issue_no = request.form['issue_no']
        issue_date = request.form['issue_date']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO clinic (c_account, c_password, c_name, phone, c_address, city, issue_no, issue_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    (username, generate_password_hash(password), clinic_name, phone, address, city, issue_no, issue_date),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {clinic_name} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register_clinic.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        is_clinic = request.form['login_type']
        db = get_db()
        error = None

        if int(is_clinic):
            clinic = db.execute(
                'SELECT * FROM clinic WHERE c_account = ?', (username,)
            ).fetchone()

            if clinic is None:
                error = 'Incorrect username.'
            elif not check_password_hash(clinic['c_password'], password):
                error = 'Incorrect password.'

            if error is None:
                session.clear()
                session['user_id'] = clinic['c_id']
                return redirect(url_for('clinic.index'))

            flash(error)
        
        user = db.execute(
            'SELECT * FROM user WHERE u_name = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['u_id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
"""
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
"""

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view