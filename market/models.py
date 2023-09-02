from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

#creating database for users
class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False, unique=True)
    budget = db.Column(db.Integer, nullable=False, default=1000)
    items = db.relationship('items', backref='owned_user', lazy=True)
    
    @property
    def budget_prettier(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget[:-3])}, {str(self.budget[-3:])}$'
    
    @property 
    def pass_word(self):
        return self.password
    
    @pass_word.setter
    def pass_word(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
            
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)
            
    
# Creates the various columns for items in the database
class items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(length=1000), nullable=False, unique=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    
    def __repr__(self):
        return f'Item: {self.name}'