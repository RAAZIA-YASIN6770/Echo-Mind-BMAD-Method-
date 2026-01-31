# 🎬 End-to-End Test Scenario: "Zoya's Learning Journey"

**Date:** January 30, 2026  
**Status:** Ready to Execute! 🚀

---

## 🎯 Test Objective

Demonstrate the complete EchoMind AI experience from onboarding to mastery achievement, showing how all systems work together:

- ✅ User Onboarding
- ✅ Mystery Seed Assignment (Prism Seed)
- ✅ Socratic Dialogue
- ✅ Confidence Ladder
- ✅ Mastery Tracking
- ✅ Knowledge Tree Growth
- ✅ Seed Evolution

---

## 👧 Meet Zoya

**Profile:**
- **Name:** Zoya
- **Age:** 10 years old
- **Grade:** 5th grade
- **Subject Interest:** Science (especially space and physics)
- **Learning Style:** Curious, asks "why" a lot
- **Parent Email:** parent@example.com

---

## 📋 Test Scenario Steps

### Step 1: New User Onboarding 🌱

**Action:** Zoya signs up for EchoMind AI

**API Call:**
```bash
curl -X POST http://localhost:5000/api/user/onboarding \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Zoya",
    "age": 10,
    "grade_level": 5,
    "parent_email": "parent@example.com"
  }'
```

**Expected Response:**
```json
{
  "success": true,
  "user": {
    "user_id": 1,
    "name": "Zoya",
    "age": 10,
    "grade_level": 5,
    "created_at": "2026-01-30T23:30:00Z"
  },
  "seed": {
    "seed_type": "prism",
    "seed_name": "Prism Seed",
    "seed_emoji": "💎",
    "current_stage": 1,
    "current_stage_name": "Tiny Crystal",
    "current_stage_emoji": "✨",
    "total_points": 0,
    "points_to_next_stage": 100,
    "special_ability": "Reveals hidden patterns in problems",
    "fun_fact": "Prism Seeds are said to be formed from frozen starlight!"
  },
  "tree": {
    "overall_health": 0,
    "tree_state": "Ready to grow! 🌱",
    "total_concepts": 0,
    "branches": {},
    "growth_tips": [
      "Start by asking questions about topics you're curious about!",
      "Don't worry about getting answers wrong - that's how we learn!",
      "Try exploring different subjects to grow all branches of your tree!"
    ]
  },
  "welcome_message": "Welcome Zoya! You received a 💎 Prism Seed! Ask questions to help it grow!"
}
```

**✅ Verification:**
- User created with ID = 1
- Prism Seed assigned (💎)
- Seed at Stage 1: "Tiny Crystal" (✨)
- Knowledge Tree initialized (empty, health = 0)
- Welcome message personalized

---

### Step 2: Zoya Asks a Science Question 🔬

**Action:** Zoya asks about gravity

**Chat Message:**
```json
{
  "user_id": "1",
  "session_id": "session_001",
  "message": "Why do things fall down?"
}
```

**API Call:**
```bash
curl -X POST http://localhost:5000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "1",
    "session_id": "session_001",
    "message": "Why do things fall down?"
  }'
```

**Expected AI Response (Socratic):**
```json
{
  "response": {
    "message": "That's a wonderful question, Zoya! 🤔 Before we explore that together, let me ask you: What do you notice happens when you drop different objects, like a ball and a feather? Do they fall the same way?",
    "type": "socratic_question",
    "confidence": 0.95,
    "category": "science",
    "subcategory": "physics"
  },
  "events": {
    "seed_drop": {
      "triggered": false,
      "reason": "First interaction, no mastery yet"
    },
    "tree_update": {
      "health_score": 5,
      "branch_updated": "science",
      "branch_health": 10
    }
  },
  "metadata": {
    "response_time_ms": 1847,
    "pii_detected": false,
    "safety_passed": true,
    "tokens_used": 156,
    "concept_id": "gravity_basics",
    "mastery_level": 0
  }
}
```

**✅ Verification:**
- AI responds with Socratic question (not direct answer)
- Question guides Zoya to think about observations
- Science branch created in Knowledge Tree
- No seed points yet (just starting)

---

### Step 3: Zoya Engages in Socratic Dialogue 💬

**Conversation Flow:**

#### **Exchange 1:**

**Zoya:** "A ball falls faster than a feather"

**AI Response:**
```json
{
  "response": {
    "message": "Great observation! 🎯 Now, why do you think the ball falls faster? What might be different about the ball and the feather?",
    "type": "socratic_question",
    "confidence": 0.93
  },
  "events": {
    "tree_update": {
      "health_score": 15,
      "branch_health": 25
    }
  },
  "metadata": {
    "mastery_level": 1,
    "progress": "building_understanding"
  }
}
```

