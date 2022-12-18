from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from dontcryweb.auth import login_required
from dontcryweb.db import get_db

bp = Blueprint('clinic', __name__)

@bp.route('/')
def index():
    db = get_db()
    medical_records = db.execute(
        'SELECT r.id, disease, medicine, created, clinic_id, username'
        ' FROM medical_record r JOIN user u ON r.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('index.html', medical_records=medical_records)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')
