from market import db, bcrypt



#creating database for users
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False, unique=True)
    budget = db.Column(db.Integer, nullable=False, default=1000)
    items = db.relationship('items', backref='owned_user', lazy=True)
    
    @property
    def pass_word(self):
        return self.password
    
    @pass_word.setter
    def pass_word(self, plain_text_password):
        self.password = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')
    
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