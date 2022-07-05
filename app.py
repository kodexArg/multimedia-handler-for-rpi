import os
import shutil

from flask import Flask, request, redirect, render_template, flash, url_for
from werkzeug.utils import secure_filename

from forms import Converter
from utils import ffmpeg, myprint, VIDEOS_PATH, CONVERTER_PATH

app = Flask(__name__)


# Routes
@app.route('/')
def home():
    """
        A simple, text only presentation of this application.
    """
    return render_template('home.html')


@app.route('/converter', methods=['GET', 'POST'])
def converter():
    """
        Convert a JPG into an MP4 movie that last x seconds
    """
    form = Converter()
    folders = os.listdir(VIDEOS_PATH)
    content = {
        'form': form,
        'folders': folders,
    }
    if form.validate_on_submit():
        # get input_filename and the picture in /static/converter
        input_filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(CONVERTER_PATH, input_filename))

        # fix and get output_filename
        output_filename = form.filename.data
        if output_filename == '':
            output_filename = input_filename.replace('.', '_')
        if len(output_filename.split('.')) == 1:
            output_filename += ".mp4"
        output_filename = output_filename.replace(' ', '_').replace('-', '_')

        # time in seconds for the video file
        seconds_lenght = form.lenght.data

        # orientation as string (default is '1920x1080')
        orientation = form.orientation.data

        # selected folders (checkboxes in the form)
        folders = form.folders.data

        # continue running ffmpeg
        ffmpeg_convertion(input_filename, output_filename,
                          seconds_lenght, orientation, folders)
        myprint('Proceso finalizado sin errores', alert_type='alert-info')

        return redirect(url_for('converter'))

    return render_template('converter.html', **content)


@app.route('/vid', methods=['GET', 'POST'])
def videos():
    """
        Display a list-view like table with all videos grouped by folder.
        Enable a serie of actions for each video, like:
        - Copy: to later paste the video in any device
        - Delete and Delete all: To remove the video in the selected device or
          delete it from every device in the list.
    """
    src, action = None, None
    if request.method == 'POST':
        action = request.form['action']
        src = request.form['src']

        myprint(f"Runing {action} on {src}", alert_type='alert-info')

    content = {
        'all_devices': video_list_as_json(),
        'MacroCopySrc': src
    }
    return render_template('videos.html', **content)


# Functions
def ffmpeg_convertion(input_filename, output_filename, lenght_in_seconds, orientation, folders):
    """
        Run ffmpeg for a given image and paste the resulting video on every folder.
    """

    myprint(input_filename, output_filename)
    input_file = os.path.join(CONVERTER_PATH, input_filename)
    output_file = os.path.join(CONVERTER_PATH, output_filename)

    # create video file, this subprocess takes a while depending on image size and time lenght
    ffmpeg(input_file, output_file, lenght_in_seconds, orientation)

    # copying video to device's folders selected in the form
    for folder in folders:
        myprint(f"Coping video to {folder}...")
        shutil.copy(output_file, os.path.join(VIDEOS_PATH, folder))

    # finally, moving the source image and video to 'processed' folder as recycle bin.
    shutil.copy2(input_file, CONVERTER_PATH / 'processed')
    shutil.copy2(output_file, CONVERTER_PATH / 'processed')
    os.remove(input_file)
    os.remove(output_file)


def video_list_as_json():
    """
    Constructs a nested dict for each device (folder) and their videos with the following structure:

    [RPI_201:{
        1:{src:source path,tag:filename},
        2:{src:source path,tag:filename}
    },
    RPI_202:{
        1:{...}}]

    """
    rpi = {}
    for folder in os.listdir(VIDEOS_PATH):
        video_path = os.path.join(VIDEOS_PATH, folder)
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
