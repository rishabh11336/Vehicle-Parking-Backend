from app.models.models import db,User
from app.app import app

from flask import Flask
from flask import request, jsonify
from flask_jwt_extended import  jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash 



@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    full_name = data['full_name']
    email = data['email']
    password = data['password']
    role = data['role']
    phone = data['phone']
    address = data['address']
    pin_code = data['pin_code']
    # Check if user already exists
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'User already exists'}), 400
    # Create user with 'user' role
    user = User(full_name=full_name, email=email, role=role, phone=phone, address=address, pin_code=pin_code, password_hash=generate_password_hash(password))
    # user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User registered successfully'}), 201
