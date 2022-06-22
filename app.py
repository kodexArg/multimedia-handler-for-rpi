import os
import shutil

from flask import Flask, redirect, render_template, flash, url_for
from werkzeug.utils import secure_filename

from forms import Converter
from utils import ffmpeg, VIDEOS_PATH, CONVERTER_PATH

app = Flask(__name__)


# Routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/converter', methods=['GET', 'POST'])
def converter():
    """ converts a JPG into a MP4 movie that last x seconds """
    form = Converter()
    folders = os.listdir(VIDEOS_PATH)
    content = {
        'form': form,
        'folders': folders,
    }

    if form.validate_on_submit():
        # input filename and save:
        input_filename = secure_filename(form.file.data.filename)
        form.file.data.save(os.path.join(CONVERTER_PATH, input_filename))

        # output file naming:
        output_filename = form.filename.data
        if output_filename == '':
            output_filename = input_filename.replace('.', '_')
        if len(output_filename.split('.')) == 1:
            output_filename += ".mp4"
        output_filename = output_filename.replace(' ', '_').replace('-', '_')

        lenght = form.lenght.data
        folders = form.folders.data

        ffmpeg_convertion(input_filename, output_filename, lenght, folders)
        flash('Proceso finalizado sin errores', 'alert-info')

        return redirect(url_for('converter'))
    return render_template('converter.html', **content)


@app.route('/vid')
def videos():
    content = {
        'all_devices': video_list_as_json()
    }
    return render_template('videos.html', **content)


# Functions
def ffmpeg_convertion(input_filename, output_filename, lenght_in_seconds, folders):

    input_file = os.path.join(CONVERTER_PATH, input_filename)
    output_file = os.path.join(CONVERTER_PATH, output_filename)

    # create video file, this subprocess takes a while depending on image size and time lenght
    ffmpeg(input_file, output_file, lenght_in_seconds)

    # copying video to device folders selected in form
    for folder in folders:
        print(f"Coping video to {folder}...")
        shutil.copy(output_file, os.path.join(VIDEOS_PATH, folder))

    # finally moving image and video to 'processed' folder.
    print(
        f"Moving {input_filename} and {output_filename} to {CONVERTER_PATH}/processed")
    shutil.copy2(input_file, CONVERTER_PATH / 'processed')
    shutil.copy2(output_file, CONVERTER_PATH / 'processed')
    os.remove(input_file)
    os.remove(output_file)
    

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
