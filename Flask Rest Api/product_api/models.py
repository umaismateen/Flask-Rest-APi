from product_api import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(80))


class Product(db.Model):
    product_id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.JSON, unique=True)