#### **Exchange 2:**

**Zoya:** "The ball is heavier?"

**AI Response:**
```json
{
  "response": {
    "message": "You're thinking well! 🌟 Weight is part of it. But here's something interesting: if we dropped them in a place with no air, like on the Moon, what do you think would happen?",
    "type": "socratic_question",
    "confidence": 0.91
  },
  "events": {
    "tree_update": {
      "health_score": 25,
      "branch_health": 40
    }
  },
  "metadata": {
    "mastery_level": 2,
    "progress": "deepening_understanding"
  }
}
```

#### **Exchange 3:**

**Zoya:** "I don't know... would they fall the same?"

**AI Response (Confidence Ladder Triggered!):**
```json
{
  "response": {
    "message": "That's a brilliant guess! 🎉 You're absolutely right! On the Moon, with no air resistance, both would fall at the same speed. Let me break this down into smaller steps: First, think about what air does when you wave your hand. Do you feel something?",
    "type": "confidence_ladder",
    "confidence": 0.88,
    "ladder_level": 1
  },
  "events": {
    "confidence_ladder": {
      "triggered": true,
      "reason": "User said 'I don't know'",
      "ladder_level": 1
    },
    "tree_update": {
      "health_score": 35,
      "branch_health": 55
    }
  },
  "metadata": {
    "mastery_level": 3,
    "progress": "confidence_building"
  }
}
```

**✅ Verification:**
- Confidence Ladder activated when Zoya said "I don't know"
- AI provides encouragement + simpler question
- Mastery level increasing (0 → 1 → 2 → 3)
- Science branch health growing (10% → 25% → 40% → 55%)

---

### Step 4: Zoya Masters the Concept! 🏆

**Final Exchange:**

**Zoya:** "Yes! Air pushes against things. So the feather has more air pushing against it because it's flat, and the ball is round so air doesn't push as much!"

**AI Response (Mastery Achieved!):**
```json
{
  "response": {
    "message": "🎉 AMAZING, Zoya! You've discovered the concept of AIR RESISTANCE! You explained it perfectly - the feather's shape catches more air, while the ball's round shape cuts through the air more easily. This is why parachutes work! You've mastered this concept! 🌟",
    "type": "mastery_confirmation",
    "confidence": 0.98,
    "mastery_achieved": true
  },
  "events": {
    "mastery_achievement": {
      "concept_id": "gravity_basics",
      "concept_name": "Gravity and Air Resistance",
      "mastery_level": 5,
      "points_awarded": 50
    },
    "seed_drop": {
      "triggered": true,
      "points_awarded": 50,
      "new_total": 50,
      "stage_up": false,
      "current_stage": 1,
      "points_to_next": 50
    },
    "tree_update": {
      "health_score": 65,
      "branch_updated": "science",
      "branch_health": 85,
      "branch_state": "Young Tree 🌳",
      "new_concept_added": true
    }
  },
  "metadata": {
    "response_time_ms": 2103,
    "mastery_level": 5,
    "progress": "mastery_achieved",
    "celebration": true
  }
}
```

**✅ Verification:**
- Mastery achieved! (Level 5)
- **50 points awarded** to Prism Seed
- Seed progress: 50/100 points (50% to next stage)
- Science branch health: **85%** (Young Tree 🌳)
- Overall tree health: **65%**
- New concept added to tree: "Gravity and Air Resistance"

---

## 📊 Step 4: JSON Output - Prism Seed Growth

### Before Mastery:
```json
{
  "seed": {
    "seed_type": "prism",
    "seed_name": "Prism Seed",
    "seed_emoji": "💎",
    "current_stage": 1,
    "current_stage_name": "Tiny Crystal",
    "current_stage_emoji": "✨",
    "total_points": 0,
    "points_to_next_stage": 100,
    "progress_percentage": 0,
    "special_ability": "Reveals hidden patterns in problems"
  }
}
```

### After Mastery (+50 points):
```json
{
  "seed": {
    "seed_type": "prism",
    "seed_name": "Prism Seed",
    "seed_emoji": "💎",
    "current_stage": 1,
    "current_stage_name": "Tiny Crystal",
    "current_stage_emoji": "✨",
    "total_points": 50,
    "points_to_next_stage": 50,
    "progress_percentage": 50,
    "special_ability": "Reveals hidden patterns in problems",
    "growth_message": "Your Prism Seed is glowing brighter! 50% to next stage!"
  }
}
```

