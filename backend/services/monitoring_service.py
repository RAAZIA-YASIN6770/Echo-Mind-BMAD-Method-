"""
============================================
EchoMind AI - Monitoring Service
Epic 10: Production Monitoring
============================================

This service tracks:
1. System Health (CPU, RAM, Disk)
2. Application Metrics (Requests, Errors, Latency)
3. Simulated APM (New Relic/Datadog style)
4. Alert Triggers
"""

import time
import logging
import threading
from typing import Dict, Any, List
from datetime import datetime

logger = logging.getLogger(__name__)

class MonitoringService:
    \"\"\"
    Internal monitoring engine to track system health and performance
    \"\"\"
    
    def __init__(self):
        self.start_time = datetime.utcnow()
        self.metrics = {
            "total_requests": 0,
            "error_count": 0,
            "latency_history": [],
            "last_error": None,
            "active_users": 0
        }
        self.alert_thresholds = {
            "error_rate": 0.05, # 5%
            "latency_ms": 2000  # 2 seconds
        }
        self._lock = threading.Lock()

    def track_request(self, latency_ms: float, success: bool = True, error_msg: str = None):
        \"\"\"Record a request metric\"\"\"
        with self._lock:
            self.metrics["total_requests"] += 1
            self.metrics["latency_history"].append(latency_ms)
            
            # Keep only last 1000 latencies
            if len(self.metrics["latency_history"]) > 1000:
                self.metrics["latency_history"].pop(0)
                
            if not success:
                self.metrics["error_count"] += 1
                self.metrics["last_error"] = {
                    "msg": error_msg,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
                # Check for critical alerts
                error_rate = self.metrics["error_count"] / self.metrics["total_requests"]
                if error_rate > self.alert_thresholds["error_rate"]:
                    self._trigger_alert("CRITICAL_ERROR_RATE", f"Error rate reached {error_rate*100:.1f}%")

    def get_system_metrics(self) -> Dict[str, Any]:
        \"\"\"
        Return aggregate metrics for the monitoring dashboard
        \"\"\"
        uptime = datetime.utcnow() - self.start_time
        
        avg_latency = 0
        if self.metrics["latency_history"]:
            avg_latency = sum(self.metrics["latency_history"]) / len(self.metrics["latency_history"])
            
        return {
            "uptime_seconds": int(uptime.total_seconds()),
            "total_requests": self.metrics["total_requests"],
            "error_count": self.metrics["error_count"],
            "error_rate": f"{(self.metrics['error_count'] / max(1, self.metrics['total_requests'])) * 100:.2f}%",
            "avg_latency_ms": int(avg_latency),
            "status": "HEALTHY" if self.metrics["error_count"] < 10 else "DEGRADED",
            "active_users": self.metrics["active_users"],
            "memory_usage": "154MB", # Simulated
            "cpu_usage": "12%",      # Simulated
            "last_error": self.metrics["last_error"]
        }

    def _trigger_alert(self, alert_type: str, message: str):
        \"\"\"Simulate PagerDuty/Slack alert\"\"\"
        logger.critical(f"🔔 ALERT TRIGGERED [{alert_type}]: {message}")
        # In production, this would call PagerDuty API or AWS SNS

# Singleton
_monitor_instance = None

def get_monitor() -> MonitoringService:
    global _monitor_instance
    if _monitor_instance is None:
        _monitor_instance = MonitoringService()
    return _monitor_instance
