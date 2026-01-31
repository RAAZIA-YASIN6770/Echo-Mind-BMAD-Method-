"""
============================================
EchoMind AI - Authentication API
Epic 4: User Authentication
============================================

Endpoints:
- POST /api/auth/register : Register new child/parent/educator
- POST /api/auth/login    : Authenticate and get tokens
- POST /api/auth/refresh  : Refresh access token
"""

from flask import Blueprint, request, jsonify
import logging
import uuid
from datetime import datetime
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.auth_service import get_auth_service
from config import settings

logger = logging.getLogger(__name__)

# Create Blueprint
auth_bp = Blueprint('auth', __name__)

# Mock Database for Sprint 4 (to be replaced with real DB in Sprint 5)
# In production, this would query the 'users' table in PostgreSQL
mock_user_db = {}

@auth_bp.route('/api/auth/register', methods=['POST'])
def register():
    \"\"\"
    Register a new user (COPPA compliant)
    \"\"\"
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'child')  # child, parent, educator
    age = data.get('age')
    
    if not all([email, password, age]):
        return jsonify({"success": False, "error": "Missing required fields"}), 400
    
    # COPPA Check
    auth_service = get_auth_service()
    if int(age) < 13 and role == 'child':
        parent_email = data.get('parent_email')
        if not parent_email:
            return jsonify({
                "success": False, 
                "error": "Parental consent (email) is required for children under 13"
            }), 403
    
    # Check if user already exists
    if email in mock_user_db:
        return jsonify({"success": False, "error": "User already exists"}), 409
    
    # Hash password
    hashed_pwd = auth_service.hash_password(password)
    
    # Create user
    user_id = str(uuid.uuid4())
    new_user = {
        "user_id": user_id,
        "email": email,
        "password_hash": hashed_pwd,
        "role": role,
        "age": age,
        "parent_pin": data.get('parent_pin'), # Optional PIN
        "created_at": datetime.utcnow().isoformat()
    }
    
    # "Save" to mock DB
    mock_user_db[email] = new_user
    
    logger.info(f"✅ User registered: {email} | Role: {role}")
    
    return jsonify({
        "success": True,
        "message": "User registered successfully",
        "user_id": user_id
    }), 201

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    \"\"\"
    Authenticate user and return JWT tokens
    \"\"\"
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({"success": False, "error": "Email and password required"}), 400
    
    # Find user
    user = mock_user_db.get(email)
    auth_service = get_auth_service()
    
    if not user or not auth_service.verify_password(password, user['password_hash']):
        return jsonify({"success": False, "error": "Invalid email or password"}), 401
    
    # Create tokens
    token_data = {
        "sub": user['user_id'],
        "email": user['email'],
        "role": user['role']
    }
    
    access_token = auth_service.create_access_token(token_data)
    refresh_token = auth_service.create_refresh_token(token_data)
    
    logger.info(f"🔑 User logged in: {email}")
    
    return jsonify({
        "success": True,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "user_id": user['user_id'],
            "email": user['email'],
            "role": user['role']
        }
    }), 200

@auth_bp.route('/api/auth/refresh', methods=['POST'])
def refresh():
    \"\"\"
    Refresh access token using refresh token
    \"\"\"
    data = request.get_json()
    refresh_token = data.get('refresh_token')
    
    if not refresh_token:
        return jsonify({"success": False, "error": "Refresh token required"}), 400
    
    auth_service = get_auth_service()
    payload = auth_service.decode_token(refresh_token)
    
    if not payload or payload.get('type') != 'refresh':
        return jsonify({"success": False, "error": "Invalid or expired refresh token"}), 401
    
    # Create new access token
    new_data = {
        "sub": payload['sub'],
        "email": payload['email'],
        "role": payload['role']
    }
    new_access_token = auth_service.create_access_token(new_data)
    
    return jsonify({
        "success": True,
        "access_token": new_access_token,
        "token_type": "bearer"
    }), 200
