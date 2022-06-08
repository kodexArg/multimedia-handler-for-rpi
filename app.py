from logging import root
import os

from flask import Flask, render_template

from folders import VIDEOS_PATH as root_videos_dir


app = Flask(__name__)


# Routes
@app.route('/')
def home():
    return render_template('home.html')


@app.route('/vid')
def videos():
    return render_template('videos.html', all_content=video_list_as_json())


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
        for video in os.listdir(video_path):    
            position += 1
            rpi_vid = {}
            rpi_vid['tag'] = video.split(sep='.')[0]
            rpi_vid['src'] = "/".join(['videos', folder, video])
            rpi_id[position] = rpi_vid
        rpi[folder] = rpi_id
    return rpi


if __name__ == "__main__":
    app.debug = True
    app.run()
