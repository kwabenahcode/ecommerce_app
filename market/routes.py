from market import app
from market.models import items, users
from flask import render_template, redirect, url_for
from market.forms import RegisterForm
from market import db

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
                            password=form.password1.data,
                            )
        db.session.add(user_create_account)
        db.session.commit()
        return redirect(url_for('market_page'))
    return render_template('register.html', form=form)

# @app.route('/about/<user>')
# def about(user):
#     return f"<h1>This is the about page {user}'s</h1>"