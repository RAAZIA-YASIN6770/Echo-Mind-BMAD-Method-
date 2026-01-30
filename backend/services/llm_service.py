"""
============================================
EchoMind AI - LLM Service
Sprint 2: OpenAI GPT-4o Integration
============================================

This service handles all interactions with the OpenAI API:
- Loads and applies the Master Socratic Prompt
- Manages API calls with retry logic
- Tracks token usage and costs
- Handles errors gracefully

User Story: US-2.4 (LLM API Wrapper)
"""

import os
import logging
import time
from typing import Dict, Any, Optional, List
from pathlib import Path
import openai
from openai import OpenAI, OpenAIError, RateLimitError, APITimeoutError
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

logger = logging.getLogger(__name__)


class LLMService:
    """
    OpenAI GPT-4o Service with Master Socratic Prompt Integration
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize LLM Service
        
        Args:
            api_key: OpenAI API key (defaults to environment variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY environment variable.")
        
        self.client = OpenAI(api_key=self.api_key)
        self.master_prompt = self._load_master_prompt()
        
        # Model configuration
        self.default_model = "gpt-4o"
        self.fallback_model = "gpt-3.5-turbo"
        
        # API parameters
        self.temperature = 0.7  # Balance creativity and consistency
        self.max_tokens = 150   # Keep responses concise for children
        self.top_p = 0.9
        
        # Cost tracking (per 1K tokens)
        self.cost_per_1k_tokens = {
            "gpt-4o": 0.005,  # GPT-4o pricing
            "gpt-4": 0.03,
            "gpt-3.5-turbo": 0.002
        }
        
        logger.info(f"✅ LLM Service initialized with model: {self.default_model}")
    
    def _load_master_prompt(self) -> str:
        """
        Load the Master Socratic Prompt from file
        
        Returns:
            Master prompt content as string
        """
        try:
            # Navigate from backend/services/ to ai-prompts/
            prompt_path = Path(__file__).parent.parent.parent / "ai-prompts" / "master-socratic-prompt.md"
            
            if not prompt_path.exists():
                logger.error(f"Master Socratic Prompt not found at: {prompt_path}")
                return self._get_fallback_prompt()
            
            with open(prompt_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            logger.info(f"✅ Master Socratic Prompt loaded ({len(content)} characters)")
            return content
        
        except Exception as e:
            logger.error(f"Error loading Master Socratic Prompt: {e}")
            return self._get_fallback_prompt()
    
    def _get_fallback_prompt(self) -> str:
        """Fallback prompt if master prompt file is not found"""
        return """
You are Eco-Mind, a Socratic AI tutor for children aged 8-13.

CORE RULES:
1. NEVER give direct answers
2. Always respond with guiding questions
3. Be encouraging and playful
4. Use age-appropriate language
5. Celebrate effort over correctness

When a child asks a question, respond with:
- A simpler guiding question
- A visual analogy
- A real-world example

If they say "I don't know", provide progressively more support.
"""
    
    def build_prompt(
        self,
        user_message: str,
        grade_level: int = 5,
        mastery_level: str = "exposure",
        conversation_history: Optional[List[Dict[str, str]]] = None,
        category: str = "general",
        emotional_state: str = "engaged"
    ) -> List[Dict[str, str]]:
        """
        Build the complete prompt with context injection
        
        Args:
            user_message: The child's question/message
            grade_level: Student grade level (3-7)
            mastery_level: Current mastery (exposure/understanding/mastery)
            conversation_history: Last 5 Q&A pairs
            category: Question category (math/science/logic/language/general)
            emotional_state: Detected emotional state
        
        Returns:
            List of message dictionaries for OpenAI API
        """
        # Build context string
        context = f"""
