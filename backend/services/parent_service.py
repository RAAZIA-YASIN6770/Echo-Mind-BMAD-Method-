"""
============================================
EchoMind AI - Parent Service
Epic 9: Parent Dashboard
============================================

This service provides data and insights for parents:
1. Aggregate child learning progress
2. Summarize safety alerts
3. Manage parental controls (time limits, categories)
4. Generate report data
"""

import logging
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class ParentService:
    """
    Service for parent dashboard and child monitoring
    """
    
    def __init__(self, db_session=None):
        self.db = db_session
        # Mock data for demonstration when DB is not fully ready
        self._mock_child_data = {
            "child_1": {
                "name": "Ahmed",
                "mastery_trend": [65, 68, 72, 70, 75, 78, 82],
                "time_spent_today": 45,
                "safety_alerts": [
                    {"type": "pii_detected", "severity": "medium", "timestamp": "2026-01-31T09:00:00Z"},
                    {"type": "jailbreak_attempt", "severity": "high", "timestamp": "2026-01-30T14:30:00Z"}
                ]
            }
        }

    def get_child_summaries(self, parent_id: str) -> List[Dict[str, Any]]:
        """
        Get a high-level summary of all children linked to this parent
        """
        # In production: query DB for all users where parent_id = parent_id
        return [
            {
                "child_id": "child_1",
                "name": "Ahmed",
                "overall_health": 78,
                "active_seed": "Prism",
                "status": "Learning",
                "alerts_active": True
            }
        ]

    def get_detailed_report(self, child_id: str) -> Dict[str, Any]:
        """
        Get detailed progress and safety metrics for a specific child
        """
        # In production: aggregate from ConceptMastery and SafetyLog tables
        child_data = self._mock_child_data.get(child_id, self._mock_child_data["child_1"])
        
        return {
            "child_id": child_id,
            "name": child_data["name"],
            "learning_insights": {
                "top_performing": "Mathematics",
                "needs_practice": "Language",
                "mastery_score": 82,
                "trend": child_data["mastery_trend"],
                "total_questions_asked": 154
            },
            "safety_report": {
                "safe_interactions": 98,
                "pii_blocked": 4,
                "jailbreak_attempts": 1,
                "alerts": child_data["safety_alerts"]
            },
            "usage": {
                "today_minutes": child_data["time_spent_today"],
                "weekly_avg_minutes": 52,
                "limit_minutes": 60
            }
        }

    def update_controls(self, parent_id: str, settings: Dict[str, Any]) -> bool:
        """
        Update parental controls like time limits and allowed categories
        """
        # In production: update ParentSettings table
        logger.info(f"Updated controls for parent {parent_id}: {settings}")
        return True

    def generate_weekly_email_data(self, child_id: str) -> Dict[str, Any]:
        """
        Prepare data for a weekly progress email
        """
        report = self.get_detailed_report(child_id)
        return {
            "subject": f"Weekly Learning Report for {report['name']}",
            "summary": f"{report['name']} achieved a 15% increase in Science mastery this week! 🌳",
            "highlights": [
                "Mastered 3 new concepts in Math",
                "Earned the 'Curious Soul' badge",
                "Interacted safely without any major alerts"
            ],
            "recommendation": "Try introducing some Biology topics next week to balance the Knowledge Tree."
        }

# Singleton instance
_parent_service_instance = None

def get_parent_service() -> ParentService:
    global _parent_service_instance
    if _parent_service_instance is None:
        _parent_service_instance = ParentService()
    return _parent_service_instance
