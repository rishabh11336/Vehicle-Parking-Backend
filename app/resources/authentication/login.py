from app.app import app
from app.models.models import db,User

from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask import request, jsonify



@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    email = data['email']
    password = data['password']
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Create JWT token
    access_token = create_access_token(identity=user.email)
    # Get user roles
    roles = user.role
    print(email, roles)
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': {
            'email': user.email,
            'roles': roles
        }
    }), 200


