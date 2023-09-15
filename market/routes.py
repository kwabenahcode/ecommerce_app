import base64
from market import app
from market.models import items, users, Products
from flask import render_template, redirect, url_for, flash, request
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm, ProductUploadForm, ItemsForm
from market import db
from sqlalchemy.exc import SQLAlchemyError
from flask_login import login_user, current_user, logout_user, login_required


# Route for the home Page
@app.route('/', methods =['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home_page():
    item = Products.query.all()
    for img in item:
        img.product_image = base64.b64encode(img.product_image).decode('utf-8')
    return render_template('home.html', current_user=current_user, items=item )

# Route for the market Page
@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    purchase_form =PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == 'POST':
        purchased_item = request.form.get('purchased_item')
        p_item_object = items.query.filter_by(name=purchased_item).first()
        if  p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.assigned_user(current_user)
                flash(f'You purchased {p_item_object.name} for {p_item_object.price}')
            else:
                flash('Please you do not have enough balance', category='danger')
        sold_item = request.form.get('sold_item')
        s_item_object = items.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash("Item was sold back to the market successfuly", category='success')
            else:
                flash(f"Something went worng with selling {s_item_object.name}", category='danger')
        return redirect(url_for('carts_page'))
    
    if request.method == "GET":
        item = items.query.all()
        owned_items = items.query.filter_by(owner =current_user.id)
        return render_template('market.html', items=item, dollar='$', current_user=current_user, purchase_form = purchase_form, selling_form=selling_form, owned_items=owned_items)


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
        flash(f"Account created successfully! you are now logged in as {user_create_account.username}", category='success')
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
            flash("Your username or password is invalid! ", category='danger')
    return render_template('login.html', form=form, current_user=current_user)


@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been Logged-out', category='info')
    return redirect(url_for('home_page'))

@app.route('/products-trends', methods=['GET', 'POST'])
def add_products():
    form = ProductUploadForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_product = Products(
                    product_name= form.product_name.data,
                    product_desc= form.product_desc.data,
                    product_price= form.product_price.data,
                    product_image= form.product_image.data.read()  # Read the image binary data
                )
                db.session.add(new_product)
                db.session.commit()
                flash('Product uploaded successfully', category='success')
                return redirect(url_for('add_products'))
            except SQLAlchemyError as e:
                db.session.rollback()  # Rollback changes in case of an error
                flash('Error adding product to the database', category='error')
                app.logger.error(str(e))  # Log the error for debugging
    return render_template('addProductsTrends.html', form=form)

@app.route('/add-Items', methods=['POST', 'GET'])
def addItem_page():
    form = ItemsForm()
    if request.method == 'POST':
        try:
            new_items = items(name = form.name.data,
                              barcode= form.barcode.data,
                              description= form.description.data,
                              price = form.price.data
                            )
            db.session.add(new_items)
            db.session.commit()
            flash('Item uploaded successfully', category='success')
            return redirect(url_for('addItem_page'))
        except SQLAlchemyError as e:
                db.session.rollback()  # Rollback changes in case of an error
                flash('Error adding Item to the database', category='error')
                app.logger.error(str(e))
    return render_template('add_items.html', form=form)

@app.route('/carts', methods=['POST', 'GET'])
def carts_page():
    selling_form = SellItemForm()
    purchase_form =PurchaseItemForm()
# Sell Item Logic
    if request.method == "POST":
        purchased_item = request.form.get('purchased_item')
        p_item_object = items.query.filter_by(name=purchased_item).first()
        if  p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.assigned_user(current_user)
                flash(f'You purchased {p_item_object.name} for {p_item_object.price}')
            else:
                flash('Please you do not have enough balance', category='danger')
        sold_item = request.form.get('sold_item')
        s_item_object = items.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash("Item was sold back to the market successfuly", category='success')
            else:
                flash(f"Something went worng with selling {s_item_object.name}", category='danger')
        return redirect(url_for('market_page'))
    if request.method == "GET":
        item = items.query.all()
        owned_items = items.query.filter_by(owner =current_user.id)
        return render_template('carts.html', items=item, dollar='$', current_user=current_user, selling_form=selling_form, purchase_form = purchase_form, owned_items=owned_items)
    




# @app.route('/about/<user>')
# def about(user):
#     return f"<h1>This is the about page {user}'s</h1>"
