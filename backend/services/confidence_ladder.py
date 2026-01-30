"""
============================================
EchoMind AI - Confidence Ladder Service
Sprint 2: "I Don't Know" Handling
============================================

This service implements the Confidence Ladder system:
- Detects "I don't know" responses
- Tracks count per session
- Provides progressively more supportive guidance:
  1st: Simpler Socratic question
  2nd: Multiple choice options
  3rd: Curiosity Detour (fun fact)

User Story: US-2.6 (Confidence Ladder Implementation)
"""

import re
import logging
import random
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)


class ConfidenceLadder:
    """
    Handles "I don't know" responses with progressive support
    """
    
    # Patterns to detect "I don't know" variations
    IDK_PATTERNS = [
        r"i\s*don'?t\s*know",
        r"\bidk\b",
        r"no\s*idea",
        r"not\s*sure",
        r"don'?t\s*understand",
        r"i\s*have\s*no\s*clue",
        r"i'?m\s*lost",
        r"i\s*can'?t",
    ]
    
    def __init__(self):
        """Initialize Confidence Ladder service"""
        self.compiled_patterns = [re.compile(pattern, re.IGNORECASE) for pattern in self.IDK_PATTERNS]
        logger.info("✅ Confidence Ladder service initialized")
    
    def detect_idk(self, message: str) -> bool:
        """
        Detect if message contains "I don't know" variations
        
        Args:
            message: User's message
        
        Returns:
            True if "I don't know" detected
        """
        for pattern in self.compiled_patterns:
            if pattern.search(message):
                logger.info(f"🎯 'I don't know' detected: {message[:50]}...")
                return True
        return False
    
    def get_ladder_level(self, idk_count: int) -> str:
        """
        Determine which ladder level to use based on count
        
        Args:
            idk_count: Number of consecutive "I don't know" responses
        
        Returns:
            Ladder level: 'simpler_question', 'multiple_choice', or 'curiosity_detour'
        """
        if idk_count == 1:
            return "simpler_question"
        elif idk_count == 2:
            return "multiple_choice"
        else:  # 3 or more
            return "curiosity_detour"
    
    def build_simpler_question_prompt(
        self,
        original_question: str,
        category: str,
        grade_level: int
    ) -> str:
        """
        Build a prompt to generate a simpler Socratic question
        
        Args:
            original_question: The original question that was too hard
            category: Question category (math/science/etc)
            grade_level: Student grade level
        
        Returns:
            Prompt for LLM to generate simpler question
        """
        return f"""
The student said "I don't know" to this question: "{original_question}"

Generate a SIMPLER Socratic question that:
1. Breaks down the concept into a smaller, easier piece
2. Starts with the absolute basics
3. Is appropriate for Grade {grade_level}
4. Still follows the Socratic method (no direct answers!)
5. Is encouraging and supportive

Category: {category}

Respond with ONLY the simpler question, nothing else.
"""
    
    def build_multiple_choice_prompt(
        self,
        original_question: str,
        category: str,
        grade_level: int
    ) -> str:
        """
        Build a prompt to generate multiple choice options
        
        Args:
            original_question: The original question
            category: Question category
            grade_level: Student grade level
        
        Returns:
            Prompt for LLM to generate multiple choice
        """
        return f"""
The student said "I don't know" TWICE. Now provide multiple choice support.

Original question: "{original_question}"

Generate a friendly multiple choice question with 3 options:
- Option A: Plausible but incorrect
- Option B: Correct answer
- Option C: Plausible but incorrect (or slightly humorous)

Make it appropriate for Grade {grade_level} and category: {category}

Format your response EXACTLY like this:
No worries! Let me give you 3 choices, and you pick the one that feels right:

A) [first option]
B) [second option]
C) [third option]

Which one makes the most sense to you? 🤔
"""
    
    def generate_curiosity_detour(
        self,
        category: str,
        original_question: str
    ) -> str:
        """
        Generate a "Curiosity Detour" - a fun fact to re-engage the student
        
        Args:
            category: Question category
            original_question: The original question (for context)
        
        Returns:
            Curiosity detour message
        """
        # Fun facts by category
        fun_facts = {
            "math": [
                "Did you know ancient Egyptians used fractions to divide bread? They only used unit fractions like 1/2, 1/3, 1/4!",
                "Fun fact: The number zero wasn't invented until around 500 AD in India! Before that, people had no way to write 'nothing'.",
                "Whoa! A googol is a 1 followed by 100 zeros. That's more than all the atoms in the universe!",
                "Cool fact: Honeybees are amazing mathematicians! They use hexagons for their honeycombs because it's the most efficient shape.",
            ],
            "science": [
                "Fun fact: Octopuses have THREE hearts! Two pump blood to the gills, and one pumps it to the rest of the body.",
                "Did you know that a day on Venus is longer than a year on Venus? It takes 243 Earth days to rotate once!",
                "Whoa! Bananas are slightly radioactive because they contain potassium. But don't worry, you'd need to eat 10 million bananas to get radiation poisoning!",
                "Cool fact: Your brain uses about 20% of your body's energy, even though it's only 2% of your body weight!",
            ],
            "logic": [
                "Fun fact: The ancient Greek philosopher Socrates never wrote anything down! Everything we know about him comes from his students.",
                "Did you know that chess has more possible games than there are atoms in the observable universe?",
                "Whoa! Sherlock Holmes, the famous detective, was based on a real doctor named Joseph Bell who taught Arthur Conan Doyle.",
            ],
            "language": [
                "Fun fact: The word 'alphabet' comes from the first two letters of the Greek alphabet: alpha and beta!",
                "Did you know that 'bookkeeper' is the only English word with three consecutive double letters?",
                "Cool fact: Shakespeare invented over 1,700 words we still use today, like 'eyeball', 'bedroom', and 'lonely'!",
            ],
            "general": [
                "Fun fact: Honey never spoils! Archaeologists found 3,000-year-old honey in Egyptian tombs that was still edible.",
                "Did you know that a group of flamingos is called a 'flamboyance'? How perfect is that!",
                "Whoa! The Eiffel Tower can grow up to 6 inches taller in summer due to thermal expansion of the metal!",
            ]
        }
        
        # Get facts for category, fallback to general
        facts = fun_facts.get(category, fun_facts["general"])
        fun_fact = random.choice(facts)
        
        return f"""
I can see this is tricky! Let's take a quick break from this. 🌱

{fun_fact}

Want to try a different topic, or should we come back to this question later? Sometimes our brains need a little break!
"""
    
    def handle_idk(
        self,
        message: str,
        idk_count: int,
        original_question: str,
        category: str,
        grade_level: int
    ) -> Dict[str, Any]:
        """
        Handle "I don't know" response based on ladder level
        
        Args:
            message: User's message
            idk_count: Current count of consecutive "I don't know" responses
            original_question: The question they're struggling with
            category: Question category
            grade_level: Student grade level
        
        Returns:
            Dictionary with:
                - ladder_level: Which level was triggered
                - prompt: Prompt for LLM (if needed)
                - direct_response: Direct response (for curiosity detour)
                - should_call_llm: Whether to call LLM or use direct response
        """
        if not self.detect_idk(message):
            return {
                "ladder_triggered": False,
                "ladder_level": None
            }
        
        ladder_level = self.get_ladder_level(idk_count)
        
        logger.info(f"🪜 Confidence Ladder triggered | level={ladder_level} | count={idk_count}")
        
        if ladder_level == "simpler_question":
            # Level 1: Generate simpler Socratic question
            return {
                "ladder_triggered": True,
                "ladder_level": "simpler_question",
                "prompt": self.build_simpler_question_prompt(original_question, category, grade_level),
                "should_call_llm": True,
                "prefix": "That's totally okay! 🌱 Let's start small. "
            }
        
        elif ladder_level == "multiple_choice":
            # Level 2: Generate multiple choice
            return {
                "ladder_triggered": True,
                "ladder_level": "multiple_choice",
                "prompt": self.build_multiple_choice_prompt(original_question, category, grade_level),
                "should_call_llm": True,
                "prefix": ""  # Prefix is included in the prompt
            }
        
        else:  # curiosity_detour
            # Level 3: Provide fun fact and suggest break
            return {
                "ladder_triggered": True,
                "ladder_level": "curiosity_detour",
                "direct_response": self.generate_curiosity_detour(category, original_question),
                "should_call_llm": False,
                "metadata": {
                    "needs_scaffolding": True,
                    "suggest_topic_change": True
                }
            }


# Singleton instance
_confidence_ladder_instance: Optional[ConfidenceLadder] = None


def get_confidence_ladder() -> ConfidenceLadder:
    """
    Get or create Confidence Ladder singleton instance
    
    Returns:
        ConfidenceLadder instance
    """
    global _confidence_ladder_instance
    
    if _confidence_ladder_instance is None:
        _confidence_ladder_instance = ConfidenceLadder()
    
    return _confidence_ladder_instance
