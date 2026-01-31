"""
============================================
EchoMind AI - Flask API Server
Sprint 4: Frontend Development & API Integration
============================================

Main Flask application that serves all API endpoints
"""

from flask import Flask
from flask_cors import CORS
import logging
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.dirname(__file__))

from api.onboarding import onboarding_bp
from api.chat import chat_bp
from middleware.security_waf import SecurityWAF

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)

# Enable CORS for React Native frontend
CORS(app, resources={
    r"/api/*": {
        "origins": "*",  # In production, specify your frontend domain
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Apply Lock 1: Security WAF (Network Layer Simulation)
SecurityWAF.apply_lock(app)

# Register blueprints
app.register_blueprint(onboarding_bp)
app.register_blueprint(chat_bp)

# Root endpoint
@app.route('/')
def index():
    """Root endpoint with API information"""
    return {
        "service": "EchoMind AI API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "onboarding": "POST /api/user/onboarding",
            "profile": "GET /api/user/<user_id>/profile",
            "health": "GET /api/health"
        },
        "documentation": "See README-SPRINT-4.md for API documentation"
    }


if __name__ == '__main__':
    logger.info("🚀 Starting EchoMind AI API Server...")
    logger.info("📡 API will be available at http://localhost:5000")
    logger.info("📚 Endpoints:")
    logger.info("   POST /api/user/onboarding - Create new user")
    logger.info("   GET  /api/user/<id>/profile - Get user profile")
    logger.info("   GET  /api/health - Health check")
    
    # Run Flask app
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
