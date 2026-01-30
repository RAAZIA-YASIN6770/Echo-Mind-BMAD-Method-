"""
============================================
EchoMind AI - User Onboarding API
Sprint 4: Frontend Development & API Integration
============================================

This module handles new user onboarding:
- Creates user profile
- Assigns Mystery Seed (Prism by default)
- Initializes Knowledge Tree
- Returns complete onboarding data for frontend

Endpoint: POST /api/user/onboarding
"""

from flask import Blueprint, request, jsonify
from datetime import datetime
import logging
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.seed_service import get_seed_service
from services.tree_health_service import get_tree_health_service

logger = logging.getLogger(__name__)

# Create Blueprint
onboarding_bp = Blueprint('onboarding', __name__)


@onboarding_bp.route('/api/user/onboarding', methods=['POST'])
def create_user_onboarding():
    """
    Create a new user profile with Mystery Seed and Knowledge Tree
    
    Request Body:
    {
        "name": "Ahmed",
        "age": 10,
        "grade_level": 5,
        "parent_email": "parent@example.com" (optional)
    }
    
    Response:
    {
        "success": true,
        "user": {
            "user_id": 123,
            "name": "Ahmed",
            "age": 10,
            "grade_level": 5,
            "created_at": "2026-01-30T23:10:00Z"
        },
        "seed": {
            "seed_type": "prism",
            "seed_name": "Prism Seed",
            "seed_emoji": "💎",
            "description": "...",
            "current_stage": 1,
            "current_stage_name": "Tiny Crystal",
            "current_stage_emoji": "✨",
            "total_points": 0,
            "special_ability": "...",
            "fun_fact": "..."
        },
        "tree": {
            "overall_health": 0,
            "tree_state": "Ready to grow! 🌱",
            "total_concepts": 0,
            "branches": {},
            "growth_tips": [...]
        },
        "welcome_message": "Welcome Ahmed! You received a 💎 Prism Seed!"
    }
    """
    try:
        # Get request data
        data = request.get_json()
        
        # Validate required fields
        if not data:
            return jsonify({
                "success": False,
                "error": "No data provided"
            }), 400
        
        name = data.get('name')
        age = data.get('age')
        grade_level = data.get('grade_level')
        
        if not all([name, age, grade_level]):
            return jsonify({
                "success": False,
                "error": "Missing required fields: name, age, grade_level"
            }), 400
        
        # Validate age and grade level
        try:
            age = int(age)
            grade_level = int(grade_level)
            
            if age < 5 or age > 18:
                return jsonify({
                    "success": False,
                    "error": "Age must be between 5 and 18"
                }), 400
            
            if grade_level < 1 or grade_level > 12:
                return jsonify({
                    "success": False,
                    "error": "Grade level must be between 1 and 12"
                }), 400
                
        except ValueError:
            return jsonify({
                "success": False,
                "error": "Age and grade_level must be numbers"
            }), 400
        
        # TODO: In production, save to database and get user_id
        # For now, generate a mock user_id
        user_id = hash(name + str(datetime.utcnow())) % 1000000
        
        # Create user profile
        user_profile = {
            "user_id": user_id,
            "name": name,
            "age": age,
            "grade_level": grade_level,
            "parent_email": data.get('parent_email'),
            "created_at": datetime.utcnow().isoformat()
        }
        
        # TODO: Save to database
        # db.execute("""
        #     INSERT INTO users (user_id, name, age, grade_level, parent_email, created_at)
        #     VALUES (?, ?, ?, ?, ?, ?)
        # """, (user_id, name, age, grade_level, parent_email, created_at))
        
        logger.info(f"✅ Created user profile for {name} (ID: {user_id})")
        
        # Step 2: Assign Prism Seed (default for all new users)
        seed_service = get_seed_service()
        
        # Force assign Prism seed
        seed_assignment = {
            "user_id": user_id,
            "seed_type": "prism",
            "seed_name": "Prism Seed",
            "seed_emoji": "💎",
            "description": "A crystalline seed that refracts light into rainbows. Grows when you solve puzzles and think logically.",
            "current_stage": 1,
            "current_stage_name": "Tiny Crystal",
            "current_stage_emoji": "✨",
            "total_points": 0,
            "next_stage_points": 50,
            "special_ability": "Reveals hidden patterns in problems",
            "fun_fact": "Prism Seeds are said to be formed from frozen starlight!",
            "assigned_at": datetime.utcnow().isoformat()
        }
        
        # TODO: Save to database
        # db.execute("""
        #     INSERT INTO user_seeds (user_id, seed_type, total_points, current_stage, assigned_at)
        #     VALUES (?, ?, ?, ?, ?)
        # """, (user_id, 'prism', 0, 1, assigned_at))
        
        logger.info(f"🌱 Assigned Prism Seed to user {user_id}")
        
        # Step 3: Initialize Knowledge Tree (empty for new user)
        tree_service = get_tree_health_service()
        tree_state = tree_service.calculate_tree_health([])
        
        logger.info(f"🌳 Initialized Knowledge Tree for user {user_id}")
        
        # Step 4: Create welcome message
        welcome_message = f"Welcome {name}! You received a {seed_assignment['seed_emoji']} {seed_assignment['seed_name']}!"
        
        # Return complete onboarding data
        response = {
            "success": True,
            "user": user_profile,
            "seed": seed_assignment,
            "tree": tree_state,
            "welcome_message": welcome_message,
            "next_steps": [
                "Ask your first question to start growing your tree!",
                "Explore different topics to grow all your branches!",
                "Earn points to level up your Mystery Seed!"
            ]
        }
        
        logger.info(f"🎉 Onboarding complete for user {user_id}")
        
        return jsonify(response), 201
        
    except Exception as e:
        logger.error(f"❌ Onboarding error: {str(e)}")
        import traceback
        traceback.print_exc()
        
        return jsonify({
            "success": False,
            "error": "Internal server error during onboarding",
            "details": str(e)
        }), 500


@onboarding_bp.route('/api/user/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id: int):
    """
    Get complete user profile including seed and tree data
    
    Response:
    {
        "success": true,
        "user": {...},
        "seed": {...},
        "tree": {...}
    }
    """
    try:
        # TODO: Fetch from database
        # For now, return mock data
        
        seed_service = get_seed_service()
        tree_service = get_tree_health_service()
        
        # Mock user data
        user_profile = {
            "user_id": user_id,
            "name": "Ahmed",
            "age": 10,
            "grade_level": 5,
            "created_at": "2026-01-30T23:10:00Z"
        }
        
        # Mock seed data (Prism at stage 2 with 75 points)
        seed_data = seed_service.calculate_growth_stage("prism", 75)
        seed_data["seed_type"] = "prism"
        seed_data["seed_name"] = "Prism Seed"
        seed_data["seed_emoji"] = "💎"
        
        # Mock tree data (some progress)
        mock_concepts = [
            {"concept_id": "addition", "category": "math", "mastery_score": 60, "attempts": 5},
            {"concept_id": "subtraction", "category": "math", "mastery_score": 45, "attempts": 3},
        ]
        tree_data = tree_service.calculate_tree_health(mock_concepts)
        
        return jsonify({
            "success": True,
            "user": user_profile,
            "seed": seed_data,
            "tree": tree_data
        }), 200
        
    except Exception as e:
        logger.error(f"❌ Error fetching profile: {str(e)}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


# Health check endpoint
@onboarding_bp.route('/api/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "EchoMind AI Onboarding API",
        "timestamp": datetime.utcnow().isoformat()
    }), 200
