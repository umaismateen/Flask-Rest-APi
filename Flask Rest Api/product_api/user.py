from flask import Blueprint, jsonify, render_template, request
from werkzeug.security import generate_password_hash

from product_api import db
from product_api.auth import token_required
from product_api.models import User
from product_api.schemas import users_schema


bp = Blueprint('user', __name__, url_prefix='/users')


@bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({'users': users_schema.dump(users)})


@bp.route('/', methods=['POST'])
def create_user():
    user_data = request.get_json()
    hashed_password = generate_password_hash(user_data['password'], method='sha256')

    new_user = User(username=user_data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})


@bp.route('/<user_id>', methods=['DELETE'])
@token_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            'username': user.username,
            'message': 'User Deleted Successfully'
        })
    return render_template('error_page.html', message='User Does Not Exist.'), 404
