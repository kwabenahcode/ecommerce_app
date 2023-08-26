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

# @app.route('/about/<user>')
# def about(user):
#     return f"<h1>This is the about page {user}'s</h1>"