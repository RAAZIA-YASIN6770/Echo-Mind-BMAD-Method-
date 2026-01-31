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
from api.auth import auth_bp
from api.parent import parent_bp
from api.monitor import monitor_bp
from middleware.security_waf import SecurityWAF
from services.monitoring_service import get_monitor
import time
from flask import g

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
app.register_blueprint(auth_bp)
app.register_blueprint(parent_bp)
app.register_blueprint(monitor_bp)

# Metrics Tracking Middleware
@app.before_request
def start_timer():
    g.start_time = time.time()

@app.after_request
def log_request(response):
    if hasattr(g, 'start_time'):
        latency = (time.time() - g.start_time) * 1000
        monitor = get_monitor()
        monitor.track_request(
            latency_ms=latency,
            success=(response.status_code < 400),
            error_msg=None if response.status_code < 400 else response.status
        )
    return response

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
