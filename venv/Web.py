from flask import Flask, url_for, request, render_template, make_response, jsonify
from Classes import DB, NewsModel, UserModel


app = Flask(__name__)


@app.route('/main')
def main_page():
    return render_template('main_page.html')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')