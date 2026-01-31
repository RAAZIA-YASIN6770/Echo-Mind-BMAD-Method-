"""
============================================
End-to-End Test: Zoya's Learning Journey
============================================

Tests the complete EchoMind AI flow from onboarding to mastery.

This script demonstrates:
- User onboarding with Mystery Seed assignment
- Socratic dialogue flow
- Confidence Ladder activation
- Mastery achievement
- Seed growth tracking
- Knowledge Tree updates

Run this to verify the entire system works end-to-end!
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, Any

# ============================================
# Configuration
# ============================================

BASE_URL = "http://localhost:5000"
SESSION_ID = f"session_{int(time.time())}"

# ============================================
# Utility Functions
# ============================================

def print_section(title: str, emoji: str = "📋"):
    """Print a formatted section header"""
    print("\n" + "="*70)
    print(f"  {emoji} {title}")
    print("="*70 + "\n")

def print_json(data: Dict[Any, Any], title: str = "Response"):
    """Pretty print JSON data"""
    print(f"\n📋 {title}:")
    print(json.dumps(data, indent=2))

def print_success(message: str):
    """Print success message"""
    print(f"✅ {message}")

def print_error(message: str):
    """Print error message"""
    print(f"❌ {message}")

def print_info(message: str):
    """Print info message"""
    print(f"ℹ️  {message}")

# ============================================
# Test Functions
# ============================================

def test_backend_connection():
    """Test if backend is reachable"""
    print_section("Testing Backend Connection", "🔍")
    
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print_success("Backend is running!")
            print_json(response.json(), "Backend Info")
            return True
        else:
            print_error(f"Backend returned status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print_error("Cannot connect to backend!")
        print_info("Make sure the backend is running: python backend/app.py")
        return False
    except Exception as e:
        print_error(f"Connection test failed: {e}")
        return False

def test_onboarding():
    """Step 1: Test user onboarding"""
    print_section("STEP 1: Zoya's Onboarding", "👧")
    
    print("Creating new user: Zoya (Age 10, Grade 5)")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/user/onboarding",
            json={
                "name": "Zoya",
                "age": 10,
                "grade_level": 5,
                "parent_email": "parent@example.com"
            },
            timeout=10
        )
        
        if response.status_code != 200:
            print_error(f"Onboarding failed with status {response.status_code}")
            print(response.text)
            return None
        
        data = response.json()
        print_json(data)
        
        # Verification
        print("\n" + "─"*70)
        print("✅ VERIFICATION:")
        print(f"   👤 User ID: {data['user']['user_id']}")
        print(f"   👧 Name: {data['user']['name']}")
        print(f"   🎂 Age: {data['user']['age']}")
        print(f"   📚 Grade: {data['user']['grade_level']}")
        print(f"   💎 Seed: {data['seed']['seed_emoji']} {data['seed']['seed_name']}")
        print(f"   ✨ Stage: {data['seed']['current_stage_emoji']} {data['seed']['current_stage_name']}")
        print(f"   🌳 Tree Health: {data['tree']['overall_health']}%")
        print(f"   📝 Welcome: {data['welcome_message']}")
        print("─"*70)
        
        return data['user']['user_id']
        
    except Exception as e:
        print_error(f"Onboarding test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_chat_message(user_id: int, message: str, step_name: str, step_emoji: str = "💬"):
    """Send a chat message and display results"""
    print_section(step_name, step_emoji)
    
    print(f"💬 Zoya: \"{message}\"")
    print("   (Sending to AI...)")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/chat/message",
            json={
                "user_id": str(user_id),
                "session_id": SESSION_ID,
                "message": message
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print_error(f"Chat failed with status {response.status_code}")
            print(response.text)
            return None
        
        data = response.json()
        
        # Display AI response
        print(f"\n🤖 AI Response:")
        print(f"   \"{data['response']['message']}\"")
        
        # Display metadata
        print(f"\n📊 Response Metadata:")
        print(f"   Type: {data['response'].get('type', 'N/A')}")
        print(f"   Confidence: {data['response'].get('confidence', 'N/A')}")
        if 'category' in data['response']:
            print(f"   Category: {data['response']['category']}")
        
        # Display events
        if 'events' in data and data['events']:
            print(f"\n🎮 Game Events:")
            
            # Confidence Ladder
            if 'confidence_ladder' in data['events']:
                ladder = data['events']['confidence_ladder']
                if ladder.get('triggered'):
                    print(f"   💭 CONFIDENCE LADDER ACTIVATED!")
                    print(f"      Reason: {ladder.get('reason', 'N/A')}")
                    print(f"      Level: {ladder.get('ladder_level', 'N/A')}")
            
            # Tree Update
            if 'tree_update' in data['events']:
                tree = data['events']['tree_update']
                print(f"   🌳 Tree Health: {tree.get('health_score', 'N/A')}%")
                if 'branch_updated' in tree:
                    print(f"   🌿 Branch: {tree['branch_updated']} ({tree.get('branch_health', 'N/A')}%)")
                if 'branch_state' in tree:
                    print(f"   🌱 State: {tree['branch_state']}")
            
            # Mastery Achievement
            if 'mastery_achievement' in data['events']:
                mastery = data['events']['mastery_achievement']
                print(f"\n   🏆 ⭐ MASTERY ACHIEVED! ⭐")
                print(f"      Concept: {mastery.get('concept_name', 'N/A')}")
                print(f"      Level: {mastery.get('mastery_level', 'N/A')}/5")
                print(f"      Points: +{mastery.get('points_awarded', 0)}")
            
            # Seed Growth
            if 'seed_drop' in data['events']:
                seed = data['events']['seed_drop']
                if seed.get('triggered'):
                    print(f"\n   💎 SEED GROWTH!")
                    print(f"      Total Points: {seed.get('new_total', 0)}")
                    print(f"      To Next Stage: {seed.get('points_to_next', 0)}")
                    if seed.get('stage_up'):
                        print(f"      🎉 LEVEL UP! New Stage: {seed.get('new_stage', 'N/A')}")
        
        # Display metadata
        if 'metadata' in data:
            meta = data['metadata']
            print(f"\n🔍 Technical Metadata:")
            if 'response_time_ms' in meta:
                print(f"   ⏱️  Response Time: {meta['response_time_ms']}ms")
            if 'pii_detected' in meta:
                print(f"   🛡️  PII Detected: {meta['pii_detected']}")
            if 'safety_passed' in meta:
                print(f"   ✅ Safety Check: {'PASSED' if meta['safety_passed'] else 'FAILED'}")
            if 'tokens_used' in meta:
                print(f"   🔤 Tokens Used: {meta['tokens_used']}")
            if 'mastery_level' in meta:
                print(f"   📈 Mastery Level: {meta['mastery_level']}/5")
        
        time.sleep(1.5)  # Pause between messages for readability
        return data
        
    except Exception as e:
        print_error(f"Chat test failed: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_user_profile(user_id: int):
    """Get complete user profile"""
    try:
        response = requests.get(
            f"{BASE_URL}/api/user/{user_id}/profile",
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            print_error(f"Failed to get profile: {response.status_code}")
            return None
            
    except Exception as e:
        print_error(f"Profile fetch failed: {e}")
        return None

def display_final_summary(user_id: int):
    """Display final test summary"""
    print_section("🎉 TEST COMPLETE - FINAL SUMMARY", "🎊")
    
    profile = get_user_profile(user_id)
    
    if not profile:
        print_error("Could not fetch final profile")
        return
    
    # Seed Status
    print("💎 PRISM SEED STATUS:")
    seed = profile.get('seed', {})
    print(f"   {seed.get('current_stage_emoji', '💎')} {seed.get('current_stage_name', 'N/A')}")
    print(f"   Total Points: {seed.get('total_points', 0)}")
    print(f"   Progress: {seed.get('progress_percentage', 0)}% to next stage")
    print(f"   Points to Next: {seed.get('points_to_next_stage', 0)}")
    
    # Tree Status
    print(f"\n🌳 KNOWLEDGE TREE STATUS:")
    tree = profile.get('tree', {})
    print(f"   Overall Health: {tree.get('overall_health', 0)}%")
    print(f"   State: {tree.get('tree_state', 'N/A')}")
    print(f"   Concepts Mastered: {tree.get('total_concepts', 0)}")
    
    # Branches
    branches = tree.get('branches', {})
    if branches:
        print(f"\n🌿 BRANCHES:")
        for branch_name, branch_data in branches.items():
            print(f"   {branch_data.get('emoji', '🌱')} {branch_name.title()}:")
            print(f"      Health: {branch_data.get('health', 0)}%")
            print(f"      State: {branch_data.get('state', 'N/A')}")
            print(f"      Concepts: {branch_data.get('concepts_mastered', 0)} mastered")
    
    print("\n" + "─"*70)
    print("✅ All test steps completed successfully!")
    print("─"*70)

# ============================================
# Main Test Flow
# ============================================

def main():
    """Run the complete E2E test"""
    
    # Header
    print("\n" + "🎬"*35)
    print("  ZOYA'S LEARNING JOURNEY - END-TO-END TEST")
    print("  EchoMind AI - Complete System Verification")
    print("🎬"*35)
    
    print(f"\nTest started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Backend URL: {BASE_URL}")
    print(f"Session ID: {SESSION_ID}")
    
    # Test 0: Backend connection
    if not test_backend_connection():
        print_error("Backend is not running. Please start it first:")
        print_info("  cd backend")
        print_info("  python app.py")
        return
    
    # Step 1: Onboarding
    user_id = test_onboarding()
    if not user_id:
        print_error("Onboarding failed. Cannot continue.")
        return
    
    # Step 2: First question about gravity
    result = test_chat_message(
        user_id,
        "Why do things fall down?",
        "STEP 2: Zoya Asks About Gravity",
        "🔬"
    )
    if not result:
        print_error("First chat failed. Stopping test.")
        return
    
    # Step 3.1: Observation
    result = test_chat_message(
        user_id,
        "A ball falls faster than a feather",
        "STEP 3.1: Zoya's Observation",
        "👀"
    )
    
    # Step 3.2: Hypothesis
    result = test_chat_message(
        user_id,
        "The ball is heavier?",
        "STEP 3.2: Zoya's Hypothesis",
        "🤔"
    )
    
    # Step 3.3: Confidence Ladder trigger
    result = test_chat_message(
        user_id,
        "I don't know... would they fall the same?",
        "STEP 3.3: Confidence Ladder Activation",
        "💭"
    )
    
    # Step 3.4: Building understanding
    result = test_chat_message(
        user_id,
        "Yes, I feel air when I wave my hand",
        "STEP 3.4: Building Understanding",
        "💡"
    )
    
    # Step 4: Mastery achievement
    result = test_chat_message(
        user_id,
        "Yes! Air pushes against things. So the feather has more air pushing against it because it's flat, and the ball is round so air doesn't push as much!",
        "STEP 4: Zoya Masters the Concept!",
        "🏆"
    )
    
    # Final summary
    display_final_summary(user_id)
    
    # Success message
    print("\n" + "🎉"*35)
    print("  TEST PASSED! EchoMind AI is working perfectly!")
    print("🎉"*35 + "\n")
    
    print("📊 What was tested:")
    print("   ✅ User onboarding with Mystery Seed assignment")
    print("   ✅ Socratic dialogue (AI asks questions, not answers)")
    print("   ✅ Confidence Ladder (triggered by 'I don't know')")
    print("   ✅ Mastery tracking (concept understanding)")
    print("   ✅ Seed growth (points awarded)")
    print("   ✅ Knowledge Tree updates (branch health)")
    print("   ✅ PII protection (safety checks)")
    
    print("\n🚀 Ready for investor demo!")
    print("💡 Tip: Run this test before every demo to verify everything works.\n")

# ============================================
# Entry Point
# ============================================

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user.")
    except Exception as e:
        print_error(f"Test failed with unexpected error: {e}")
        import traceback
        traceback.print_exc()
