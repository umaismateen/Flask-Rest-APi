from flask import Blueprint, render_template, request, jsonify

from product_api import db
from product_api.auth import token_required
from product_api.models import Product
from product_api.schemas import product_schema, products_schema

bp = Blueprint('product', __name__, url_prefix='/products')


@bp.route('/', methods=['GET'])
@token_required
def get_products():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    products = Product.query.filter_by().paginate(page=page, per_page=per_page).items
    return jsonify({'products': [extract_product(product) for product in products_schema.dump(products)]})


def extract_product(raw_product):
    product = raw_product['product']
    return {
        'name': product['name'],
        'url': product['url'],
        'retailer_sku': product['retailer_sku']
    }


@bp.route('/<retailer_sku>', methods=['GET'])
@token_required
def get_product(retailer_sku):
    product = Product.query.filter_by(product_id=retailer_sku).first()
    if product:
        return jsonify(product_schema.dump(product)['product'])
    return render_template('error_page.html', message='Product Does Not Exist.'), 404


@bp.route('/<retailer_sku>', methods=['PUT'])
@token_required
def update_product(retailer_sku):
    product = Product.query.filter_by(product_id=retailer_sku).first()
    if product:
        name = request.json['name']
        description = request.json['description']

        updated_product = {
            **product_schema.dump(product)['product'],
            'name': name,
            'description': description,
        }

        product.product = updated_product
        db.session.commit()
        return updated_product
    return render_template('error_page.html', message='Product Does Not Exist.'), 404


@bp.route('/<retailer_sku>', methods=['DELETE'])
@token_required
def delete_product(retailer_sku):
    product = Product.query.filter_by(product_id=retailer_sku).first()
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify(product_schema.dump(product)['product'])
    return render_template('error_page.html', message='Product Does Not Exist.'), 404
