"""
============================================
EchoMind AI - Response Scrubber Service
Sprint 2: Socratic Compliance Validation (Lock 3)
============================================

This service validates that LLM responses follow Socratic principles:
- Detects direct answers
- Ensures responses end with questions
- Validates tone (encouraging, not condescending)
- Checks response length for age-appropriateness
- Auto-regenerates if validation fails

User Story: US-2.5 (Response Scrubber - Lock 3)
"""

import re
import logging
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class ResponseScrubber:
    """
    Validates and fixes LLM responses to ensure Socratic compliance
    """
    
    # Patterns that indicate direct answers (FORBIDDEN)
    DIRECT_ANSWER_PATTERNS = [
        r"the answer is\s+(.+)",
        r"it is\s+(\d+|[a-z]+)\s*\.?\s*$",
        r"^\d+\s*\.?\s*$",  # Just a number
        r"^[A-Z][a-z]+\s+is\s+(.+)\.$",  # Definition format
        r"the correct answer",
        r"the solution is",
        r"here'?s the answer",
        r"^yes,?\s+it'?s",
        r"^no,?\s+it'?s",
    ]
    
    # Imperative commands to avoid (too authoritative)
    IMPERATIVE_PATTERNS = [
        r"you must",
        r"you should",
        r"you need to",
        r"do this",
        r"calculate this",
        r"solve this",
    ]
    
    # Negative/discouraging words to avoid
    NEGATIVE_WORDS = [
        "wrong",
        "incorrect",
        "bad",
        "stupid",
        "dumb",
        "failure",
        "fail",
    ]
    
    # Encouraging words that should be present
    ENCOURAGING_WORDS = [
        "great",
        "interesting",
        "curious",
        "wonder",
        "explore",
        "think",
        "imagine",
        "nice",
        "good",
        "awesome",
    ]
    
    def __init__(self):
        """Initialize Response Scrubber"""
        self.compiled_direct_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.DIRECT_ANSWER_PATTERNS
        ]
        self.compiled_imperative_patterns = [
            re.compile(pattern, re.IGNORECASE) for pattern in self.IMPERATIVE_PATTERNS
        ]
        logger.info("✅ Response Scrubber initialized")
    
    def validate(self, response: str) -> Dict[str, Any]:
        """
        Validate if response follows Socratic principles
        
        Args:
            response: The LLM's response to validate
        
        Returns:
            Dictionary with:
                - is_valid: Boolean indicating if response passes
                - violations: List of violation types
                - score: Compliance score (0-100)
                - details: Detailed validation results
        """
        violations = []
        details = {}
        
        # Check 1: Direct answer detection
        has_direct_answer = self._check_direct_answer(response)
        details["has_direct_answer"] = has_direct_answer
        if has_direct_answer:
            violations.append("direct_answer")
        
        # Check 2: Must end with question mark
        ends_with_question = response.strip().endswith("?")
        details["ends_with_question"] = ends_with_question
        if not ends_with_question:
            violations.append("no_question_mark")
        
        # Check 3: Must contain at least one question
        question_count = response.count("?")
        details["question_count"] = question_count
        if question_count < 1:
            violations.append("no_questions")
        
        # Check 4: Check for imperative commands
        has_imperatives = self._check_imperatives(response)
        details["has_imperatives"] = has_imperatives
        if has_imperatives:
            violations.append("imperative_commands")
        
        # Check 5: Check tone (encouraging vs discouraging)
        tone_check = self._check_tone(response)
        details["tone"] = tone_check
        if tone_check["has_negative_words"]:
            violations.append("negative_tone")
        if not tone_check["has_encouraging_words"]:
            violations.append("lacks_encouragement")
        
        # Check 6: Length check (should be concise for children)
        length_check = self._check_length(response)
        details["length"] = length_check
        if not length_check["is_appropriate"]:
            violations.append("too_long")
        
        # Calculate compliance score
        max_score = 100
        deductions = {
            "direct_answer": 50,  # Critical violation
            "no_question_mark": 20,
            "no_questions": 30,
            "imperative_commands": 15,
            "negative_tone": 25,
            "lacks_encouragement": 10,
            "too_long": 10,
        }
        
        score = max_score
        for violation in violations:
            score -= deductions.get(violation, 10)
        score = max(0, score)  # Don't go below 0
        
        is_valid = score >= 70  # Pass threshold
        
        logger.info(
            f"🔍 Response validation | "
            f"valid={is_valid} | "
            f"score={score} | "
            f"violations={violations}"
        )
        
        return {
            "is_valid": is_valid,
            "violations": violations,
            "score": score,
            "details": details
        }
    
    def _check_direct_answer(self, response: str) -> bool:
        """Check if response contains a direct answer"""
        for pattern in self.compiled_direct_patterns:
            if pattern.search(response):
                logger.warning(f"⚠️ Direct answer detected: {pattern.pattern}")
                return True
        return False
    
    def _check_imperatives(self, response: str) -> bool:
        """Check if response contains imperative commands"""
        for pattern in self.compiled_imperative_patterns:
            if pattern.search(response):
                logger.warning(f"⚠️ Imperative command detected: {pattern.pattern}")
                return True
        return False
    
    def _check_tone(self, response: str) -> Dict[str, Any]:
        """Check if tone is encouraging and positive"""
        response_lower = response.lower()
        
        # Check for negative words
        has_negative = any(word in response_lower for word in self.NEGATIVE_WORDS)
        
        # Check for encouraging words
        has_encouraging = any(word in response_lower for word in self.ENCOURAGING_WORDS)
        
        return {
            "has_negative_words": has_negative,
            "has_encouraging_words": has_encouraging
        }
    
    def _check_length(self, response: str) -> Dict[str, Any]:
        """Check if response length is appropriate for children"""
        char_count = len(response)
        word_count = len(response.split())
        
        # Guidelines: 50-300 characters, 10-60 words
        is_appropriate = (50 <= char_count <= 300) and (10 <= word_count <= 60)
        
        return {
            "char_count": char_count,
            "word_count": word_count,
            "is_appropriate": is_appropriate,
            "too_short": char_count < 50,
            "too_long": char_count > 300
        }
    
    def scrub(
        self,
        response: str,
        max_retries: int = 2
    ) -> Dict[str, Any]:
        """
        Validate response and provide feedback for regeneration if needed
        
        Args:
            response: The LLM's response
            max_retries: Maximum number of regeneration attempts
        
        Returns:
            Dictionary with:
                - is_valid: Whether response passed validation
                - response: The original response (if valid)
                - validation: Validation details
                - should_regenerate: Whether to regenerate
                - regeneration_prompt: Prompt for fixing issues
        """
        validation = self.validate(response)
        
        if validation["is_valid"]:
            logger.info("✅ Response passed Socratic validation")
            return {
                "is_valid": True,
                "response": response,
                "validation": validation,
                "should_regenerate": False
            }
        
        # Response failed validation
        logger.warning(f"❌ Response failed validation | violations={validation['violations']}")
        
        # Build regeneration prompt
        regeneration_prompt = self._build_regeneration_prompt(response, validation)
        
        return {
            "is_valid": False,
            "response": response,
            "validation": validation,
            "should_regenerate": True,
            "regeneration_prompt": regeneration_prompt
        }
    
    def _build_regeneration_prompt(
        self,
        original_response: str,
        validation: Dict[str, Any]
    ) -> str:
        """
        Build a prompt to fix validation issues
        
        Args:
            original_response: The response that failed
            validation: Validation results
        
        Returns:
            Prompt for LLM to regenerate response
        """
        violations = validation["violations"]
        
        prompt = f"""
Your previous response failed Socratic validation. Please rewrite it.

ORIGINAL RESPONSE:
"{original_response}"

ISSUES DETECTED:
"""
        
        if "direct_answer" in violations:
            prompt += "- You gave a DIRECT ANSWER. NEVER do this! Always respond with questions.\n"
        
        if "no_question_mark" in violations or "no_questions" in violations:
            prompt += "- Your response must END with a question mark and contain at least one question.\n"
        
        if "imperative_commands" in violations:
            prompt += "- Avoid imperative commands like 'you must' or 'do this'. Be gentle and guiding.\n"
        
        if "negative_tone" in violations:
            prompt += "- Avoid negative words like 'wrong' or 'incorrect'. Be encouraging!\n"
        
        if "lacks_encouragement" in violations:
            prompt += "- Add encouraging words like 'great', 'interesting', 'curious', etc.\n"
        
        if "too_long" in violations:
            prompt += "- Keep it SHORT and concise (50-300 characters). Children have short attention spans.\n"
        
        prompt += """
REWRITE the response following these rules:
1. NEVER give direct answers
2. Always end with a question
3. Be encouraging and playful
4. Use simple, age-appropriate language
5. Keep it concise (2-3 sentences max)

REWRITTEN RESPONSE:
"""
        
        return prompt
    
    def get_fallback_response(self) -> str:
        """
        Get a safe fallback response when all retries fail
        
        Returns:
            A guaranteed Socratic-compliant response
        """
        fallback_responses = [
            "That's a great question! 🤔 What do you already know about this topic?",
            "Interesting! Let me think about how to help you explore this. What's the first thing that comes to your mind?",
            "Hmm, that's tricky! What's the EASIEST part of this question? Even a tiny clue helps!",
            "I love how you're thinking about this! What would happen if we started with something simpler?",
        ]
        
        import random
        return random.choice(fallback_responses)


# Singleton instance
_response_scrubber_instance: Optional[ResponseScrubber] = None


def get_response_scrubber() -> ResponseScrubber:
    """
    Get or create Response Scrubber singleton instance
    
    Returns:
        ResponseScrubber instance
    """
    global _response_scrubber_instance
    
    if _response_scrubber_instance is None:
        _response_scrubber_instance = ResponseScrubber()
    
    return _response_scrubber_instance
