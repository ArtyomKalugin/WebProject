from flask import Flask, url_for, request, render_template, make_response, jsonify
import sqlite3


class DB:
    def __init__(self):
        conn = sqlite3.connect('theory.db', check_same_thread=False)
        self.conn = conn

    def get_connection(self):
        return self.conn

    def __del__(self):
        self.conn.close()


class UserModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128),
                             salt VARCHAR(20)
                             )''')
        cursor.close()
        self.connection.commit()

    def exists(self, user_name):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?",
                       (user_name,))
        row = cursor.fetchone()

        return (True, row[0]) if row else (False,)

    def get(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (str(user_id),))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def insert(self, user_name, password_hash, salt):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (user_name, password_hash, salt) 
                          VALUES (?,?,?)''', (user_name, password_hash, salt))
        cursor.close()
        self.connection.commit()

    def delete(self, user_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM users WHERE id = ?''', (str(user_id),))
        cursor.close()
        self.connection.commit()


class TheoryModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS theory
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             title VARCHAR(100),
                             content VARCHAR(1000),
                             user VARCHAR(50),
                             data VARCHAR(20),
                             filename VARCHAR(50)
                             )''')
        cursor.close()
        self.connection.commit()

    def insert(self, title, content, user, data, filename):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO theory
                          (title, content, user, data, filename) 
                          VALUES (?,?,?,?,?)''', (title, content, user, data, filename))
        cursor.close()
        self.connection.commit()

    def get(self, theory_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM theory WHERE id = ?", (theory_id,))
        row = cursor.fetchone()
        return row

    def get_all(self, user=None):
        cursor = self.connection.cursor()
        if user:
            cursor.execute("SELECT * FROM theory WHERE user = ?",
                           (user,))
        else:
            cursor.execute("SELECT * FROM theory")
        rows = cursor.fetchall()
        return rows

    def delete(self, theory_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM theory WHERE id = ?''', (str(theory_id),))
        cursor.close()
        self.connection.commit()