CURRENT CONTEXT:
- Student Grade Level: Grade {grade_level}
- Mastery Level: {mastery_level}
- Topic Category: {category}
- Emotional State: {emotional_state}
"""
        
        # Add conversation history if available
        if conversation_history and len(conversation_history) > 0:
            context += "\nRECENT CONVERSATION:\n"
            for i, exchange in enumerate(conversation_history[-5:], 1):
                context += f"{i}. Student: {exchange.get('question', '')}\n"
                context += f"   You: {exchange.get('response', '')}\n"
        
        context += f"\nCURRENT STUDENT MESSAGE: {user_message}\n"
        
        # Build messages array
        messages = [
            {
                "role": "system",
                "content": self.master_prompt + "\n\n" + context
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
        
        return messages
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((RateLimitError, APITimeoutError))
    )
    def generate_response(
        self,
        user_message: str,
        grade_level: int = 5,
        mastery_level: str = "exposure",
        conversation_history: Optional[List[Dict[str, str]]] = None,
        category: str = "general",
        complexity: str = "moderate",
        emotional_state: str = "engaged"
    ) -> Dict[str, Any]:
        """
        Generate a Socratic response using OpenAI API
        
        Args:
            user_message: The child's question/message
            grade_level: Student grade level (3-7)
            mastery_level: Current mastery level
            conversation_history: Recent conversation context
            category: Question category
            complexity: Question complexity (simple/moderate/complex)
            emotional_state: Detected emotional state
        
        Returns:
            Dictionary containing:
                - response: The AI's Socratic response
                - model_used: Which model was used
                - tokens_used: Total tokens consumed
                - cost: Estimated cost in USD
                - latency_ms: Response time in milliseconds
        """
        start_time = time.time()
        
        try:
            # Select model based on complexity
            model = self._select_model(complexity)
            
            # Build prompt
            messages = self.build_prompt(
                user_message=user_message,
                grade_level=grade_level,
                mastery_level=mastery_level,
                conversation_history=conversation_history,
                category=category,
                emotional_state=emotional_state
            )
            
            logger.info(f"🤖 Calling OpenAI API | model={model} | complexity={complexity}")
            
            # Call OpenAI API
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p
            )
            
            # Extract response
            ai_response = response.choices[0].message.content.strip()
            tokens_used = response.usage.total_tokens
            
            # Calculate cost
            cost = self._calculate_cost(tokens_used, model)
            
            # Calculate latency
            latency_ms = int((time.time() - start_time) * 1000)
            
            logger.info(
                f"✅ OpenAI response received | "
                f"tokens={tokens_used} | "
                f"cost=${cost:.4f} | "
                f"latency={latency_ms}ms"
            )
            
            return {
                "response": ai_response,
                "model_used": model,
                "tokens_used": tokens_used,
                "cost": cost,
                "latency_ms": latency_ms,
                "success": True
            }
        
        except RateLimitError as e:
            logger.warning(f"⚠️ Rate limit hit, retrying... {e}")
            raise  # Will be retried by @retry decorator
        
        except APITimeoutError as e:
            logger.warning(f"⚠️ API timeout, retrying... {e}")
            raise  # Will be retried by @retry decorator
        
        except OpenAIError as e:
            logger.error(f"❌ OpenAI API error: {e}")
            return self._get_fallback_response(str(e))
        
        except Exception as e:
            logger.error(f"❌ Unexpected error in LLM service: {e}", exc_info=True)
            return self._get_fallback_response(str(e))
    
    def _select_model(self, complexity: str) -> str:
        """
        Select appropriate model based on question complexity
        
        Args:
            complexity: Question complexity (simple/moderate/complex)
        
        Returns:
            Model name to use
        """
        if complexity == "simple":
            return self.fallback_model  # Use cheaper model for simple questions
        else:
            return self.default_model  # Use GPT-4o for moderate/complex
    
    def _calculate_cost(self, tokens: int, model: str) -> float:
        """
        Calculate estimated cost for API call
        
        Args:
            tokens: Total tokens used
            model: Model name
        
        Returns:
            Cost in USD
        """
        cost_per_1k = self.cost_per_1k_tokens.get(model, 0.005)
        return (tokens / 1000) * cost_per_1k
    
    def _get_fallback_response(self, error_msg: str) -> Dict[str, Any]:
        """
        Return a canned Socratic response when API fails
        
        Args:
            error_msg: Error message for logging
        
        Returns:
            Fallback response dictionary
        """
        logger.error(f"Using fallback response due to: {error_msg}")
        
        return {
            "response": (
                "That's a great question! 🤔 Let me think about how to help you explore this. "
                "What do you already know about this topic? Even a small idea can be a great starting point!"
            ),
            "model_used": "fallback",
            "tokens_used": 0,
            "cost": 0.0,
            "latency_ms": 0,
            "success": False,
            "error": error_msg
        }


# Singleton instance
_llm_service_instance: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """
    Get or create LLM service singleton instance
    
    Returns:
        LLMService instance
    """
    global _llm_service_instance
    
    if _llm_service_instance is None:
        _llm_service_instance = LLMService()
    
    return _llm_service_instance
