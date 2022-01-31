import datetime
import functools
import jwt

from flask import Blueprint, jsonify, render_template, request, session
from werkzeug.security import check_password_hash

from product_api import app
from product_api.models import User

bp = Blueprint('auth', __name__)


def token_required(f):
    @functools.wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'access-token' in request.headers:
            token = request.headers['access-token']
        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            User.query.filter_by(user_id=data['user_id']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated


@bp.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return render_template('error_page.html', message='Could not verify.'), 401

    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return render_template('error_page.html', message='User Does Not Exist.'), 401

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({
            'user_id': user.user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        }, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('UTF-8')})

    return render_template('error_page.html', message='Password Incorrect.'), 401


@bp.route("/logout")
@token_required
def logout():
    session.clear()
    return jsonify({'message': 'Token is removed!'})
