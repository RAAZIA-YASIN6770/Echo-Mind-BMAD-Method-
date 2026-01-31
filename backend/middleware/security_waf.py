"""
============================================
EchoMind AI - Security WAF Middleware (Lock 1)
Epic 3: Triple-Lock Safety System
============================================

This middleware simulates the AWS WAF (Network Layer) at the application level.
It provides:
1. Rate Limiting (Prevent DDoS/Abuse)
2. IP Blacklisting (Simulated)
3. Pattern-based Blocking (SQL Injection, XSS patterns)
4. Request Size Limiting
"""

import time
import logging
from flask import request, jsonify
from functools import wraps

logger = logging.getLogger(__name__)

# Simple in-memory rate limiting for local development
# Format: {ip: [timestamp1, timestamp2, ...]}
rate_limit_store = {}

# Configuration
LIMIT_PER_MINUTE = 60 # 1 request per second average
BLOCKED_IPS = {"192.168.1.99"} # Example blocked IP

# Malicious patterns (Simulated WAF rules)
MALICIOUS_PATTERNS = [
    "<script>", "javascript:", "eval(", 
    "UNION SELECT", "DROP TABLE", "OR 1=1",
    "../", "/etc/passwd", "cmd.exe"
]

class SecurityWAF:
    \"\"\"
    Simulated Web Application Firewall (Lock 1)
    \"\"\"
    
    @staticmethod
    def apply_lock(app):
        \"\"\"Apply Lock 1 to the Flask app\"\"\"
        
        @app.before_request
        def waf_gatekeeper():
            # 1. IP Check
            client_ip = request.remote_addr
            if client_ip in BLOCKED_IPS:
                logger.warning(f"🚫 Lock 1: Blocked IP attempt | {client_ip}")
                return jsonify({"error": "Access denied by security policy"}), 403
            
            # 2. Rate Limiting
            if not SecurityWAF._check_rate_limit(client_ip):
                logger.warning(f"🚫 Lock 1: Rate limit exceeded | {client_ip}")
                return jsonify({"error": "Too many requests. Please slow down. 🌱"}), 429
            
            # 3. Payload Inspection (Basic XSS/SQLi)
            if request.method in ["POST", "PUT"]:
                payload = request.get_data(as_text=True)
                if any(pattern in payload for pattern in MALICIOUS_PATTERNS):
                    logger.critical(f"🚨 Lock 1: Malicious pattern detected! | {client_ip}")
                    return jsonify({"error": "Security violation detected"}), 400
            
            # 4. Request Size Limit
            if request.content_length and request.content_length > 10 * 1024: # 10KB limit
                return jsonify({"error": "Request too large"}), 413

    @staticmethod
    def _check_rate_limit(ip):
        \"\"\"Simple sliding window rate limiter\"\"\"
        now = time.time()
        if ip not in rate_limit_store:
            rate_limit_store[ip] = []
        
        # Filter out timestamps older than 60 seconds
        rate_limit_store[ip] = [t for t in rate_limit_store[ip] if now - t < 60]
        
        if len(rate_limit_store[ip]) >= LIMIT_PER_MINUTE:
            return False
        
        rate_limit_store[ip].append(now)
        return True

def security_lock_required(f):
    \"\"\"Decorator version of the WAF for specific routes\"\"\"
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This could be used for even stricter checks
        return f(*args, **kwargs)
    return decorated_function
