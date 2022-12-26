from flask import Blueprint, flash, request, redirect, render_template, url_for
import os
from werkzeug.utils import secure_filename
import logging


upload_image_views = Blueprint('upload_image_views', __name__, template_folder='../templates')

UPLOAD_FOLDER = 'APP/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_image():

    print("into upload")

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        logging.warning('Image already saved')
        logging.warning('filename: ' + filename)
        print('upload_image filename: ' + filename)
        flash('Image successfully uploaded and displayed below')
        image_path = os.path.join("static/uploads/", filename)
        logging.warning('image_path: ' + image_path)
        # return render_template('upload_image.html', image_path=image_path)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)
