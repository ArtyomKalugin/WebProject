from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField


class LoadPhotoForm(FlaskForm):
    file = FileField('Загрузите фотографию')
    submit = SubmitField('Применить')