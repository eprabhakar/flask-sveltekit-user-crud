import os
import boto3
from flask import  Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
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

s3 = boto3.client('s3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
    )
bucket_name = os.environ.get('S3_BUCKET', 'my-cdev-bucket')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    user_id = request.form.get('user_id')

    if file:
        filename = secure_filename(file.filename)
        key = f"{user_id}/{filename}"  # e.g. 1234/passport.pdf

        s3.upload_fileobj(file, bucket_name, key)
        return jsonify({"message": "Uploaded", "file_key": key})
    return jsonify({"error": "No file uploaded"}), 400

@app.route('/search', methods=['GET'])
def search_users():
    query = request.args.get('q', '').strip()

    if not query:
        return jsonify({'error': 'Search query is required'}), 400

    # Search by username or email using LIKE
    users = db.session.query(User).filter(
        db.or_(
            User.username.ilike(f'%{query}%'),
            User.email.ilike(f'%{query}%')
        )
    ).all()
    # Convert to dict for response
    results = [{
        'id': user.id,
        'username': user.username,
        'email': user.email
    } for user in users]

    return jsonify(results), 200

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
    user = db.session.query(User).filter_by(username=data['username']).first()
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
        user = db.session.get(User,user_id)
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
    admin = db.session.get(User,admin_id)
    if not admin or admin.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    data = request.json
    user = db.session.get(User,user_id)
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
    admin = db.session.get(User,admin_id)
    if not admin or admin.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return '', 204

@app.route('/user', methods=['POST'])
def create_user():
    admin_id = session.get('user_id')
    admin = db.session.get(User, admin_id)
    if not admin or admin.role != 'admin':
        return jsonify({'error': 'Forbidden'}), 403

    data = request.json
    if not all(k in data for k in ('username', 'email', 'password', 'role')):
        return jsonify({'error': 'Missing fields'}), 400

    existing_user = db.session.query(User).filter(
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

@app.route('/users/<int:user_id>/reset-password', methods=['PUT'])
def reset_password(user_id):
    admin_id = session.get('user_id')
    #admin = User.query.get(admin_id)
    admin = db.session.get(User, admin_id)
    if not admin:
        return jsonify({'error': 'Forbidden'}), 403

    data = request.get_json()
    new_password = data.get('password')

    if not new_password:
        return jsonify({'error': 'Password required'}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({'message': 'Password reset successful'})


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)