### After 2nd Mastery (+50 more points = 100 total):
```json
{
  "seed": {
    "seed_type": "prism",
    "seed_name": "Prism Seed",
    "seed_emoji": "💎",
    "current_stage": 2,
    "current_stage_name": "Glowing Gem",
    "current_stage_emoji": "💠",
    "total_points": 100,
    "points_to_next_stage": 150,
    "progress_percentage": 0,
    "special_ability": "Reveals hidden patterns in problems",
    "stage_up_message": "🎉 LEVEL UP! Your Tiny Crystal evolved into a Glowing Gem! 💠",
    "celebration": true
  }
}
```

**Prism Seed Evolution Path:**
1. **Stage 1:** Tiny Crystal ✨ (0-99 points)
2. **Stage 2:** Glowing Gem 💠 (100-249 points)
3. **Stage 3:** Radiant Prism 🔷 (250-499 points)
4. **Stage 4:** Crystal Palace 🏰 (500-999 points)
5. **Stage 5:** Rainbow Beacon 🌈 (1000+ points) - MAX LEVEL

---

## 🌳 Step 4: JSON Output - Science Branch Update

### Before Any Learning:
```json
{
  "tree": {
    "overall_health": 0,
    "tree_state": "Ready to grow! 🌱",
    "total_concepts": 0,
    "branches": {}
  }
}
```

### After First Question (No Mastery Yet):
```json
{
  "tree": {
    "overall_health": 5,
    "tree_state": "Starting to sprout! 🌱",
    "total_concepts": 0,
    "branches": {
      "science": {
        "category": "science",
        "health": 10,
        "state": "Sprout 🌱",
        "concepts_mastered": 0,
        "concepts_in_progress": 1,
        "emoji": "🔬"
      }
    }
  }
}
```

### After Mastery Achievement:
```json
{
  "tree": {
    "overall_health": 65,
    "tree_state": "Growing strong! 🌳",
    "total_concepts": 1,
    "branches": {
      "science": {
        "category": "science",
        "health": 85,
        "state": "Young Tree 🌳",
        "concepts_mastered": 1,
        "concepts_in_progress": 0,
        "emoji": "🔬",
        "concepts": [
          {
            "concept_id": "gravity_basics",
            "concept_name": "Gravity and Air Resistance",
            "mastery_level": 5,
            "mastered_at": "2026-01-30T23:45:00Z",
            "points_earned": 50
          }
        ]
      }
    },
    "growth_tips": [
      "Amazing work on Science! 🔬",
      "Try exploring Math next to grow another branch!",
      "You're on your way to a mighty Knowledge Tree! 🌳"
    ]
  }
}
```

**Branch Health States:**
- **0-39%:** Sprout 🌱
- **40-59%:** Sapling 🌿
- **60-79%:** Young Tree 🌳
- **80-100%:** Mighty Tree 🌲

---

## 🎯 Complete Test Script (Python)

Save this as `test_zoya_journey.py`:

