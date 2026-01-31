"""
============================================
EchoMind AI - Parent API
Epic 9: Parent Dashboard
============================================

Endpoints:
- GET /api/parent/dashboard : Get summary of all children
- GET /api/parent/child/<id>/report : Detailed child report
- PUT /api/parent/settings : Update parental controls
"""

from flask import Blueprint, request, jsonify
import logging
import sys
import os
from datetime import datetime

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from services.parent_service import get_parent_service
from middleware.auth_middleware import token_required, roles_required

logger = logging.getLogger(__name__)

# Create Blueprint
parent_bp = Blueprint('parent', __name__)

@parent_bp.route('/api/parent/dashboard', methods=['GET'])
@token_required
@roles_required(['parent'])
def get_dashboard():
    \"\"\"Get parent dashboard data\"\"\"
    parent_id = request.user.get('sub')
    service = get_parent_service()
    
    children = service.get_child_summaries(parent_id)
    
    return jsonify({
        "success": True,
        "parent_id": parent_id,
        "children": children
    })

@parent_bp.route('/api/parent/child/<child_id>/report', methods=['GET'])
@token_required
@roles_required(['parent'])
def get_child_report(child_id):
    \"\"\"Get detailed report for a specific child\"\"\"
    service = get_parent_service()
    report = service.get_detailed_report(child_id)
    
    return jsonify({
        "success": True,
        "report": report
    })

@parent_bp.route('/api/parent/settings', methods=['PUT'])
@token_required
@roles_required(['parent'])
def update_settings():
    \"\"\"Update parental controls\"\"\"
    parent_id = request.user.get('sub')
    data = request.get_json()
    
    if not data:
        return jsonify({"success": False, "error": "No data provided"}), 400
        
    service = get_parent_service()
    success = service.update_controls(parent_id, data)
    
    return jsonify({
        "success": success,
        "message": "Settings updated successfully" if success else "Failed to update settings"
    })

@parent_bp.route('/api/parent/child/<child_id>/weekly-email-preview', methods=['GET'])
@token_required
@roles_required(['parent'])
def email_preview(child_id):
    \"\"\"Preview the data that would be sent in a weekly email\"\"\"
    service = get_parent_service()
    email_data = service.generate_weekly_email_data(child_id)
    
    return jsonify({
        "success": True,
        "email_data": email_data
    })

@parent_bp.route('/api/parent/child/<child_id>/export-data', methods=['GET'])
@token_required
@roles_required(['parent'])
def export_child_data(child_id):
    \"\"\"Export all data for a child (GDPR Compliance)\"\"\"
    service = get_parent_service()
    report = service.get_detailed_report(child_id)
    
    # In production, this would be a full dump of all related rows
    return jsonify({
        "success": True,
        "export_date": datetime.utcnow().isoformat(),
        "data": report,
        "notice": "This export contains all personally identifiable and learning data for the specified child."
    })
