from crypt import methods
from logging import root
import os

from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from werkzeug.utils import secure_filename


from folders import VIDEOS_PATH as root_videos_dir


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Super Secure Password (not really...)'


# Forms
class Converter(FlaskForm):
    file = FileField()


# Routes
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


@app.route('/converter', methods=['GET', 'POST'])
def converter():
    """ converts a JPG into a MP4 movie that last a setted time """
    form = Converter()

    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('converter/' + filename)
        return redirect(url_for('home'))

    return render_template('converter.html', form=form)


@app.route('/vid')
def videos():
    content = {
        "all_devices": video_list_as_json()
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


if __name__ == "__main__":
    app.debug = True
    app.run()
