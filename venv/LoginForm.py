from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


# Класс для формы авторизации
class SignInForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Войти')

# Класс для формы регистрации
class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password_one = PasswordField('Пароль', validators=[DataRequired()])
    password_two = PasswordField('Повторите пароль', validators=[DataRequired()])
    submit = SubmitField('Зарегистрироваться')
