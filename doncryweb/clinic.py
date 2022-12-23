import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from doncryweb.db import get_db

bp = Blueprint('clinic', __name__, url_prefix='/clinic')

@bp.route('/home', methods=('GET', 'POST'))
def home():
    return render_template('clinic_home.html')
