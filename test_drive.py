"""
============================================
EchoMind AI - Interactive Test Drive Script
============================================

This script allows you to test the EchoMind AI system in real-time:
- Tests LLM Service in Mock Mode (no API key required)
- Tests Confidence Ladder ("I don't know" handling)
- Tests PII Scrubber (detects and removes sensitive info)
- Interactive terminal interface

Usage:
    python test_drive.py
    
Then type questions and see how the system responds!
"""

import sys
import os

# Fix Windows encoding issues
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from services.llm_service import LLMService
from services.confidence_ladder import ConfidenceLadder
from middleware.pii_scrubber import PIIScrubber
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(message)s'
)

class EchoMindTestDrive:
    """Interactive test drive for EchoMind AI"""
    
    def __init__(self):
        """Initialize all services in Mock Mode"""
        print("\n" + "="*60)
        print("🌱 EchoMind AI - Interactive Test Drive")
        print("="*60)
        print("\nInitializing services...")
        
        # Initialize services
        self.llm_service = LLMService()  # Will auto-enable Mock Mode if no API key
        self.confidence_ladder = ConfidenceLadder()
        self.pii_scrubber = PIIScrubber()
        
        # Session state
        self.idk_count = 0
        self.last_question = ""
        self.conversation_history = []
        
        print("\n✅ All services initialized!")
        print(f"🎭 Mock Mode: {'ENABLED' if self.llm_service.mock_mode else 'DISABLED'}")
        print("\n" + "-"*60)
    
    def print_help(self):
        """Print help information"""
        print("\n📚 COMMANDS:")
        print("  - Type any question to get a Socratic response")
        print("  - Type 'I don't know' to test the Confidence Ladder")
        print("  - Include PII (email, phone, name) to test the scrubber")
        print("  - Type 'help' to see this message")
        print("  - Type 'stats' to see session statistics")
        print("  - Type 'reset' to reset the session")
        print("  - Type 'quit' or 'exit' to quit")
        print("\n💡 TIP: Try different categories by mentioning:")
        print("   - Math: numbers, equations, calculations")
        print("   - Science: experiments, nature, biology")
        print("   - Logic: puzzles, reasoning, problems")
        print("   - Language: words, grammar, stories")
        print("-"*60)
    
    def detect_category(self, message: str) -> str:
        """Detect question category from message"""
        message_lower = message.lower()
        
        # Math keywords
        if any(word in message_lower for word in ['math', 'number', 'add', 'subtract', 'multiply', 'divide', 'equation', 'calculate', 'fraction', 'percent']):
            return "math"
        
        # Science keywords
        if any(word in message_lower for word in ['science', 'experiment', 'plant', 'animal', 'water', 'energy', 'gravity', 'space', 'earth', 'biology', 'chemistry', 'physics']):
            return "science"
        
        # Logic keywords
        if any(word in message_lower for word in ['logic', 'puzzle', 'riddle', 'solve', 'think', 'reason', 'problem', 'pattern']):
            return "logic"
        
        # Language keywords
        if any(word in message_lower for word in ['language', 'word', 'sentence', 'grammar', 'story', 'write', 'read', 'book', 'spell']):
            return "language"
        
        return "general"
    
    def print_stats(self):
        """Print session statistics"""
        print("\n📊 SESSION STATISTICS:")
        print(f"  - Messages sent: {len(self.conversation_history)}")
        print(f"  - 'I don't know' count: {self.idk_count}")
        print(f"  - Mock Mode: {'ON' if self.llm_service.mock_mode else 'OFF'}")
        print("-"*60)
    
    def reset_session(self):
        """Reset session state"""
        self.idk_count = 0
        self.last_question = ""
        self.conversation_history = []
        print("\n🔄 Session reset!")
        print("-"*60)
    
    def process_message(self, user_message: str):
        """Process a user message through the full pipeline"""
        
        # Step 1: PII Scrubbing
        print("\n🔒 Step 1: PII Scrubbing...")
        scrub_result = self.pii_scrubber.scrub_all(user_message)
        
        if scrub_result['pii_detected']:
            print(f"   ⚠️  PII DETECTED! Removed: {scrub_result['detections']}")
            print(f"   Original: {user_message}")
            print(f"   Scrubbed: {scrub_result['scrubbed_text']}")
            user_message = scrub_result['scrubbed_text']
        else:
            print("   ✅ No PII detected")
        
        # Step 2: Confidence Ladder Check
        print("\n🪜 Step 2: Confidence Ladder Check...")
        is_idk = self.confidence_ladder.detect_idk(user_message)
        
        if is_idk:
            self.idk_count += 1
            print(f"   🎯 'I don't know' detected! (Count: {self.idk_count})")
            
            ladder_result = self.confidence_ladder.handle_idk(
                message=user_message,
                idk_count=self.idk_count,
                original_question=self.last_question or "the previous question",
                category=self.detect_category(self.last_question),
                grade_level=5
            )
            
            print(f"   📊 Ladder Level: {ladder_result['ladder_level']}")
            
            # If curiosity detour, use direct response
            if not ladder_result['should_call_llm']:
                response_text = ladder_result['direct_response']
                print("\n🤖 EchoMind Response:")
                print(f"   {response_text}")
                print("-"*60)
                return
        else:
            self.idk_count = 0  # Reset count
            self.last_question = user_message
            print("   ✅ Normal question detected")
        
        # Step 3: Detect Category
        category = self.detect_category(user_message)
        print(f"\n🏷️  Step 3: Category Detection...")
        print(f"   Category: {category}")
        
        # Step 4: Generate Response
        print(f"\n🤖 Step 4: Generating Socratic Response...")
        response = self.llm_service.generate_response(
            user_message=user_message,
            category=category,
            grade_level=5,
            mastery_level="exposure",
            conversation_history=self.conversation_history[-5:]  # Last 5 exchanges
        )
        
        # Display response
        print(f"\n{'='*60}")
        print("🌱 EchoMind Response:")
        print(f"{'='*60}")
        print(f"\n{response['response']}\n")
        print(f"{'='*60}")
        print(f"📊 Metadata:")
        print(f"   Model: {response['model_used']}")
        print(f"   Tokens: {response['tokens_used']}")
        print(f"   Cost: ${response['cost']:.4f}")
        print(f"   Latency: {response['latency_ms']}ms")
        print(f"   Category: {category}")
        print("-"*60)
        
        # Store in conversation history
        self.conversation_history.append({
            'question': user_message,
            'response': response['response']
        })
    
    def run(self):
        """Run the interactive test drive"""
        self.print_help()
        
        print("\n🚀 Ready! Type your first question...\n")
        
        while True:
            try:
                # Get user input
                user_input = input("You: ").strip()
                
                # Handle empty input
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.lower() in ['quit', 'exit', 'q']:
                    print("\n👋 Thanks for testing EchoMind AI! Goodbye!")
                    break
                
                elif user_input.lower() == 'help':
                    self.print_help()
                    continue
                
                elif user_input.lower() == 'stats':
                    self.print_stats()
                    continue
                
                elif user_input.lower() == 'reset':
                    self.reset_session()
                    continue
                
                # Process the message
                self.process_message(user_input)
                
            except KeyboardInterrupt:
                print("\n\n👋 Interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                import traceback
                traceback.print_exc()


if __name__ == "__main__":
    # Run the test drive
    test_drive = EchoMindTestDrive()
    test_drive.run()
