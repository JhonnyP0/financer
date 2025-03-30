from flask_wtf import FlaskForm
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config('SECRET_KEY')= os.getenv('API_KEY')

#flask login config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#database connection
def db_connect():
    return mysql.connector.connect(
    host = 'localhost',
    #host = os.getenv('DB_HOST'),
    port = os.getenv('DB_PORT'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_NAME')
    )

#user class flask login
class User(UserMixin):
    def __init__(self,id,username):
        self.id=id
        self.username=username

@login_manager.user_loader
def userload(user_id):
    conn = db_connect()
    cursor = conn.cursor()

    cursor.execute("select * from users where id = %s", (user_id,))
    user= cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return User(user['id'], user['username'])
    else:
        return None

@app.route('/', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username=request.form['username']
        password=request.form['password']

        conn=db_connect()
        cursor=conn.cursor()

        cursor.execute("select * from users where username = %s", (username,))

        user=cursor.fetchone()

        cursor.close()
        conn.close()

        if user:
            if check_password_hash(user['password'], password):
                userlog=User(user['id'],user['username'],user['email'])
                login_user(userlog)
                flash('Login successful', 'success')
                return(redirect(url_for('dashboard')))
            else:
                flash('Password incorrect', 'danger')
        else:
            flash('User cannot be found', 'danger')

    return render_template('login.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)