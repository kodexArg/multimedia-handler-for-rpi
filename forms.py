import os

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField, IntegerField, SelectMultipleField, SelectField, widgets
from wtforms.validators import DataRequired

from utils import VIDEOS_PATH


# Forms
class CheckboxMultipleField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Converter(FlaskForm):
    file = FileField(
        'Image to convert',
        validators=[DataRequired('Requried')]
    )
    filename = StringField(
        'Video Name (optional)'
    )
    orientation = SelectField(
        'Orientation',
        choices=['1920x1080', '1080x1920', '1280x720', '720x1280'],
        default = 1
    )
    lenght = IntegerField(
        'Time in seconds',
        validators=[DataRequired('Requried')]
    )
    folders = CheckboxMultipleField(
        "Copy to device's folders:",
        choices=os.listdir(VIDEOS_PATH)
    )
    submit = SubmitField(
        'Convert'
    )
