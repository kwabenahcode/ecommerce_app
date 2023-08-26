from flask import Flask, render_template, current_app
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)


# Created an instance of the Sqlalchemy
db = SQLAlchemy()
# Sqlalchemy connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db.init_app(app)



# Creates the various columns in the database
class items(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1000), nullable=False, unique=True)
    
    def __repr__(self):
        return f'Item: {self.name}'


#Routes for the home Page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

#Routes for the market Page
@app.route('/market')
def market_page():
    items = [
        {'id': 1, 'name': 'Phone', 'barcode': '10923044', 'price': 500 },
        {'id': 2, 'name': 'Laptop', 'barcode': '10906101', 'price': 900},
        {'id': 3, 'name': 'keyboard', 'barcode': '10903933', 'price': 200}
        ]
    return render_template('market.html', items=items, dollar='$')

# @app.route('/about/<user>')
# def about(user):
#     return f"<h1>This is the about page {user}'s</h1>"

