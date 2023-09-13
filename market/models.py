from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

# creating database for users


class users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False, unique=True)
    budget = db.Column(db.Integer, nullable=False, default=10000)
    items = db.relationship('items', backref='owned_user', lazy=True)

    @property
    def budget_prettier(self):
        myBudget_string = str(self.budget)
        if len(myBudget_string) >= 4:
            return f'{myBudget_string[:-3]},{myBudget_string[-3:]} $'
        else:
            return f'{myBudget_string}'

    @property
    def pass_word(self):
        return self.password

    @pass_word.setter
    def pass_word(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(
            plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password, attempted_password)
    
    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price
    
    def can_sell(self, item_obj):
        return item_obj in self.items
        


# Creates the various columns for items in the database
class items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False, unique=True)
    barcode = db.Column(db.String(12), nullable=False, unique=True)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(length=1000),
                            nullable=False, unique=True)
    owner = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'Item: {self.name}'
    
    def assigned_user(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()
        
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
        
class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    product_name = db.Column(db.String(50), nullable=False, unique=True)
    product_desc = db.Column(db.String(1000), nullable=False, unique=True)
    product_price = db.Column(db.String(50), nullable=False)
    product_image = db.Column(db.LargeBinary)
    
    # def __init__(self, product_name, product_desc, product_price, product_image):
    #     self.product_name = product_name
    #     self.product_desc = product_desc
    #     self.product_price = product_price
    #     self.product_image = product_image
        
    
