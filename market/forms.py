from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length, EqualTo,Email, DataRequired, ValidationError
from market.models import users

class RegisterForm(FlaskForm):
    def validate_username(self, username_to_check):
        user_exist = users.query.filter_by(username=username_to_check.data).first()
        if user_exist:
            raise ValidationError("The username already exist")
        
    def validate_email(self, email_to_check):
        email_exist = users.query.filter_by(email=email_to_check.data).first()
        if email_exist:
            raise ValidationError("The email already exist")
        
    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email = StringField(label='Email Address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Register')
    

class LoginForm(FlaskForm):
    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    password = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    login = SubmitField(label='Login')
    
class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase')
    
class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell')