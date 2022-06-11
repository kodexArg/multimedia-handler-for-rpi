import imp
import os

from flask import Flask, render_template, redirect, url_for, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField, IntegerField, SelectMultipleField, widgets
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

from folders import VIDEOS_PATH as root_videos_dir

app = Flask(__name__)


# Forms
class CheckboxMultipleField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Converter(FlaskForm):
    file = FileField(
        'Elija la imagen JPG para convertir',
        validators=[DataRequired('Obligatorio')]
    )
    lenght = IntegerField(
        'Indique la duración en segundos',
        validators=[DataRequired('Obligatorio')]
    )
    folders = CheckboxMultipleField(
        'Copiar a los siguientes dispositivos (selecciones individuales con tecla Ctrl)',
        choices=os.listdir(root_videos_dir)
    )
    submit = SubmitField('Subir y procesar')


# Routes
@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


@app.route('/converter', methods=['GET', 'POST'])
def converter():
    """ converts a JPG into a MP4 movie that last a setted time """
    form = Converter()
    folders = os.listdir(root_videos_dir)

    content = {
        'form': form,
        'folders': folders,
    }

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('static/converter/' + filename)
        content['response'] = request

    return render_template('converter.html', **content)


@app.route('/vid')
def videos():
    content = {
        'all_devices': video_list_as_json()
    }
    return render_template('videos.html', **content)


# Functions
def video_list_as_json():
    """
    Construct a nested dict for each device (raspberry pi) and their videos with the following structure:

    [RPI_201:{
        1:{src:source path,tag:filename},
        2:{src:source path,tag:filename}
    },
    RPI_202:{
        1:{...}}]
    """

    rpi = {}
    for folder in os.listdir(root_videos_dir):
        video_path = os.path.join(root_videos_dir, folder)
        position = 0
        rpi_id = {}
        if os.path.isdir(video_path):
            for video in os.listdir(video_path):
                position += 1
                rpi_vid = {}
                rpi_vid['tag'] = video.split(
                    sep='.')[0].replace('_', ' ').lower()
                rpi_vid['src'] = "/".join(['videos', folder, video])
                rpi_id[position] = rpi_vid
            rpi[folder] = rpi_id
    return rpi


if __name__ == '__main__':
    app.debug = True
    app.config['SECRET_KEY'] = 'Super Secure Password (not really...)'
    app.run()
