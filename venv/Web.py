from flask import Flask, url_for, request, render_template, make_response, jsonify, session, redirect
from Classes import DB, TheoryModel, UserModel
from LoginForm import LoginForm, SignInForm
import string
from werkzeug.security import generate_password_hash, check_password_hash, gen_salt
import random
from Search import TitleSearch, AuthorSearch, SubmitButton
import datetime
from AddTheory import AddTheoryForm
import shutil
import imghdr
import os
from Victorine import QuizForm, alias
from LoadPhoto import LoadPhotoForm


# Глобальные переменные, ключ
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()


# Функция создания пароля, хэширование и соление
def password_salt(password):
    hash = generate_password_hash(password)
    salt = gen_salt(random.choice(range(1, 10)))
    hash += salt

    return (hash, salt)


# Функция для фотографий, если существуют - удаляем, иначе перемащем в папку
def move_photo(way, name):
    if os.path.exists(way):
        os.remove(way)

    shutil.move(name, 'static/img')


# Страница, на которой отображается информация о среиале
@app.route('/main')
def main_page():
    return render_template('main_page.html')


# Регистрация
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    err = None
    if form.validate_on_submit():
        name = request.form['username']
        pso = request.form['password_one']
        pst = request.form['password_two']
        data = datetime.date.today()

        check = [False, False]

        # Проверка логина и пароля
        if UserModel(db.get_connection()).exists(name)[0]:
            err = 'Такой логин уже существует'
            return render_template('login.html', title='Регистрация', form=form, err=err)

        if len(name) > 5:
            for letter in name:
                if letter.isalpha():
                    check[0] = True
                    if letter not in string.ascii_letters:
                        err = 'Логин должен содержать латинские буквы и цифры'
                        return render_template('login.html', title='Регистрация', form=form, err=err)
                if letter.isdigit():
                    check[1] = True
        else:
            err = 'Логин должен быть длиннее 5 символов'
            return render_template('login.html', title='Регистрация', form=form, err=err)

        if check[0] is False or check[1] is False:
            err = 'Логин должен содержать латинские буквы и цифры'
            return render_template('login.html', title='Регистрация', form=form, err=err)

        if pso != pst:
            err = 'Пароли не одинаковы'
            return render_template('login.html', title='Регистрация', form=form, err=err)
        else:
            if len(pso) > 5:
                # Создание пользователя
                user = UserModel(db.get_connection())

                hash, salt = password_salt(pso)

                user.insert(name, hash, salt, data, 'Cреднестатистический обыватель', 'default.png')

                session['username'] = name
                session['photo'] = 'default.png'

                if user.exists(name)[0]:
                    session['id'] = user.exists(name)[1]

                return redirect('/success_login')
            else:
                err = 'Пароль должен быть длиннее 5 символов'
                return render_template('login.html', title='Регистрация', form=form, err=err)

    return render_template('login.html', title='Регистрация', form=form, err=err)


# Выход из системы
@app.route('/logout')
def logout():
    if 'username' not in session:
        return redirect('/sign_in')

    # Достаточно забыть пользователя в системе
    session.pop('username', 0)
    session.pop('photo', 0)
    session.pop('id', 0)
    return redirect('/sign_in')


# Вход в систему
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    err = None
    if form.validate_on_submit():
        name = request.form['username']
        password = request.form['password']

        user = UserModel(db.get_connection())
        exists = user.exists(name)
        if (exists[0]):
            password_model = user.get(exists[1])[2]
            salt = len(user.get(exists[1])[3])

            # Проверка валидности введеных данных
            if check_password_hash(password_model[:len(password_model) - salt], password):
                photo = user.get(exists[1])[6]
                session['username'] = name
                session['photo'] = photo
                session['id'] = exists[1]

                return redirect('/main')
            else:
                err = 'Ошибка в логине или пароле'
                return render_template('sign_in.html', title='Авторизация', form=form, err=err)
        else:
            err = 'Пользователь не существует'
            return render_template('sign_in.html', title='Авторизация', form=form, err=err)

    return render_template('sign_in.html', title='Авторизация', form=form, err=err)


# При успешной регистрации
@app.route('/success_login')
def success_login():
    return render_template('success_login.html')


