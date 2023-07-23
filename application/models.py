from application.database import db
from flask_sqlalchemy import SQLAlchemy
from passlib.hash import sha256_crypt
from datetime import datetime

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    
    cart_item  = db.relationship('CartItem', uselist=False, backref='user')
    
    def __init__(self, name, password):
        self.name = name
        self.password = sha256_crypt.hash(password)


class Manager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    category = db.relationship("Category", backref="creator")
    def __init__(self, username, password):
        self.username = username
        self.password = sha256_crypt.hash(password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    maker = db.Column(db.Integer, db.ForeignKey("manager.id"))  # related to manager 
    prod = db.relationship("Product", backref="category", lazy=True)  # related to products

    def __repr__(self):
        return self.name

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    unit = db.Column(db.String(20), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    parent = db.Column(db.Integer, db.ForeignKey("category.id"))
   
    cart_items = db.relationship('CartItem', backref='product', lazy=True)
    p_items = db.relationship('PurchasedProduct', backref='product', lazy=True)

    def __repr__(self):
        return self.name

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id', ondelete='CASCADE'))
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Integer, nullable=False)

class PurchasedProduct(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float, nullable=False)
      # Add this line to include purchased_at field
    purchased_at = db.Column(db.DateTime, default=datetime.utcnow)

   
    def __repr__(self):
        return f"PurchasedProduct(id={self.id}, user_id={self.user_id}, product_id={self.product_id})"