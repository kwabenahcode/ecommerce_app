from flask import Flask, render_template

app = Flask(__name__)

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
    return render_template('market.html', items=items)

# @app.route('/about/<user>')
# def about(user):
#     return f"<h1>This is the about page {user}'s</h1>"

