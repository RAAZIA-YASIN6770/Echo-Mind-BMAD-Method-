"""
============================================
EchoMind AI - Chat API
Epic 3: Triple-Lock Safety System Integration
============================================

This module handles the chat message endpoint and applies the Triple-Lock Safety System:
1. Lock 1: Security Middleware (Network level - simulated)
2. Lock 2: Safety Filter (PII scrubbing, jailbreak detection)
3. Lock 3: Response Scrubber (Socratic validation)
"""

from flask import Blueprint, request, jsonify
import logging
import sys
import os
import time

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from safety_filter import SafetyFilter
from middleware.pii_scrubber import scrub_pii
from services.response_scrubber import get_response_scrubber
from socratic_engine import get_socratic_engine

logger = logging.getLogger(__name__)

# Create Blueprint
chat_bp = Blueprint('chat', __name__)

# Initialize Safety Engine (Lock 2)
safety_filter = SafetyFilter()

@chat_bp.route('/api/chat/message', methods=['POST'])
def handle_chat_message():
    \"\"\"
    Handle incoming chat messages with Triple-Lock Safety
    \"\"\"
    start_time = time.time()
    
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({"success": False, "error": "Missing message"}), 400
        
        user_id = data.get('user_id', 'anonymous')
        session_id = data.get('session_id', 'default')
        user_input = data.get('message', '')
        grade_level = data.get('grade_level', 5)
        
        # --------------------------------------------------------------------
        # LOCK 2: Safety Filter (Input Validation & Scrubbing)
        # --------------------------------------------------------------------
        
        # 2a. Jailbreak & Intent Detection
        safety_result = safety_filter.analyze_input(user_input, user_id, session_id)
        
        if not safety_result['is_safe']:
            logger.warning(f"⚠️ Lock 2 Triggered (Safety Filter) | user={user_id} | violations={safety_result['violations']}")
            
            # If it's a high-severity violation (like jailbreak), return a firm response
            if 'prompt_injection' in safety_result['violations']:
                return jsonify({
                    "success": True,
                    "response": safety_result['recommended_response'],
                    "metadata": {
                        "safety_lock": 2,
                        "violation": "jailbreak_attempt",
                        "passed": False
                    }
                }), 200 # Return 200 so UI can show the message
            
            # For other violations, use the recommended response
            return jsonify({
                "success": True,
                "response": safety_result['recommended_response'],
                "metadata": {
                    "safety_lock": 2,
                    "violation": safety_result['violations'][0],
                    "passed": False
                }
            }), 200

        # 2b. Zero-Knowledge PII Scrubbing
        # We use the standalone scrub_pii function to ensure OpenAI never sees real names/emails
        scrub_result = scrub_pii(user_input)
        clean_input = scrub_result['scrubbed_text']
        pii_detected = scrub_result['pii_detected']
        
        if pii_detected:
            logger.info(f"🛡️ Lock 2 (PII Scrubber) | user={user_id} | Removed: {scrub_result['detections']}")

        # --------------------------------------------------------------------
        # PROCESSING: Socratic Engine (The Brain)
        # --------------------------------------------------------------------
        
        engine = get_socratic_engine()
        engine_result = engine.process_message(
            user_id=user_id,
            session_id=session_id,
            message=clean_input,
            grade_level=grade_level,
            pii_detected=pii_detected
        )
        
        ai_response = engine_result['response']['message']
        
        # --------------------------------------------------------------------
        # LOCK 3: Response Scrubber (Output Validation)
        # --------------------------------------------------------------------
        
        scrubber = get_response_scrubber()
        scrub_validation = scrubber.validate(ai_response)
        
        final_response = ai_response
        lock_3_triggered = False
        
        if not scrub_validation['is_valid']:
            logger.warning(f"🛡️ Lock 3 Triggered (Response Scrubber) | user={user_id} | score={scrub_validation['score']}")
            # In a real scenario, we might retry the LLM call here.
            # For now, we use the scrubber's suggested changes or a fallback
            lock_3_triggered = True
            # The SocraticEngine already does one layer of scrubbing, but this is the final check
            if scrub_validation['score'] < 50:
                final_response = "That's a great question! What do you think might be the first step in solving this? 🤔"

        # --------------------------------------------------------------------
        # RESPONSE BUILDING
        # --------------------------------------------------------------------
        
        latency = (time.time() - start_time) * 1000
        
        return jsonify({
            "success": True,
            "response": final_response,
            "category": engine_result.get('category', 'general'),
            "metadata": {
                "latency_ms": int(latency),
                "pii_detected": pii_detected,
                "lock_2_passed": True,
                "lock_3_passed": not lock_3_triggered,
                "lock_3_score": scrub_validation['score'],
                "tokens_used": engine_result.get('metadata', {}).get('tokens_used', 0)
            },
            "events": engine_result.get('events', {})
        })

    except Exception as e:
        logger.error(f"❌ Error in chat endpoint: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "error": "I'm having a little trouble thinking right now. Can we try again in a moment? 🌱",
            "details": str(e)
        }), 500
