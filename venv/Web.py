from flask import Flask, url_for, request, render_template, make_response, jsonify, session, redirect
from Classes import DB, TheoryModel, UserModel
from LoginForm import LoginForm, SignInForm
import string
from werkzeug.security import generate_password_hash, check_password_hash, gen_salt
import random
from Search import ContentSearch, AuthorSearch, SubmitButton
import datetime
from AddTheory import AddTheoryForm
import shutil
import imghdr
import os


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()

'''''''''
M = UserModel(db.get_connection())
M.init_table()

n = TheoryModel(db.get_connection())
n.init_table()
'''



@app.route('/main')
def main_page():
    return render_template('main_page.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    err = None
    if form.validate_on_submit():
        name = request.form['username']
        pso = request.form['password_one']
        pst = request.form['password_two']

        check = [False, False]

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
                user = UserModel(db.get_connection())
                hash = generate_password_hash(pso)
                salt = gen_salt(random.choice(range(10)))
                hash += salt

                user.insert(name, hash, salt)
                session['username'] = name
                return redirect('/success_login')
            else:
                err = 'Пароль должен быть длиннее 5 символов'
                return render_template('login.html', title='Регистрация', form=form, err=err)

    return render_template('login.html', title='Регистрация', form=form, err=err)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    return redirect('/sign_in')


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

            if check_password_hash(password_model[:len(password_model) - salt], password):
                session['username'] = name
                return redirect('/main')
            else:
                err = 'Ошибка в логине или пароле'
                return render_template('sign_in.html', title='Авторизация', form=form, err=err)
        else:
            err = 'Пользователь не существует'
            return render_template('sign_in.html', title='Авторизация', form=form, err=err)

    return render_template('sign_in.html', title='Авторизация', form=form, err=err)


@app.route('/success_login')
def success_login():
    return render_template('success_login.html')


@app.route('/theories', methods=['GET', 'POST'])
def theories():
    aut = AuthorSearch()
    cont = ContentSearch()
    form = SubmitButton()

    theor = TheoryModel(db.get_connection())
    all_teories = theor.get_all()
    all_teories = all_teories[::-1]

    for i in range(len(all_teories)):
        if len(all_teories[i][2]) > 100:
            all_teories[i] = (all_teories[i][0], all_teories[i][1], all_teories[i][2][:100] + '...',
                              all_teories[i][3], all_teories[i][4])

    if form.validate_on_submit():
        pass
    else:
        return render_template('theories.html', aut=aut, cont=cont, form=form, t=all_teories)


@app.route('/cabinet')
def cabinet():
    return 'PASS'


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

        if len(title) < 10:
            err = 'Длина заголовка должна быть больше 10 символов'
            return render_template('add_theory.html', form=form, err=err)

        if len(text) < 20:
            err = 'Длина текста должна быть больше 20 символов'
            return render_template('add_theory.html', form=form, err=err)

        if len(text) > 1000:
            err = 'Длина текста должна быть меньше 1000 символов'
            return render_template('add_theory.html', form=form, err=err)

        if f:
            name = f.filename
            result = open(name, 'wb')
            result.write(f.read())
            result.close()

            way = 'static/img/' + name

            if os.path.exists(way):
                os.remove(way)

            shutil.move(name, 'static/img')

            if not imghdr.what(way):
                err = 'Файл недопустимого формата'
                return render_template('add_theory.html', form=form, err=err)
        else:
            name = None

        theor = TheoryModel(db.get_connection())
        theor.insert(title, text, session['username'], data, name)

        return redirect('/theories')

    else:
        return render_template('add_theory.html', form=form, err=err)


@app.route('/read_theory/<int:theory_id>', methods=['GET'])
def read_theory(theory_id):
    theor = TheoryModel(db.get_connection()).get(theory_id)
    return render_template('read_theory.html', t=theor)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')