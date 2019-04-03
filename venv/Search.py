from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


# Класс для формы поиска по заголовку
class TitleSearch(FlaskForm):
    title = StringField('Поиск по названию')


# Класс для формы поиска по автору
class AuthorSearch(FlaskForm):
    author = StringField('Поиск по автору')


# Класс для формы кнопки
class SubmitButton(FlaskForm):
    submit = SubmitField('Поиск')


