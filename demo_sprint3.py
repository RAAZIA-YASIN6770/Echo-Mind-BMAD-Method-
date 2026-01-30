"""
============================================
EchoMind AI - Sprint 3 Demo Script
============================================

Demonstrates:
- Mystery Seed Assignment (US-8.1)
- Seed Growth & Leveling
- Knowledge Tree Health Calculation (US-7.1)
- Branch Visualization Data
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

from services.seed_service import get_seed_service, SeedType
from services.tree_health_service import get_tree_health_service


def print_section(title: str):
    """Print a section header"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}\n")


def demo_mystery_seed():
    """Demonstrate Mystery Seed assignment and growth"""
    print_section("🌱 MYSTERY SEED DEMO")
    
    seed_service = get_seed_service()
    
    # Assign seeds to 3 different users
    print("📦 Assigning Mystery Seeds to new users...\n")
    
    for user_id in [1, 2, 3]:
        assignment = seed_service.assign_random_seed(user_id)
        print(f"User {user_id}: {assignment['seed_emoji']} {assignment['seed_name']}")
        print(f"  └─ {assignment['description']}")
        print(f"  └─ Current Stage: {assignment['current_stage_emoji']} {assignment['current_stage_name']}")
        print(f"  └─ Special Ability: {assignment['special_ability']}")
        print(f"  └─ Fun Fact: {assignment['fun_fact']}\n")
    
    # Demonstrate growth progression
    print("\n" + "-"*70)
    print("🌟 SEED GROWTH PROGRESSION DEMO")
    print("-"*70 + "\n")
    
    # Simulate a Prism Seed growing
    seed_type = "prism"
    print(f"Tracking growth of {SeedType.PRISM.value.upper()} seed:\n")
    
    # Award points progressively
    point_milestones = [
        (25, "Solved first math puzzle"),
        (30, "Completed logic challenge"),
        (50, "Mastered fractions"),
        (100, "Solved complex equation"),
        (150, "Discovered pattern"),
        (200, "Helped another student"),
    ]
    
    current_points = 0
    for points, reason in point_milestones:
        result = seed_service.award_points(seed_type, current_points, points, reason)
        current_points = result["new_total_points"]
        
        print(f"🎁 +{points} points: {reason}")
        print(f"   Total: {current_points} points")
        
        if result["leveled_up"]:
            print(f"   🎉 LEVEL UP! {result['new_stage_emoji']} {result['new_stage_name']}")
            print(f"   {result['celebration_message']}")
        else:
            stage_info = seed_service.calculate_growth_stage(seed_type, current_points)
            print(f"   Progress: {stage_info['progress_percentage']:.1f}% to next level")
        print()
    
    # Show all seed types
    print("\n" + "-"*70)
    print("📚 ALL SEED TYPES")
    print("-"*70 + "\n")
    
    for seed_type in SeedType:
        info = seed_service.get_seed_info(seed_type.value)
        print(f"{info['emoji']} {info['name']}")
        print(f"  Primary Category: {info['primary_category']}")
        print(f"  Growth Stages:")
        for stage in info['growth_stages']:
            print(f"    {stage['emoji']} {stage['name']} ({stage['points_required']} pts)")
        print()


