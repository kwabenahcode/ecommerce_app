from flask import Flask, render_template

app = Flask(__name__)

#Routes for the home Page
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

#

# @app.route('/about/<user>')
# def about(user):
#     return f"<h1>This is the about page {user}'s</h1>"

