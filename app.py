import os

import cv2 as cv
from flask import Flask, render_template
app = Flask(__name__)

from folders import VIDEOS_PATH as videos_dir 


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/vid')
def videos():
    return render_template('videos.html')


if __name__ == "__main__":
    app.debug = True
    app.run()