def demo_knowledge_tree():
    """Demonstrate Knowledge Tree health calculation"""
    print_section("🌳 KNOWLEDGE TREE HEALTH DEMO")
    
    tree_service = get_tree_health_service()
    
    # Simulate concept mastery data
    print("📊 Simulating student learning progress...\n")
    
    concept_data = [
        # Math concepts
        {"concept_id": "addition", "category": "math", "mastery_score": 85, "attempts": 10},
        {"concept_id": "subtraction", "category": "math", "mastery_score": 75, "attempts": 8},
        {"concept_id": "multiplication", "category": "math", "mastery_score": 60, "attempts": 5},
        {"concept_id": "fractions", "category": "math", "mastery_score": 40, "attempts": 3},
        
        # Science concepts
        {"concept_id": "photosynthesis", "category": "science", "mastery_score": 90, "attempts": 12},
        {"concept_id": "water_cycle", "category": "science", "mastery_score": 70, "attempts": 7},
        {"concept_id": "gravity", "category": "science", "mastery_score": 55, "attempts": 4},
        
        # Logic concepts
        {"concept_id": "patterns", "category": "logic", "mastery_score": 65, "attempts": 6},
        {"concept_id": "puzzles", "category": "logic", "mastery_score": 50, "attempts": 4},
        
        # Language concepts
        {"concept_id": "grammar", "category": "language", "mastery_score": 45, "attempts": 3},
        {"concept_id": "vocabulary", "category": "language", "mastery_score": 30, "attempts": 2},
    ]
    
    # Calculate tree health
    tree_health = tree_service.calculate_tree_health(concept_data)
    
    print(f"🌳 Overall Tree Health: {tree_health['overall_health']}/100")
    print(f"🎯 Tree State: {tree_health['tree_state']}")
    print(f"📚 Total Concepts Learned: {tree_health['total_concepts']}")
    print(f"🌿 Active Branches: {tree_health['total_branches']}\n")
    
    print("-"*70)
    print("BRANCH DETAILS")
    print("-"*70 + "\n")
    
    for category, branch in tree_health['branches'].items():
        print(f"{branch['emoji']} {branch['name']}")
        print(f"  Health: {branch['health_score']}/100")
        print(f"  Growth Stage: {branch['growth_stage_emoji']} {branch['growth_stage']}")
        print(f"  Concepts: {branch['concept_count']}")
        print(f"  Mastery Distribution:")
        print(f"    🌱 Exposure: {branch['mastery_distribution']['exposure']}")
        print(f"    🌿 Developing: {branch['mastery_distribution']['developing']}")
        print(f"    🌳 Proficient: {branch['mastery_distribution']['proficient']}")
        print(f"    ✨ Mastery: {branch['mastery_distribution']['mastery']}")
        print()
    
    print("-"*70)
    print("💡 GROWTH TIPS")
    print("-"*70 + "\n")
    
    for tip in tree_health['growth_tips']:
        print(f"  {tip}")
    
    # Demonstrate branch visualization
    print("\n" + "-"*70)
    print("🎨 BRANCH VISUALIZATION DATA (for Frontend)")
    print("-"*70 + "\n")
    
    math_concepts = [c for c in concept_data if c['category'] == 'math']
    viz_data = tree_service.get_branch_visualization_data('math', math_concepts)
    
    print(f"Category: {viz_data['category']}")
    print(f"Name: {viz_data['name']}")
    print(f"Color: {viz_data['color']}")
    print(f"Health: {viz_data['health_score']}/100")
    print(f"Growth Stage: {viz_data['growth_stage_emoji']} {viz_data['growth_stage']}")
    print(f"\nConcepts:")
    for concept in viz_data['concepts']:
        print(f"  - {concept['concept_id']}: {concept['mastery_score']}% ({concept['mastery_level']})")


def demo_new_user_experience():
    """Demonstrate complete new user experience"""
    print_section("🎮 NEW USER EXPERIENCE")
    
    seed_service = get_seed_service()
    tree_service = get_tree_health_service()
    
    user_id = 999
    
    print(f"👤 New User ID: {user_id}\n")
    
    # Step 1: Assign Mystery Seed
    print("STEP 1: Mystery Seed Assignment")
    print("-" * 40)
    seed = seed_service.assign_random_seed(user_id)
    print(f"🎁 You received: {seed['seed_emoji']} {seed['seed_name']}!")
    print(f"📖 {seed['description']}")
    print(f"✨ Special Ability: {seed['special_ability']}\n")
    
    # Step 2: Show initial tree state
    print("STEP 2: Initial Knowledge Tree State")
    print("-" * 40)
    initial_tree = tree_service.calculate_tree_health([])
    print(f"🌳 Tree State: {initial_tree['tree_state']}")
    print(f"💡 Tips:")
    for tip in initial_tree['growth_tips']:
        print(f"  {tip}")
    
    print("\n" + "="*70)
    print("✅ User onboarding complete! Ready to learn!")
    print("="*70)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("  🌱 EchoMind AI - Sprint 3 Gamification Demo")
    print("="*70)
    
    # Run all demos
    demo_mystery_seed()
    demo_knowledge_tree()
    demo_new_user_experience()
    
    print("\n" + "="*70)
    print("  ✅ Sprint 3 Demo Complete!")
    print("="*70)
    print("\n💡 Next Steps:")
    print("  1. Integrate seed_service with user registration")
    print("  2. Connect tree_health_service to dashboard API")
    print("  3. Build frontend visualizations")
    print("  4. Add real-time updates on learning progress")
    print("\n")
