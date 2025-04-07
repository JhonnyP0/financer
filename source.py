from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import InputRequired,Length, EqualTo
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password


#login form

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit=SubmitField('Log In')
#register form

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(),Length(min=5,max=10)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    confirm_password=PasswordField('Repeat Password', validators=[InputRequired(), EqualTo('password', message='passwords must be the same')])
    email = EmailField('E-mail', validators=[InputRequired()])
    submit=SubmitField('Register')