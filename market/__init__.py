from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)


# Created an instance of the Sqlalchemy
db = SQLAlchemy()

# creating an instance of the Bcrypt
bcrypt = Bcrypt(app)

# creating an instance of the LoginManager
login_manager = LoginManager(app)
# Sqlalchemy connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'fab07273c260515be3aa1c06'
engine = create_engine("mysql+pymysql://user:pw@host/db", pool_pre_ping=True)
Session = sessionmaker(bind=engine)
session = Session()
db.session.expire_on_commit = False
db.init_app(app)
login_manager.login_view = 'login_page'
login_manager.login_message_category = 'info'

from market import routes

# with app.app_context():
#     db.create_all()
