from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class TitleSearch(FlaskForm):
    title = StringField('Поиск по названию')


class AuthorSearch(FlaskForm):
    author = StringField('Поиск по автору')


class SubmitButton(FlaskForm):
    submit = SubmitField('Поиск')


