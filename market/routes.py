from market import app
from market.models import items, users
from flask import render_template, redirect, url_for, flash
from market.forms import RegisterForm, LoginForm
from market import db
# from flask_login import login_user


#Routes for the home Page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

#Routes for the market Page
@app.route('/market')
def market_page():
    item = items.query.all()
    return render_template('market.html', items=item, dollar='$')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_create_account = users(
                            username=form.username.data,
                            email=form.email.data,
                            pass_word=form.password1.data,
                            )
        db.session.add(user_create_account)
        db.session.commit()
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for error_messages in form.errors.values():
            flash(f'The error is {error_messages}', category='danger')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = users.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            # login_user(user_details_exist)
            flash(f'success! you are logged in as: {attempted_user.username}', category='success')
            return redirect (url_for('market_page'))
        else:
            flash("Your username and password do not match! ", category='danger')
    return render_template('login.html', form=form)

# @app.route('/about/<user>')
# def about(user):
#     return f"<h1>This is the about page {user}'s</h1>"