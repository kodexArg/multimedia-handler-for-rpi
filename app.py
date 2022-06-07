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
    return render_template('videos.html', vids=video_list_as_json())


# Functions
def video_list_as_json():
    all_videos = []
    for folder in os.listdir(root_videos_dir):
        # each folder should indetify a Raspberry Pi
        video_path = os.path.join(root_videos_dir, folder)
        rpi_vids = {}
        for video in os.listdir(video_path):
            rpi_vids['device'] = folder
            rpi_vids['tag'] = video.split(sep='.')[0]
            rpi_vids['src'] = "/".join(['videos', folder, video])
            all_videos.append(rpi_vids)
    return all_videos


if __name__ == "__main__":
    app.debug = True
    app.run()
