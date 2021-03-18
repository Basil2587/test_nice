import os
import pathlib

from flask import Flask, request, render_template
from flask_dropzone import Dropzone
from PIL import Image


basedir = os.path.abspath(os.path.dirname(__file__))


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

@app.route('/img/')
def image_size():
    path=os.path.join(basedir, 'uploads')
    dir_list = [os.path.join(path, x) for x in os.listdir(path)]
    if dir_list:
        date_list = [[x, os.path.getctime(x)] for x in dir_list]
    # сортируем список по дате создания в обратном порядке
        sort_date_list = sorted(date_list, key=lambda x: x[1], reverse=True)
    try:
        image = Image.open(sort_date_list[0][0])
    except FileNotFoundError:  
        return("Файл не найден")
    path_file=pathlib.Path(sort_date_list[0][0])
    name=path_file.name
    width = image.size[0] # Определяем ширину. 
    height = image.size[1] # Определяем высоту.  
    pix = image.load()
    medium_color = str(pix[4, 4])
    return render_template(
        "size.html", 
        width=width, 
        height=height, 
        medium_color=medium_color, 
        name=name
        )


if __name__ == '__main__':
    app.run(debug=True)