```python
"""
End-to-End Test: Zoya's Learning Journey
Tests the complete EchoMind AI flow from onboarding to mastery
"""

import requests
import json
import time
from datetime import datetime

BASE_URL = "http://localhost:5000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60 + "\n")

def print_json(data, title="Response"):
    print(f"\n📋 {title}:")
    print(json.dumps(data, indent=2))

def test_onboarding():
    print_section("STEP 1: Zoya's Onboarding")
    
    response = requests.post(
        f"{BASE_URL}/api/user/onboarding",
        json={
            "name": "Zoya",
            "age": 10,
            "grade_level": 5,
            "parent_email": "parent@example.com"
        }
    )
    
    data = response.json()
    print_json(data)
    
    print("\n✅ Verification:")
    print(f"   User ID: {data['user']['user_id']}")
    print(f"   Seed Type: {data['seed']['seed_emoji']} {data['seed']['seed_name']}")
    print(f"   Seed Stage: {data['seed']['current_stage_emoji']} {data['seed']['current_stage_name']}")
    print(f"   Tree Health: {data['tree']['overall_health']}%")
    
    return data['user']['user_id']

def test_chat_message(user_id, message, step_name):
    print_section(step_name)
    print(f"💬 Zoya: \"{message}\"")
    
    response = requests.post(
        f"{BASE_URL}/api/chat/message",
        json={
            "user_id": str(user_id),
            "session_id": "session_001",
            "message": message
        }
    )
    
    data = response.json()
    
    print(f"\n🤖 AI: \"{data['response']['message']}\"")
    print(f"\n📊 Metadata:")
    print(f"   Type: {data['response']['type']}")
    print(f"   Confidence: {data['response']['confidence']}")
    
    if 'events' in data and data['events']:
        print(f"\n🎮 Events:")
        if 'tree_update' in data['events']:
            tree = data['events']['tree_update']
            print(f"   Tree Health: {tree.get('health_score', 'N/A')}%")
            if 'branch_updated' in tree:
                print(f"   Branch: {tree['branch_updated']} ({tree.get('branch_health', 'N/A')}%)")
        
        if 'mastery_achievement' in data['events']:
            mastery = data['events']['mastery_achievement']
            print(f"\n🏆 MASTERY ACHIEVED!")
            print(f"   Concept: {mastery['concept_name']}")
            print(f"   Points: +{mastery['points_awarded']}")
        
        if 'seed_drop' in data['events'] and data['events']['seed_drop'].get('triggered'):
            seed = data['events']['seed_drop']
            print(f"\n💎 SEED GROWTH!")
            print(f"   Points: {seed['new_total']}")
            print(f"   To Next Stage: {seed['points_to_next']}")
            if seed.get('stage_up'):
                print(f"   🎉 LEVEL UP! New Stage: {seed['new_stage']}")
    
    time.sleep(1)  # Pause between messages
    return data

def main():
    print("\n" + "🎬"*30)
    print("  ZOYA'S LEARNING JOURNEY - E2E TEST")
    print("🎬"*30)
    
    try:
        # Step 1: Onboarding
        user_id = test_onboarding()
        
        # Step 2: First question
        test_chat_message(
            user_id,
            "Why do things fall down?",
            "STEP 2: Zoya Asks About Gravity"
        )
        
        # Step 3: Socratic dialogue
        test_chat_message(
            user_id,
            "A ball falls faster than a feather",
            "STEP 3.1: Zoya's Observation"
        )
        
        test_chat_message(
            user_id,
            "The ball is heavier?",
            "STEP 3.2: Zoya's Hypothesis"
        )
        
        test_chat_message(
            user_id,
            "I don't know... would they fall the same?",
            "STEP 3.3: Confidence Ladder Trigger"
        )
        
        # Step 4: Mastery
        result = test_chat_message(
            user_id,
            "Yes! Air pushes against things. So the feather has more air pushing against it because it's flat, and the ball is round so air doesn't push as much!",
            "STEP 4: Zoya Masters the Concept!"
        )
        
        # Final summary
        print_section("🎉 TEST COMPLETE!")
        print("✅ All steps executed successfully!")
        print("\n📊 Final State:")
        
        # Get final profile
        profile = requests.get(f"{BASE_URL}/api/user/{user_id}/profile").json()
        print_json(profile['seed'], "Prism Seed Status")
        print_json(profile['tree'], "Knowledge Tree Status")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
```

---

## 🚀 How to Run the Test

### Prerequisites:
1. Backend server running: `python backend/app.py`
2. Database initialized: `python backend/init_db.py`

### Run the test:
```bash
cd "c:\Users\Raazia Yasin\Documents\echobmad"
python test_zoya_journey.py
```

### Expected Output:
```
🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬
  ZOYA'S LEARNING JOURNEY - E2E TEST
🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬🎬

============================================================
  STEP 1: Zoya's Onboarding
============================================================

📋 Response:
{
  "success": true,
  "user": { ... },
  "seed": { ... },
  "tree": { ... }
}

✅ Verification:
   User ID: 1
   Seed Type: 💎 Prism Seed
   Seed Stage: ✨ Tiny Crystal
   Tree Health: 0%

[... continues through all steps ...]

============================================================
  🎉 TEST COMPLETE!
============================================================
✅ All steps executed successfully!
```

---

## 📈 Success Metrics

After running the complete test, verify:

- ✅ **User Created:** Zoya (ID: 1)
- ✅ **Seed Assigned:** Prism Seed 💎
- ✅ **Seed Points:** 50+ points earned
- ✅ **Seed Progress:** 50%+ to next stage
- ✅ **Concepts Mastered:** 1 (Gravity and Air Resistance)
- ✅ **Science Branch:** 85% health (Young Tree 🌳)
- ✅ **Overall Tree Health:** 65%+
- ✅ **Confidence Ladder:** Triggered when "I don't know" detected
- ✅ **Socratic Responses:** All AI responses are questions, not direct answers
- ✅ **PII Protection:** No personal data exposed

---

## 🎊 Investor Demo Script

**Show this flow to investors:**

1. **Start:** "Meet Zoya, a 10-year-old curious about science."
2. **Onboarding:** "She signs up and gets a Mystery Seed - a Prism Seed!"
3. **First Question:** "She asks why things fall down."
4. **Socratic Magic:** "Instead of answering, our AI asks HER questions."
5. **Confidence Ladder:** "When she says 'I don't know,' we adapt!"
6. **Mastery:** "Through dialogue, she discovers air resistance herself!"
7. **Rewards:** "She earns 50 points, her seed grows, her tree flourishes!"
8. **Result:** "Learning through discovery, not memorization. That's EchoMind."

---

*EchoMind AI - Where learning comes alive* 🌱

**Generated:** January 30, 2026  
**Sprint:** Final Assembly - E2E Test Scenario
