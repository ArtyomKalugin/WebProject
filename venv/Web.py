from flask import Flask, url_for, request, render_template, make_response, jsonify, session, redirect
from Classes import DB, TheoryModel, UserModel
from LoginForm import LoginForm, SignInForm
import string
from werkzeug.security import generate_password_hash
import bcrypt


app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()


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
                user.insert(name, hash)
                session['username'] = name
                return redirect('/success_login')
            else:
                err = 'Пароль должен быть длиннее 5 символов'
                return render_template('login.html', title='Регистрация', form=form, err=err)

    return render_template('login.html', title='Регистрация', form=form, err=err)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    return redirect('/login')


@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    form = SignInForm()
    err = None
    if form.validate_on_submit():
        name = request.form['username']
        password = request.form['password']

        user = UserModel(db.get_connection())
        exists = user.exists(name, generate_password_hash(password))
        hash = generate_password_hash(password)
        old = UserModel(db.get_connection()).get(8)
        isSamePassword = bcrypt.hashpw(hash, old)
        print(isSamePassword)
        if (exists[0]):
            session['username'] = name
            return redirect('/success_login')
        else:
            err = 'Ошибка в логине или пароле'
            return render_template('sign_in.html', title='Авторизация', form=form, err=err)

    return render_template('sign_in.html', title='Авторизация', form=form, err=err)


@app.route('/success_login')
def success_login():
    return render_template('success_login.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')