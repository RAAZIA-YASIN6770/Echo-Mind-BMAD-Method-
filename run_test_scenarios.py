"""
============================================
EchoMind AI - Automated Test Scenarios
============================================

Runs 3 specific test scenarios to demonstrate:
- Scenario A: PII Scrubbing (Safety)
- Scenario B: Confidence Ladder (Struggle handling)
- Scenario C: Normal Socratic Response (Success)
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


class ScenarioTester:
    """Automated scenario testing for EchoMind AI"""
    
    def __init__(self):
        """Initialize all services"""
        print("\n" + "="*70)
        print("🧪 EchoMind AI - Automated Test Scenarios")
        print("="*70)
        print("\nInitializing services...")
        
        self.llm_service = LLMService()
        self.confidence_ladder = ConfidenceLadder()
        self.pii_scrubber = PIIScrubber()
        
        self.idk_count = 0
        self.last_question = ""
        
        print(f"\n✅ Services initialized!")
        print(f"🎭 Mock Mode: {'ENABLED' if self.llm_service.mock_mode else 'DISABLED'}")
        print("="*70)
    
    def detect_category(self, message: str) -> str:
        """Detect question category"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ['math', 'number', 'add', 'subtract', 'multiply', 'divide', '+', '-', '*', '/']):
            return "math"
        if any(word in message_lower for word in ['science', 'plant', 'photosynthesis', 'animal', 'biology']):
            return "science"
        if any(word in message_lower for word in ['logic', 'puzzle', 'riddle']):
            return "logic"
        if any(word in message_lower for word in ['language', 'word', 'grammar']):
            return "language"
        
        return "general"
    
    def run_scenario(self, scenario_name: str, user_message: str, description: str):
        """Run a single test scenario"""
        print(f"\n{'='*70}")
        print(f"📋 SCENARIO: {scenario_name}")
        print(f"📝 Description: {description}")
        print(f"{'='*70}")
        print(f"\n💬 User Input: \"{user_message}\"")
        print("\n" + "-"*70)
        
        # Step 1: PII Scrubbing
        print("\n🔒 STEP 1: PII Scrubbing")
        scrub_result = self.pii_scrubber.scrub_all(user_message)
        
        if scrub_result['pii_detected']:
            print(f"   ⚠️  PII DETECTED!")
            print(f"   Types found: {scrub_result['detections']}")
            print(f"   Original: {user_message}")
            print(f"   Scrubbed: {scrub_result['scrubbed_text']}")
            user_message = scrub_result['scrubbed_text']
        else:
            print("   ✅ No PII detected - message is safe")
        
        # Step 2: Confidence Ladder
        print("\n🪜 STEP 2: Confidence Ladder Check")
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
            
            if not ladder_result['should_call_llm']:
                print("\n🤖 STEP 3: Direct Response (No LLM needed)")
                print(f"\n{'='*70}")
                print("🌱 EchoMind Response:")
                print(f"{'='*70}")
                print(f"\n{ladder_result['direct_response']}\n")
                print(f"{'='*70}")
                return
        else:
            self.idk_count = 0
            self.last_question = user_message
            print("   ✅ Normal question detected")
        
        # Step 3: Category Detection
        category = self.detect_category(user_message)
        print(f"\n🏷️  STEP 3: Category Detection")
        print(f"   Detected category: {category}")
        
        # Step 4: LLM Response
        print(f"\n🤖 STEP 4: Generating Socratic Response")
        response = self.llm_service.generate_response(
            user_message=user_message,
            category=category,
            grade_level=5,
            mastery_level="exposure",
            conversation_history=[]
        )
        
        print(f"\n{'='*70}")
        print("🌱 EchoMind Response:")
        print(f"{'='*70}")
        print(f"\n{response['response']}\n")
        print(f"{'='*70}")
        print(f"📊 Response Metadata:")
        print(f"   Model: {response['model_used']}")
        print(f"   Tokens: {response['tokens_used']}")
        print(f"   Cost: ${response['cost']:.4f}")
        print(f"   Latency: {response['latency_ms']}ms")
        print(f"   Category: {category}")
        print(f"{'='*70}")
    
    def run_all_scenarios(self):
        """Run all three test scenarios"""
        
        # Scenario A: Safety (PII Scrubbing)
        self.run_scenario(
            scenario_name="A - Safety (PII Scrubbing)",
            user_message="My name is Ahmed and my phone is 0300-1234567. How do I solve 2+2?",
            description="Tests PII detection and scrubbing of name and phone number"
        )
        
        input("\n\n⏸️  Press ENTER to continue to Scenario B...")
        
        # Scenario B: Struggle (Confidence Ladder)
        # Reset for fresh scenario
        self.idk_count = 0
        self.last_question = "What is photosynthesis?"
        
        print("\n\n")
        self.run_scenario(
            scenario_name="B - Struggle (Confidence Ladder) - Attempt 1",
            user_message="I don't know",
            description="First 'I don't know' - should offer hint"
        )
        
        input("\n\n⏸️  Press ENTER for Attempt 2...")
        
        print("\n\n")
        self.run_scenario(
            scenario_name="B - Struggle (Confidence Ladder) - Attempt 2",
            user_message="I don't know",
            description="Second 'I don't know' - should simplify question"
        )
        
        input("\n\n⏸️  Press ENTER for Attempt 3...")
        
        print("\n\n")
        self.run_scenario(
            scenario_name="B - Struggle (Confidence Ladder) - Attempt 3",
            user_message="I don't know",
            description="Third 'I don't know' - should offer curiosity detour"
        )
        
        input("\n\n⏸️  Press ENTER to continue to Scenario C...")
        
        # Scenario C: Success (Normal Socratic Response)
        self.idk_count = 0
        
        print("\n\n")
        self.run_scenario(
            scenario_name="C - Success (Normal Socratic Response)",
            user_message="Photosynthesis is how plants make food using sun.",
            description="Tests normal Socratic questioning on correct answer"
        )
        
        print("\n\n" + "="*70)
        print("✅ All scenarios completed!")
        print("="*70)


if __name__ == "__main__":
    tester = ScenarioTester()
    tester.run_all_scenarios()
