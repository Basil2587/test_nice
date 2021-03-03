import os

from flask import Flask, request, render_template
from flask_dropzone import Dropzone

basedir = os.path.abspath(os.path.dirname(__file__))

#UPLOAD_FOLDER = 'static'
#ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config.update(
    UPLOADED_PATH = os.path.join(basedir,'uploads'),
    DROPZONE_MAX_FILE_SIZE = 5024,
    DROPZONE_TIMEOUT = 5*60*1000)

dropzone=Dropzone(app)
@app.route('/', methods=['POST','GET'])
def upload_file():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
