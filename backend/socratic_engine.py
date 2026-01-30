"""
============================================
EchoMind AI - Socratic Engine (Sprint 2)
Sprint 2: Core Socratic Intelligence Integration
============================================

This module orchestrates all Socratic Intelligence services:
- LLM Service (OpenAI GPT-4o)
- Confidence Ladder ("I don't know" handling)
- Mastery Service (concept tracking)
- Response Scrubber (Socratic compliance)

This will be integrated into main.py
"""

import logging
import time
from typing import Dict, Any, Optional, List
from datetime import datetime

from services.llm_service import get_llm_service
from services.confidence_ladder import get_confidence_ladder
from services.mastery_service import get_mastery_service
from services.response_scrubber import get_response_scrubber

logger = logging.getLogger(__name__)


class SocraticEngine:
    """
    Main orchestrator for Socratic Intelligence
    """
    
    def __init__(self):
        """Initialize Socratic Engine with all services"""
        self.llm_service = get_llm_service()
        self.confidence_ladder = get_confidence_ladder()
        self.mastery_service = get_mastery_service()
        self.response_scrubber = get_response_scrubber()
        
        # Session state (in-memory for Sprint 2)
        self._session_state: Dict[str, Dict[str, Any]] = {}
        
        logger.info("✅ Socratic Engine initialized")
    
    def process_message(
        self,
        user_id: str,
        session_id: str,
        message: str,
        grade_level: int = 5,
        pii_detected: bool = False
    ) -> Dict[str, Any]:
        """
        Process a user message through the full Socratic pipeline
        
        Args:
            user_id: User UUID
            session_id: Session UUID
            message: User's message
            grade_level: Student grade level (3-7)
            pii_detected: Whether PII was detected by middleware
        
        Returns:
            Complete response dictionary
        """
        start_time = time.time()
        
        try:
            # Get or create session state
            session_state = self._get_session_state(session_id, user_id)
            
            # Step 1: Simple question classification (basic for Sprint 2)
            category = self._classify_question(message)
            logger.info(f"📊 Question classified | category={category}")
            
            # Step 2: Check for "I don't know" (Confidence Ladder)
            idk_detected = self.confidence_ladder.detect_idk(message)
            if idk_detected:
                session_state["idk_count"] = session_state.get("idk_count", 0) + 1
            else:
                # Reset counter if they're engaging
                session_state["idk_count"] = 0
            
            # Step 3: Get mastery level for the concept
            concept_name = self._extract_concept(message, category)
            mastery = self.mastery_service.get_mastery(user_id, concept_name)
            logger.info(
                f"📚 Mastery retrieved | "
                f"concept={concept_name} | "
                f"level={mastery['mastery_level']}"
            )
            
            # Step 4: Handle Confidence Ladder if triggered
            if idk_detected:
                ladder_result = self.confidence_ladder.handle_idk(
                    message=message,
                    idk_count=session_state["idk_count"],
                    original_question=session_state.get("last_question", message),
                    category=category,
                    grade_level=grade_level
                )
                
                if ladder_result["ladder_triggered"]:
                    logger.info(f"🪜 Confidence Ladder | level={ladder_result['ladder_level']}")
                    
                    # If curiosity detour, return direct response
                    if not ladder_result.get("should_call_llm", True):
                        return self._build_response(
                            response_text=ladder_result["direct_response"],
                            metadata={
                                "ladder_level": ladder_result["ladder_level"],
                                "category": category,
                                "mastery_level": mastery["mastery_level"],
                                "pii_detected": pii_detected,
                                "latency_ms": int((time.time() - start_time) * 1000)
                            }
                        )
                    
                    # Otherwise, use ladder prompt
                    user_message_for_llm = ladder_result.get("prompt", message)
                    response_prefix = ladder_result.get("prefix", "")
                else:
                    user_message_for_llm = message
                    response_prefix = ""
            else:
                user_message_for_llm = message
                response_prefix = ""
            
            # Step 5: Get conversation history
            conversation_history = session_state.get("history", [])
            
            # Step 6: Generate LLM response
            llm_result = self.llm_service.generate_response(
                user_message=user_message_for_llm,
                grade_level=grade_level,
                mastery_level=mastery["mastery_level"],
                conversation_history=conversation_history,
                category=category,
                complexity="moderate",  # Will be enhanced in future
                emotional_state="engaged"  # Will be detected in future
            )
            
            if not llm_result["success"]:
                logger.error("LLM service failed, using fallback")
                return self._build_fallback_response(pii_detected)
            
            raw_response = llm_result["response"]
            
            # Step 7: Scrub response for Socratic compliance
            scrub_result = self.response_scrubber.scrub(raw_response)
            
            if scrub_result["should_regenerate"]:
                logger.warning("⚠️ Response failed validation, regenerating...")
                
                # Try to regenerate once
                regen_result = self.llm_service.generate_response(
                    user_message=scrub_result["regeneration_prompt"],
                    grade_level=grade_level,
                    mastery_level=mastery["mastery_level"],
                    conversation_history=[],
                    category=category,
                    complexity="simple"
                )
                
                if regen_result["success"]:
                    # Re-validate
                    regen_scrub = self.response_scrubber.scrub(regen_result["response"])
                    if regen_scrub["is_valid"]:
                        final_response = regen_result["response"]
                    else:
                        # Use fallback after 2 failures
                        final_response = self.response_scrubber.get_fallback_response()
                else:
                    final_response = self.response_scrubber.get_fallback_response()
            else:
                final_response = raw_response
            
            # Add prefix if from Confidence Ladder
            if response_prefix:
                final_response = response_prefix + final_response
            
            # Step 8: Update session state
            session_state["history"].append({
                "question": message,
                "response": final_response,
                "timestamp": datetime.utcnow().isoformat()
            })
            
            # Keep only last 5 exchanges
            if len(session_state["history"]) > 5:
                session_state["history"] = session_state["history"][-5:]
            
            session_state["last_question"] = message
            session_state["message_count"] = session_state.get("message_count", 0) + 1
            
            # Step 9: Update mastery (simple scoring for Sprint 2)
            # In future, we'll analyze the quality of their response
            interaction_quality = 3  # Default moderate score
            self.mastery_service.update_mastery(
                user_id=user_id,
                concept_name=concept_name,
                interaction_quality=interaction_quality,
                demonstrated_understanding=False
            )
            
            # Step 10: Build final response
            latency_ms = int((time.time() - start_time) * 1000)
            
            return self._build_response(
                response_text=final_response,
                metadata={
                    "category": category,
                    "concept": concept_name,
                    "mastery_level": mastery["mastery_level"],
                    "idk_count": session_state["idk_count"],
                    "model_used": llm_result.get("model_used", "unknown"),
                    "tokens_used": llm_result.get("tokens_used", 0),
                    "cost": llm_result.get("cost", 0.0),
                    "pii_detected": pii_detected,
                    "validation_score": scrub_result["validation"]["score"],
                    "latency_ms": latency_ms
                }
            )
        
        except Exception as e:
            logger.error(f"❌ Error in Socratic Engine: {e}", exc_info=True)
            return self._build_fallback_response(pii_detected)
    
    def _get_session_state(self, session_id: str, user_id: str) -> Dict[str, Any]:
        """Get or create session state"""
        if session_id not in self._session_state:
            self._session_state[session_id] = {
                "user_id": user_id,
                "history": [],
                "idk_count": 0,
                "message_count": 0,
                "started_at": datetime.utcnow().isoformat()
            }
        return self._session_state[session_id]
    
    def _classify_question(self, message: str) -> str:
        """
        Simple question classification (will be enhanced in future)
        
        Args:
            message: User's message
        
        Returns:
            Category: math, science, logic, language, or general
        """
        message_lower = message.lower()
        
        # Math keywords
        if any(word in message_lower for word in [
            'add', 'subtract', 'multiply', 'divide', 'fraction', 'equation',
            'number', 'calculate', 'times', 'plus', 'minus', 'equal'
        ]):
            return "math"
        
        # Science keywords
        if any(word in message_lower for word in [
            'atom', 'cell', 'energy', 'force', 'photosynthesis', 'plant',
            'animal', 'planet', 'space', 'chemical', 'biology', 'physics'
        ]):
            return "science"
        
        # Logic keywords
        if any(word in message_lower for word in [
            'because', 'therefore', 'if', 'then', 'logic', 'reason', 'prove'
        ]):
            return "logic"
        
        # Language keywords
        if any(word in message_lower for word in [
            'word', 'sentence', 'grammar', 'spelling', 'meaning', 'definition',
            'synonym', 'antonym', 'verb', 'noun'
        ]):
            return "language"
        
        return "general"
    
    def _extract_concept(self, message: str, category: str) -> str:
        """
        Extract the main concept from the message
        
        Args:
            message: User's message
            category: Question category
        
        Returns:
            Concept name
        """
        # Simple extraction (will be enhanced with NLP in future)
        message_lower = message.lower()
        
        # Math concepts
        if category == "math":
            if 'multiply' in message_lower or 'times' in message_lower:
                return "multiplication"
            if 'divide' in message_lower:
                return "division"
            if 'add' in message_lower or 'plus' in message_lower:
                return "addition"
            if 'subtract' in message_lower or 'minus' in message_lower:
                return "subtraction"
            if 'fraction' in message_lower:
                return "fractions"
        
        # Science concepts
        if category == "science":
            if 'photosynthesis' in message_lower:
                return "photosynthesis"
            if 'cell' in message_lower:
                return "cells"
            if 'planet' in message_lower or 'space' in message_lower:
                return "astronomy"
        
        # Default: use category as concept
        return category
    
    def _build_response(
        self,
        response_text: str,
        metadata: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build the final response dictionary"""
        return {
            "response": {
                "message": response_text,
                "type": "socratic_question",
                "confidence": 0.9
            },
            "events": {
                "seed_drop": {
                    "triggered": False  # Will be implemented in future
                },
                "tree_update": {
                    "health_score": 50  # Will be calculated in future
                }
            },
            "metadata": {
                **metadata,
                "safety_passed": True,
                "sprint": "sprint_2_socratic_intelligence"
            }
        }
    
    def _build_fallback_response(self, pii_detected: bool) -> Dict[str, Any]:
        """Build a fallback response when errors occur"""
        return {
            "response": {
                "message": self.response_scrubber.get_fallback_response(),
                "type": "fallback",
                "confidence": 1.0
            },
            "events": {
                "seed_drop": {"triggered": False},
                "tree_update": {"health_score": 50}
            },
            "metadata": {
                "pii_detected": pii_detected,
                "safety_passed": True,
                "sprint": "sprint_2_fallback",
                "error": "Service unavailable"
            }
        }


# Singleton instance
_socratic_engine_instance: Optional['SocraticEngine'] = None


def get_socratic_engine() -> SocraticEngine:
    """
    Get or create Socratic Engine singleton instance
    
    Returns:
        SocraticEngine instance
    """
    global _socratic_engine_instance
    
    if _socratic_engine_instance is None:
        _socratic_engine_instance = SocraticEngine()
    
    return _socratic_engine_instance
