from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length

class RegisterForm(FlaskForm):
    username = StringField(label='User Name', validators='Length(min=2, max=)')
    email = StringField(label='Email Address')
    password1 = PasswordField(label='Password')
    password2 = PasswordField(label='Confirm Password')
    submit = SubmitField(label='Register')