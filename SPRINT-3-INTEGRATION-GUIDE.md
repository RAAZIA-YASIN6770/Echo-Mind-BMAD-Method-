# 🚀 Quick Start: Sprint 3 Gamification Features

## 🌱 Mystery Seed Service

### Basic Usage

```python
from services.seed_service import get_seed_service

seed_service = get_seed_service()

# Assign a random seed to a new user
seed = seed_service.assign_random_seed(user_id=123)
print(f"Assigned: {seed['seed_emoji']} {seed['seed_name']}")

# Get seed information
info = seed_service.get_seed_info("prism")
print(f"Growth Stages: {info['growth_stages']}")

# Calculate current growth stage
stage = seed_service.calculate_growth_stage("prism", total_points=175)
print(f"Current Stage: {stage['current_stage_name']}")
print(f"Progress: {stage['progress_percentage']}%")

# Award points and check for level up
result = seed_service.award_points(
    seed_type="prism",
    current_points=100,
    points_to_add=75,
    reason="Solved complex puzzle"
)

if result['leveled_up']:
    print(f"🎉 {result['celebration_message']}")
```

---

## 🌳 Knowledge Tree Health Service

### Basic Usage

```python
from services.tree_health_service import get_tree_health_service

tree_service = get_tree_health_service()

# Prepare concept mastery data
concepts = [
    {
        "concept_id": "addition",
        "category": "math",
        "mastery_score": 85,
        "attempts": 10
    },
    {
        "concept_id": "photosynthesis",
        "category": "science",
        "mastery_score": 90,
        "attempts": 12
    }
]

# Calculate tree health
tree_health = tree_service.calculate_tree_health(concepts)

print(f"Overall Health: {tree_health['overall_health']}/100")
print(f"Tree State: {tree_health['tree_state']}")

# Access branch details
for category, branch in tree_health['branches'].items():
    print(f"{branch['emoji']} {branch['name']}: {branch['health_score']}/100")

# Get visualization data for frontend
viz_data = tree_service.get_branch_visualization_data(
    category="math",
    concepts=[c for c in concepts if c['category'] == 'math']
)
```

---

## 🎮 Integration Example: New User Onboarding

```python
from services.seed_service import get_seed_service
from services.tree_health_service import get_tree_health_service

def onboard_new_user(user_id: int):
    """Complete onboarding flow for new user"""
    
    # Step 1: Assign Mystery Seed
    seed_service = get_seed_service()
    seed = seed_service.assign_random_seed(user_id)
    
    # Save to database
    db.execute("""
        INSERT INTO user_seeds (user_id, seed_type, total_points, current_stage)
        VALUES (?, ?, ?, ?)
    """, (user_id, seed['seed_type'], 0, 1))
    
    # Step 2: Initialize Knowledge Tree
    tree_service = get_tree_health_service()
    initial_tree = tree_service.calculate_tree_health([])
    
    # Return onboarding data for frontend
    return {
        "seed": seed,
        "tree": initial_tree,
        "welcome_message": f"Welcome! You received a {seed['seed_emoji']} {seed['seed_name']}!"
    }
```

---

## 🎁 Integration Example: Award Points After Learning

```python
def handle_correct_answer(user_id: int, concept_id: str, category: str):
    """Award points when student answers correctly"""
    
    # Fetch user's seed info from database
    user_seed = db.query("""
        SELECT seed_type, total_points 
        FROM user_seeds 
        WHERE user_id = ?
    """, (user_id,))
    
    # Award points based on difficulty
    points_to_award = 10  # Base points
    
    seed_service = get_seed_service()
    result = seed_service.award_points(
        seed_type=user_seed['seed_type'],
        current_points=user_seed['total_points'],
        points_to_add=points_to_award,
        reason=f"Mastered {concept_id}"
    )
    
    # Update database
    db.execute("""
        UPDATE user_seeds 
        SET total_points = ?, current_stage = ?
        WHERE user_id = ?
    """, (result['new_total_points'], result['new_stage'], user_id))
    
    # Return celebration if leveled up
    if result['leveled_up']:
        return {
            "leveled_up": True,
            "message": result['celebration_message'],
            "new_stage": result['new_stage_name'],
            "emoji": result['new_stage_emoji']
        }
    
    return {"leveled_up": False}
```

---

## 📊 Integration Example: Dashboard API Endpoint

```python
from flask import Flask, jsonify
from services.tree_health_service import get_tree_health_service

app = Flask(__name__)

@app.route('/api/user/<int:user_id>/dashboard')
def get_user_dashboard(user_id: int):
    """Get complete dashboard data for user"""
    
    # Fetch concept mastery from database
    concepts = db.query("""
        SELECT concept_id, category, mastery_score, attempts
        FROM concept_mastery
        WHERE user_id = ?
    """, (user_id,))
    
    # Calculate tree health
    tree_service = get_tree_health_service()
    tree_health = tree_service.calculate_tree_health(concepts)
    
    # Fetch seed info
    seed_info = db.query("""
        SELECT seed_type, total_points, current_stage
        FROM user_seeds
        WHERE user_id = ?
    """, (user_id,))
    
    seed_service = get_seed_service()
    seed_stage = seed_service.calculate_growth_stage(
        seed_info['seed_type'],
        seed_info['total_points']
    )
    
    return jsonify({
        "tree_health": tree_health,
        "seed": {
            "type": seed_info['seed_type'],
            "stage": seed_stage,
            "points": seed_info['total_points']
        }
    })
```

