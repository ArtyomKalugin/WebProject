from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired


class AddTheoryForm(FlaskForm):
    title = StringField('Заголовок теории', validators=[DataRequired()])
    content = TextAreaField('Текст теории', validators=[DataRequired()])
    file = FileField('Прикрепите фотографию')
    submit = SubmitField('Добавить')