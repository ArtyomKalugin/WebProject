from flask_wtf import FlaskForm
from wtforms import SubmitField, FileField


# Класс формы для загрузки фото
class LoadPhotoForm(FlaskForm):
    file = FileField('Загрузите фотографию')
    submit = SubmitField('Применить')