# Страница со всеми теориями
@app.route('/theories', methods=['GET', 'POST'])
def theories():
    aut = AuthorSearch()
    tit = TitleSearch()
    form = SubmitButton()

    theor = TheoryModel(db.get_connection())
    all_teories = theor.get_all()
    all_teories = all_teories[::-1]
    result = []
    note = 'Все теории:'

    # Если теория больше 100 символов, то она печатается в сокращенном виде
    for i in range(len(all_teories)):
        if len(all_teories[i][2]) > 100:
            all_teories[i] = (all_teories[i][0], all_teories[i][1], all_teories[i][2][:100] + '...',
                              all_teories[i][3], all_teories[i][4])

    if form.validate_on_submit():
        author = request.form['author']
        title = request.form['title']

        if author and not title:
            note = 'По вашему запросу нашлось:'
            for elem in all_teories:
                if author.lower() in elem[3].lower():
                    result.append(elem)

        if not author and title:
            note = 'По вашему запросу нашлось:'
            for elem in all_teories:
                if title.lower() in elem[1].lower():
                    result.append(elem)

        if author and title:
            note = 'По вашему запросу нашлось:'
            for elem in all_teories:
                if title.lower() in elem[1].lower() and author.lower() in elem[3].lower():
                    result.append(elem)

        if len(result) == 0:
            note = 'По вашему запросу ничего не нашлось!'

        return render_template('theories.html', aut=aut, tit=tit, form=form, t=result, n=note)
    else:
        return render_template('theories.html', aut=aut, tit=tit, form=form, t=all_teories, n=note)


# Личный кабинет
@app.route('/cabinet', methods=['GET', 'POST'])
def cabinet():
    if 'username' not in session:
        return redirect('/sign_in')

    um = UserModel(db.get_connection())
    all = []
    err = None

    if um.exists(session['username'])[0]:
        all = um.get(um.exists(session['username'])[1])

    tm = TheoryModel(db.get_connection())
    content = 'Всего теорий: ' + str(len(tm.get_all(user_id=all[0])))

    form = LoadPhotoForm()

    # Загрузка фотографии
    if form.validate_on_submit():
        f = form.file.data

        if f:
            name = f.filename
            session['photo'] = name
            result = open(name, 'wb')
            result.write(f.read())
            result.close()

            way = 'static/img/' + name

            # Если фотография уже существует в нашей папке, то удаляем ее
            move_photo(way, name)

            # Проверка того, является ли файл фотографией
            if not imghdr.what(way):
                err = 'Файл недопустимого формата'
                os.remove(way)
                return render_template('cabinet.html', n=session['username'], i=all[0], d=all[4], l=content, s=all[5],
                                       p=all[6], err=err)
            else:
                um = UserModel(db.get_connection())
                if um.exists(session['username'])[0]:
                    id = um.exists(session['username'])[1]
                um.change_photo(name, id)

        return redirect('/cabinet')

    else:
        return render_template('cabinet.html', n=session['username'], i=all[0], d=all[4], l=content, s=all[5], p=all[6], err=err, form=form)


# Добавление теории
@app.route('/add_theory', methods=['GET', 'POST'])
def add_theory():
    if 'username' not in session:
        return redirect('/sign_in')

    form = AddTheoryForm()
    data = datetime.date.today()
    err = None

    if form.validate_on_submit():
        title = request.form['title']
        text = request.form['content']
        f = form.file.data

        # Провека валидности
        if len(title) < 10:
            err = 'Длина заголовка должна быть больше 10 символов'
            return render_template('add_theory.html', form=form, err=err)

        if len(text) < 20:
            err = 'Длина текста должна быть больше 20 символов'
            return render_template('add_theory.html', form=form, err=err)

        if len(text) > 10000:
            err = 'Длина текста должна быть меньше 1000 символов'
            return render_template('add_theory.html', form=form, err=err)

        if f:
            # То же самое, что и с личным кабинетом, если фотка есть - удаляем
            name = f.filename
            result = open(name, 'wb')
            result.write(f.read())
            result.close()

            way = 'static/img/' + name

            move_photo(way, name)

            if not imghdr.what(way):
                err = 'Файл недопустимого формата'
                os.remove(way)
                return render_template('add_theory.html', form=form, err=err)
        else:
            name = None

        theor = TheoryModel(db.get_connection())
        if UserModel(db.get_connection()).exists(session['username'])[0]:
            id = UserModel(db.get_connection()).exists(session['username'])[1]
        theor.insert(title, text, session['username'], data, name, id)

        return redirect('/theories')

    else:
        return render_template('add_theory.html', form=form, err=err)