---

## 🎨 Frontend Integration Example (React)

```jsx
import React, { useEffect, useState } from 'react';

function KnowledgeTreeDashboard({ userId }) {
  const [treeData, setTreeData] = useState(null);
  
  useEffect(() => {
    fetch(`/api/user/${userId}/dashboard`)
      .then(res => res.json())
      .then(data => setTreeData(data));
  }, [userId]);
  
  if (!treeData) return <div>Loading...</div>;
  
  return (
    <div className="dashboard">
      {/* Tree Health */}
      <div className="tree-health">
        <h2>🌳 Knowledge Tree</h2>
        <div className="health-bar">
          <div 
            className="health-fill" 
            style={{ width: `${treeData.tree_health.overall_health}%` }}
          />
        </div>
        <p>{treeData.tree_health.tree_state}</p>
      </div>
      
      {/* Branches */}
      <div className="branches">
        {Object.entries(treeData.tree_health.branches).map(([category, branch]) => (
          <div key={category} className="branch">
            <span className="emoji">{branch.emoji}</span>
            <span className="name">{branch.name}</span>
            <div className="health">{branch.health_score}/100</div>
            <span className="stage">{branch.growth_stage_emoji}</span>
          </div>
        ))}
      </div>
      
      {/* Mystery Seed */}
      <div className="mystery-seed">
        <h2>🌱 Your Mystery Seed</h2>
        <div className="seed-display">
          <span className="seed-emoji">{treeData.seed.stage.current_stage_emoji}</span>
          <h3>{treeData.seed.stage.current_stage_name}</h3>
          <div className="progress-bar">
            <div 
              className="progress-fill"
              style={{ width: `${treeData.seed.stage.progress_percentage}%` }}
            />
          </div>
          <p>{treeData.seed.points} / {treeData.seed.stage.next_stage_points} points</p>
        </div>
      </div>
      
      {/* Growth Tips */}
      <div className="growth-tips">
        <h3>💡 Growth Tips</h3>
        {treeData.tree_health.growth_tips.map((tip, i) => (
          <p key={i}>{tip}</p>
        ))}
      </div>
    </div>
  );
}
```

---

## 🗄️ Database Schema Updates

### Add these tables to your database:

```sql
-- User Seeds Table
CREATE TABLE user_seeds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    seed_type TEXT NOT NULL,  -- 'prism', 'coral', 'math', 'nebula'
    total_points INTEGER DEFAULT 0,
    current_stage INTEGER DEFAULT 1,
    assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Seed Progress Log (optional - for analytics)
CREATE TABLE seed_progress_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    points_awarded INTEGER NOT NULL,
    reason TEXT,
    old_stage INTEGER,
    new_stage INTEGER,
    leveled_up BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Update concept_mastery table to include category
ALTER TABLE concept_mastery ADD COLUMN category TEXT DEFAULT 'general';
```

---

## 🎯 Point Award Guidelines

### Recommended Point Values:

| Achievement | Points | Reason |
|------------|--------|---------|
| First attempt (correct) | 10 | Base reward |
| Second attempt (correct) | 7 | Slight reduction |
| Third+ attempt (correct) | 5 | Persistence reward |
| Mastery level reached | 25 | Major milestone |
| Helped another student | 15 | Social learning |
| Daily streak | 5 | Consistency bonus |
| Perfect quiz | 30 | Excellence reward |

---

## 🧪 Testing Your Integration

```python
# Test seed assignment
def test_seed_assignment():
    seed_service = get_seed_service()
    seed = seed_service.assign_random_seed(999)
    assert seed['seed_type'] in ['prism', 'coral', 'math', 'nebula']
    assert seed['current_stage'] == 1
    assert seed['total_points'] == 0
    print("✅ Seed assignment test passed")

# Test tree health calculation
def test_tree_health():
    tree_service = get_tree_health_service()
    concepts = [
        {"concept_id": "test", "category": "math", "mastery_score": 75, "attempts": 5}
    ]
    tree = tree_service.calculate_tree_health(concepts)
    assert tree['overall_health'] > 0
    assert 'math' in tree['branches']
    print("✅ Tree health test passed")

# Run tests
test_seed_assignment()
test_tree_health()
```

---

## 📚 API Endpoints to Implement

```
POST   /api/user/seed/assign          - Assign seed to new user
GET    /api/user/seed/status          - Get current seed status
POST   /api/user/seed/award-points    - Award points
GET    /api/user/tree/health          - Get tree health
GET    /api/user/tree/branch/:category - Get branch details
GET    /api/user/dashboard            - Get complete dashboard
```

---

## 🎨 UI/UX Recommendations

1. **Seed Display:**
   - Large emoji (3-4x normal size)
   - Animated glow effect on level up
   - Progress bar with gradient
   - Particle effects when awarding points

2. **Tree Visualization:**
   - SVG-based tree graphic
   - Branches grow based on health
   - Color-coded by category
   - Animated leaves for mastery concepts

3. **Celebrations:**
   - Confetti animation on level up
   - Sound effects (optional)
   - Modal with celebration message
   - Share achievement button

---

**Ready to integrate! 🚀**

For questions or issues, refer to:
- `SPRINT-2-3-TEST-RESULTS.md` - Full test results
- `demo_sprint3.py` - Working examples
- `backend/services/seed_service.py` - Seed service code
- `backend/services/tree_health_service.py` - Tree health code
