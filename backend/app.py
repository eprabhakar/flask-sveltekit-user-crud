import os
from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User
from dotenv import load_dotenv
from flask import abort

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app, supports_credentials=True)
db.init_app(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    user = User(username=data['username'], email=data['email'],
                role=data.get('role', 'user'),
                password_hash=generate_password_hash(data['password']))
    db.session.add(user)
    db.session.commit()
    #session['user_id'] = user.id
    return jsonify(user.to_dict())

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password_hash, data['password']):
        session['user_id'] = user.id
        return jsonify(user.to_dict())
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 204


@app.route('/me')
def me():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        return jsonify(user.to_dict())
    return jsonify({'user': None})

@app.route('/users')
def list_users():
    user_id = session.get('user_id')
    if not user_id:
        return '', 401
    #user = User.query.get(user_id)
    #if user.role != 'admin':
    #    return '', 403
    return jsonify([u.to_dict() for u in User.query.all()])

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    admin_id = session.get('user_id')
    admin = User.query.get(admin_id)
    if not admin or admin.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    data = request.json
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    #user.role = data.get('role', user.role)
    db.session.commit()
    return jsonify(user.to_dict())

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    admin_id = session.get('user_id')
    admin = User.query.get(admin_id)
    if not admin or admin.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return '', 204

@app.route('/user', methods=['POST'])
def create_user():
    admin_id = session.get('user_id')
    admin = User.query.get(admin_id)
    if not admin or admin.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    data = request.json
    if not all(k in data for k in ('username', 'email', 'password', 'role')):
        return jsonify({'error': 'Missing fields'}), 400

    existing_user = User.query.filter(
        (User.username == data['username']) | (User.email == data['email'])
    ).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 400

    new_user = User(
        username=data['username'],
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        role=data['role']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)