# Отдельная страница для чтения теории
@app.route('/read_theory/<int:theory_id>', methods=['GET'])
def read_theory(theory_id):
    theor = TheoryModel(db.get_connection()).get(theory_id)
    id = theor[6]

    if UserModel(db.get_connection()).exists(theor[3])[0]:
        photo = UserModel(db.get_connection()).get(id)[6]
    else:
        photo = 'delete_user.png'
    return render_template('read_theory.html', t=theor, p=photo, u=None)


# Удаление аккаунта
@app.route('/delete')
def delete():
    if 'username' not in session:
        return redirect('/sign_in')

    um = UserModel(db.get_connection())
    if um.exists(session['username'])[0]:
        photo = um.get(um.exists(session['username'])[1])[6]
        um.delete(um.exists(session['username'])[1])

    way = 'static/img/' + photo
    os.remove(way)

    session.pop('username', 0)
    session.pop('photo', 0)
    session.pop('id', 0)

    return redirect('/login')


# Страница с собственными теориями
@app.route('/read_my_theories', methods=['GET', 'POST'])
def read_my_theories():
    if 'username' not in session:
        return redirect('/sign_in')

    theor = TheoryModel(db.get_connection())
    tit = TitleSearch()
    form = SubmitButton()
    result = []

    err = 'Все ваши теории'
    if UserModel(db.get_connection()).exists(session['username'])[0]:
        id = UserModel(db.get_connection()).exists(session['username'])[1]

    all_teories = theor.get_all(user_id=id)
    all_teories = all_teories[::-1]

    for i in range(len(all_teories)):
        if len(all_teories[i][2]) > 100:
            all_teories[i] = (all_teories[i][0], all_teories[i][1], all_teories[i][2][:100] + '...',
                              all_teories[i][3], all_teories[i][4])

    if len(all_teories) == 0:
        err = 'Вы еще не добавили ни одной теории!'
        return render_template('read_my_theories.html', tit=tit, form=form, t=result, n=err)

    if form.validate_on_submit():
        # Поиск по автору и по содержанию
        title = request.form['title']

        if title:
            err = 'По вашему запросу нашлось:'
            for elem in all_teories:
                if title.lower() in elem[1].lower():
                    result.append(elem)

        if len(result) == 0:
            err = 'По вашему запросу ничего не нашлось!'

        return render_template('read_my_theories.html', tit=tit, form=form, t=result, n=err)

    else:
        return render_template('read_my_theories.html', n=err, t=all_teories, tit=tit, form=form)


# Удаление какой-то теории
@app.route('/delete_theory/<int:theory_id>', methods=['GET'])
def delete_theory(theory_id):
    TheoryModel(db.get_connection()).delete(theory_id)

    return redirect('/read_my_theories')


# Чтение собственной теории
@app.route('/read_theory_my/<int:theory_id>', methods=['GET'])
def read_theory_my(theory_id):
    theor = TheoryModel(db.get_connection()).get(theory_id)
    return render_template('read_theory.html', t=theor, u='1')


# Кабинет другого пользователя, отображается не вся информация
@app.route('/cabinet_other/<int:user_id>', methods=['GET'])
def cabinet_other(user_id):
    if 'username' not in session:
        return redirect('/sign_in')

    if user_id == session['id']:
        return redirect('/cabinet')

    um = UserModel(db.get_connection())
    all = um.get(user_id)

    if all:
        tm = TheoryModel(db.get_connection())
        content = 'Всего теорий: ' + str(len(tm.get_all(user_id=all[0])))

        return render_template('cabinet_other.html', n=all[1], i=all[0], d=all[4], l=content, q=None, s=all[5], p=all[6])
    else:
        return render_template('cabinet_other.html', q='1')


# Викторина
@app.route('/victorine', methods=['GET', 'POST'])
def victorine():

    if 'username' not in session:
        return redirect('/sign_in')

    form = QuizForm()

    if form.validate_on_submit():
        result = []
        true_answers = 0
        status = (None, None)

        for i in range(6):
            block = 'block_' + str(i + 1)
            result.append(request.form.get(block))

        for elem in result:
            if elem == 'True':
                true_answers += 1

        if true_answers == 0:
            status = (str(true_answers), 'Среднестатистический обыватель!')
        else:
            status = (str(true_answers), alias[true_answers - 1])

        um = UserModel(db.get_connection())
        if um.exists(session['username'])[0]:
            um.change_status(status[1], um.exists(session['username'])[1])

        return render_template('result_quiz.html', r=status)
    else:
        return render_template('victorine.html', form=form)


# Страница с информацией о сайте
@app.route('/got')
def got():
    return render_template('got.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
