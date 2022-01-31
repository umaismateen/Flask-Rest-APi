from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///scrapy_products.db'

db = SQLAlchemy(app)
ma = Marshmallow(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error_page.html', message='Url Does not Exist.'), 404


from product_api import auth, product, user

app.register_blueprint(auth.bp)
app.register_blueprint(product.bp)
app.register_blueprint(user.bp)
app.register_error_handler(404, page_not_found)
