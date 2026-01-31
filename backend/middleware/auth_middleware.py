"""
============================================
EchoMind AI - Auth Middleware
Epic 4: User Authentication
============================================

This module provides decorators to protect Flask routes:
- @token_required: Ensures a valid JWT is provided
- @roles_required: Ensures the user has the necessary role
"""

from flask import request, jsonify
from functools import wraps
import logging
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from services.auth_service import get_auth_service

logger = logging.getLogger(__name__)

def token_required(f):
    \"\"\"
    Decorator to ensure a valid JWT access token is provided in the header
    \"\"\"
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({
                "success": False, 
                "error": "Authentication token is missing"
            }), 401
        
        auth_service = get_auth_service()
        payload = auth_service.decode_token(token)
        
        if not payload or payload.get('type') != 'access':
            return jsonify({
                "success": False, 
                "error": "Invalid or expired token"
            }), 401
        
        # Add user info to request context (simulated with extra kwargs or global g)
        request.user = payload
        
        return f(*args, **kwargs)
    
    return decorated_function

def roles_required(allowed_roles):
    \"\"\"
    Decorator to ensure the authenticated user has the required role
    \"\"\"
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # token_required must be used before this
            if not hasattr(request, 'user'):
                return jsonify({
                    "success": False, 
                    "error": "Authentication required before role check"
                }), 401
            
            user_role = request.user.get('role')
            if user_role not in allowed_roles:
                logger.warning(f"🚫 Role violation | user={request.user.get('sub')} | required={allowed_roles} | actual={user_role}")
                return jsonify({
                    "success": False, 
                    "error": f"Role '{user_role}' does not have permission for this action"
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
