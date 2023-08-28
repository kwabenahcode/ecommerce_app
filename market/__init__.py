from flask import Flask, render_template, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Created an instance of the Sqlalchemy
db = SQLAlchemy()

# Sqlalchemy connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
engine = create_engine("mysql+pymysql://user:pw@host/db", pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()
db.session.expire_on_commit = False
db.init_app(app)

from market import routes 

# with app.app_context():
#     db.create_all()