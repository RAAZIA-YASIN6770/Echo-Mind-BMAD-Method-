"""
============================================
EchoMind AI - Monitoring API
Epic 10: Production Monitoring
============================================

Endpoints:
- GET /api/admin/metrics : Live system performance metrics
- GET /api/admin/health  : Detailed health check
"""

from flask import Blueprint, jsonify
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.monitoring_service import get_monitor
from middleware.auth_middleware import token_required, roles_required

# Create Blueprint
monitor_bp = Blueprint('monitor', __name__)

@monitor_bp.route('/api/admin/metrics', methods=['GET'])
@token_required
@roles_required(['educator', 'parent']) # Admin roles
def get_metrics():
    \"\"\"Return live performance metrics\"\"\"
    monitor = get_monitor()
    metrics = monitor.get_system_metrics()
    
    return jsonify({
        "success": True,
        "metrics": metrics
    })

@monitor_bp.route('/api/admin/health', methods=['GET'])
def health_check():
    \"\"\"Detailed health check for load balancers\"\"\"
    monitor = get_monitor()
    metrics = monitor.get_system_metrics()
    
    # Simple logic for load balancer health
    status_code = 200
    if metrics['error_count'] > 100: # Example logic
        status_code = 503
        
    return jsonify({
        "status": metrics['status'],
        "uptime": metrics['uptime_seconds'],
        "version": "1.0.0"
    }), status_code
