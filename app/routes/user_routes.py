from flask import Blueprint, request, jsonify, render_template
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('user', __name__)

@bp.route('/users', methods=['POST'])
def create_user():
    data = request.form
    password_hash = generate_password_hash(data['password'])
    new_user = User(username=data['username'], email=data['email'], password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.form
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@bp.route('/create_user', methods=['GET'])
def create_user_form():
    return render_template('create_user.html')