import os

from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FileField, IntegerField, SelectMultipleField, BooleanField, widgets
from wtforms.validators import DataRequired

from utils import VIDEOS_PATH


# Forms
class CheckboxMultipleField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class Converter(FlaskForm):
    file = FileField(
        'Imagen a convertir',
        validators=[DataRequired('Obligatorio')]
    )
    filename = StringField('Nombre del video (opcional)')
    orientation = BooleanField('Orientado Vertical?')
    lenght = IntegerField(
        'Duración',
        validators=[DataRequired('Obligatorio')]
    )
    folders = CheckboxMultipleField(
        'Copiar a',
        choices=os.listdir(VIDEOS_PATH)
    )
    submit = SubmitField('Convertir')
