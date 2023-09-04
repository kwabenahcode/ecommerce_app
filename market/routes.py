from market import app
from market.models import items, users
from flask import render_template, redirect, url_for, flash
from market.forms import RegisterForm, LoginForm
from market import db
from flask_login import login_user, current_user, logout_user, login_required


# Routes for the home Page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html', current_user=current_user)

# Routes for the market Page


@app.route('/market')
@login_required
def market_page():
    item = items.query.all()
    return render_template('market.html', items=item, dollar='$', current_user=current_user)


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
        login_user(user_create_account)
        flash(f"Account created successfully! you are now logged in as {user_create_account.username}")
        return redirect(url_for('market_page'))
    if form.errors != {}:
        for error_messages in form.errors.values():
            flash(f'The error is {error_messages}', category='danger')
    return render_template('register.html', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = users.query.filter_by(
            username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(
                f'success! you are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))
        else:
            flash("Your username and password do not match! ", category='danger')
    return render_template('login.html', form=form, current_user=current_user)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been Logged-out', category='info')
    return redirect(url_for('home_page'))


# @app.route('/about/<user>')
# def about(user):
#     return f"<h1>This is the about page {user}'s</h1>"
