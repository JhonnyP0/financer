from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import mysql.connector
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv
import os
from source import User, LoginForm, RegisterForm

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY']= os.getenv('API_KEY')

#flask login config
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#database connection
def db_connect():
    return mysql.connector.connect(
    host = 'localhost',                     #for development
    #host = os.getenv('DB_HOST'),           #for production
    port = os.getenv('DB_PORT'),
    user = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    database = os.getenv('DB_NAME')
    )

@login_manager.user_loader
def userload(user_id):
    conn = db_connect()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("select * from users where id = %s", (user_id,))
    user= cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        return User(user['id'], user['username'], user['password_hash'])
    return None

@app.route('/', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        conn=db_connect()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (form.username.data,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], form.password.data):
            userobj=User(user['id'], user['username'], user['password_hash'])
            login_user(userobj)
            flash('loged in','success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect credentials', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        password=form.password.data
        hashed_password=generate_password_hash(password)
        try:
            conn=db_connect()
            cursor=conn.cursor(dictionary=True)
            cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)", (form.username.data, hashed_password, form.email.data,))
            print(form.username.data, hashed_password, form.email.data)
            conn.commit()
            flash('Register succeded','success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(str(e), 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html', form=form)

@app.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    return render_template('dashboard.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5050, debug=True)