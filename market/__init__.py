from flask import Flask, render_template, current_app
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Created an instance of the Sqlalchemy
db = SQLAlchemy()

# Sqlalchemy connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
db.init_app(app)

from market import routes 