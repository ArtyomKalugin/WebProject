from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField
from wtforms.validators import DataRequired


# Статусы пользователя, которые он получит после прохождения викторины
alias = ['Ничего не знающий!', 'Посмотревший одну серию', 'Отдыхающий на Железных Островах', 'Брат Ночного Дозора',
             'Почти гуру', 'Смертоносный']


# Класс для формы викторины(радиобаттоны)
class QuizForm(FlaskForm):
    block_1 = RadioField(u'Одно из имен Дейнерис Таргариен – Мать … ', choices=[
        ('1', u'Ящериц'),
        ('True', u'Драконов'),
        ('3', u'Саламандр')], default=3, validators=[DataRequired()])

    block_2 = RadioField(u'Как зовут актера, который сыграл Тириона Ланнистера?', choices=[
        ('True', u'Питер Динклэйдж'),
        ('2', u'Джейсон Момоа'),
        ('3', u'Иэн Глен')], default=3, validators=[DataRequired()])

    block_3 = RadioField(u'Кто является настоящим отцом Джоффри Баратеона?', choices=[
        ('1', u'Роберт Баратеон'),
        ('2', u'Джон Аррен'),
        ('True', u'Джейме Ланнистер')], default='True', validators=[DataRequired()])

    block_4 = RadioField(u'Кто несет свою службу на Стене?', choices=[
        ('1', u'Ночная Стража'),
        ('True', u'Ночной Дозор'),
        ('3', u'Ночное Братство')], default=3, validators=[DataRequired()])

    block_5 = RadioField(u'Что подарил Джон Сноу своей сестре Арье перед отъездом из Винтерфела?', choices=[
        ('True', u'Клинок'),
        ('2', u'Брошь'),
        ('3', u'Перстень')], default=3, validators=[DataRequired()])

    block_6 = RadioField(u'Чего больше всего на свете боится Сандор Клиган по прозвищу Пёс?', choices=[
        ('True', u'Огня'),
        ('2', u'Воды'),
        ('3', u'Крови')], default=3, validators=[DataRequired()])

    submit = SubmitField('Показать и сохранить результат')
