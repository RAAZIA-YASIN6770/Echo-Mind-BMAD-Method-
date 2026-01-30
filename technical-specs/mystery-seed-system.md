# Mystery Seed System - Technical Specification
**Version**: 1.0  
**Purpose**: Gamification mechanic that rewards curiosity and deep learning through collectible "seeds" that bloom into rewards.

---

## OVERVIEW

### What is a Mystery Seed?
- A **collectible reward** that appears after meaningful learning engagement
- Seeds are **topic-specific** (e.g., "Light Seed," "Ocean Seed," "Math Seed")
- Seeds **bloom** into rewards (mini-games, badges, tree decorations) when mastery is achieved
- **Psychological Hook**: Curiosity (what will it become?) + Collection + Delayed Gratification

---

## TRIGGER CONDITIONS (When Does a Seed Drop?)

### Primary Triggers:
1. **Curiosity Streak**: Child asks 3+ follow-up questions on the same topic unprompted
2. **Deep Dive**: Child spends 5+ minutes exploring a single concept
3. **Mastery Milestone**: Child correctly answers 5 questions in a topic category
4. **Critical Thinking Win**: Child successfully completes a "Misconception Buster" challenge
5. **Random Drop**: 10% chance after any successful answer (keeps engagement unpredictable)

### Anti-Gaming Measures:
- **Cooldown**: Maximum 1 seed per topic per day (prevents spam)
- **Quality Check**: Seed only drops if `mastery_level >= "understanding"` (not just correct guesses)
- **No Repeat Seeds**: Same seed type won't drop twice until previous one blooms

---

## DATA MODEL (Database Schema)

### New Table: `mystery_seeds`
```sql
CREATE TABLE mystery_seeds (
    seed_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    seed_type VARCHAR(50) NOT NULL,  -- e.g., 'light', 'ocean', 'math'
    status VARCHAR(20) DEFAULT 'planted',  -- 'planted', 'growing', 'bloomed'
    progress INTEGER DEFAULT 0,  -- 0-100 (tracks growth toward bloom)
    bloom_requirement JSONB,  -- Stores what's needed to bloom
    dropped_at TIMESTAMP DEFAULT NOW(),
    bloomed_at TIMESTAMP,
    reward_unlocked VARCHAR(100)  -- e.g., 'prism_minigame', 'ocean_badge'
);
```

### Updated Table: `tree_state`
```sql
ALTER TABLE tree_state ADD COLUMN seed_inventory JSONB DEFAULT '[]';
-- Stores array of active seed_ids for quick UI rendering
```

### New Table: `concept_mastery`
```sql
CREATE TABLE concept_mastery (
    mastery_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    concept_name VARCHAR(100) NOT NULL,  -- e.g., 'photosynthesis', 'multiplication'
    topic_category VARCHAR(50),  -- e.g., 'biology', 'math'
    mastery_level VARCHAR(20),  -- 'exposure', 'understanding', 'mastery'
    question_count INTEGER DEFAULT 0,  -- Total questions asked on this concept
    correct_count INTEGER DEFAULT 0,
    follow_up_count INTEGER DEFAULT 0,  -- Unprompted follow-up questions
    last_interaction TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## BLOOM LOGIC (How Does a Seed Grow?)

### Bloom Requirements (Stored in `bloom_requirement` JSONB)
```json
{
  "type": "light_seed",
  "requirements": {
    "follow_up_questions": 3,
    "correct_answers": 2,
    "time_spent_minutes": 5,
    "concepts_explored": ["refraction", "spectrum", "wavelength"]
  },
  "reward": {
    "type": "minigame",
    "name": "Prism Explorer",
    "description": "Unlock a game where you split light into rainbows!"
  }
}
```

### Growth Calculation Algorithm
```python
def calculate_seed_progress(seed_id, user_id):
    """
    Calculates how close a seed is to blooming (0-100%)
    """
    seed = db.query(MysterySeeds).filter_by(seed_id=seed_id).first()
    requirements = seed.bloom_requirement
    
    # Get user's progress on related concepts
    mastery_data = db.query(ConceptMastery).filter_by(
        user_id=user_id,
        topic_category=seed.seed_type
    ).all()
    
    # Calculate progress for each requirement
    progress_scores = []
    
    # 1. Follow-up questions
    total_followups = sum([m.follow_up_count for m in mastery_data])
    followup_progress = min(100, (total_followups / requirements['follow_up_questions']) * 100)
    progress_scores.append(followup_progress)
    
    # 2. Correct answers
    total_correct = sum([m.correct_count for m in mastery_data])
    correct_progress = min(100, (total_correct / requirements['correct_answers']) * 100)
    progress_scores.append(correct_progress)
    
    # 3. Concepts explored
    explored_concepts = [m.concept_name for m in mastery_data]
    required_concepts = requirements['concepts_explored']
    concept_progress = (len(set(explored_concepts) & set(required_concepts)) / len(required_concepts)) * 100
    progress_scores.append(concept_progress)
    
    # Overall progress (average of all requirements)
    overall_progress = sum(progress_scores) / len(progress_scores)
    
    # Update seed status
    if overall_progress >= 100:
        seed.status = 'bloomed'
        seed.bloomed_at = datetime.now()
        unlock_reward(user_id, seed.reward_unlocked)
    elif overall_progress >= 50:
        seed.status = 'growing'
    
    seed.progress = int(overall_progress)
    db.commit()
    
    return overall_progress
```

---

## MASTERY DETECTION (When is a Concept "Mastered"?)

### Mastery Levels:
1. **Exposure** (0-30%): Child has seen the concept but shows limited understanding
2. **Understanding** (31-70%): Child can answer questions with hints and explain reasoning
3. **Mastery** (71-100%): Child can solve independently, explain to others, and apply to new contexts

### Mastery Calculation Algorithm:
```python
def update_concept_mastery(user_id, concept_name, interaction_data):
    """
    Updates mastery level based on interaction quality
    
    interaction_data = {
        'correct': bool,
        'hints_needed': int,
        'explanation_quality': str,  # 'none', 'partial', 'complete'
        'is_followup': bool
    }
    """
    mastery = db.query(ConceptMastery).filter_by(
        user_id=user_id,
        concept_name=concept_name
    ).first()
    
    if not mastery:
        # First interaction - create new record
        mastery = ConceptMastery(
            user_id=user_id,
            concept_name=concept_name,
            topic_category=get_topic_category(concept_name),
            mastery_level='exposure'
        )
        db.add(mastery)
    
    # Update counts
    mastery.question_count += 1
    if interaction_data['correct']:
        mastery.correct_count += 1
    if interaction_data['is_followup']:
        mastery.follow_up_count += 1
    
    # Calculate mastery score (0-100)
    accuracy = (mastery.correct_count / mastery.question_count) * 100
    
    # Bonus for explanations
    explanation_bonus = {
        'none': 0,
        'partial': 10,
        'complete': 25
    }[interaction_data['explanation_quality']]
    
    # Penalty for excessive hints
    hint_penalty = min(20, interaction_data['hints_needed'] * 5)
    
    # Bonus for follow-up questions (shows curiosity)
    curiosity_bonus = min(15, mastery.follow_up_count * 3)
    
    mastery_score = accuracy + explanation_bonus - hint_penalty + curiosity_bonus
    mastery_score = max(0, min(100, mastery_score))  # Clamp to 0-100
    
    # Assign mastery level
    if mastery_score >= 71:
        mastery.mastery_level = 'mastery'
        trigger_bloom_check(user_id, mastery.topic_category)  # Check if any seeds can bloom
    elif mastery_score >= 31:
        mastery.mastery_level = 'understanding'
    else:
        mastery.mastery_level = 'exposure'
    
    mastery.last_interaction = datetime.now()
    db.commit()
    
    return mastery.mastery_level
```

---

## SEED TYPES & REWARDS

### Seed Catalog:
```python
SEED_CATALOG = {
    'light_seed': {
        'name': 'Prism Seed',
        'emoji': '🌈',
        'description': 'This seed loves questions about light and color!',
        'bloom_requirements': {
            'follow_up_questions': 3,
            'correct_answers': 2,
            'concepts_explored': ['refraction', 'spectrum', 'wavelength']
        },
        'reward': {
            'type': 'minigame',
            'name': 'Rainbow Splitter',
            'asset': 'prism_game.html'
        }
    },
    'ocean_seed': {
        'name': 'Coral Seed',
        'emoji': '🪸',
        'description': 'This seed grows when you explore the mysteries of the ocean!',
        'bloom_requirements': {
            'follow_up_questions': 4,
            'correct_answers': 3,
            'concepts_explored': ['ocean_currents', 'marine_life', 'coral_reefs']
        },
        'reward': {
            'type': 'badge',
            'name': 'Ocean Explorer',
            'asset': 'ocean_badge.svg'
        }
    },
    'math_seed': {
        'name': 'Golden Ratio Seed',
        'emoji': '🔢',
        'description': 'This seed blooms when you master number patterns!',
        'bloom_requirements': {
            'follow_up_questions': 2,
            'correct_answers': 5,
            'concepts_explored': ['multiplication', 'division', 'patterns']
        },
        'reward': {
            'type': 'tree_decoration',
            'name': 'Fibonacci Spiral Branch',
            'asset': 'fibonacci_branch.svg'
        }
    },
    'space_seed': {
        'name': 'Nebula Seed',
        'emoji': '🌌',
        'description': 'This seed glows when you ask about stars and planets!',
        'bloom_requirements': {
            'follow_up_questions': 3,
            'correct_answers': 3,
            'concepts_explored': ['planets', 'stars', 'gravity']
        },
        'reward': {
            'type': 'minigame',
            'name': 'Planet Builder',
            'asset': 'planet_game.html'
        }
    }
}
```

---

## UI/UX FLOW

### 1. Seed Drop Animation
```javascript
// When a seed is earned
function dropMysterySeeed(seedType) {
    const seed = SEED_CATALOG[seedType];
    
    // Show floating notification
    showNotification({
        icon: seed.emoji,
        title: '🌱 Mystery Seed Earned!',
        message: seed.description,
        duration: 5000,
        animation: 'float-down'
    });
    
    // Add to inventory (bottom of screen)
    addToInventory(seed);
    
    // Play sound effect
    playSound('seed_drop.mp3');
}
```

### 2. Seed Progress Indicator
```javascript
// Show seed growth in inventory
function renderSeedInventory(seeds) {
    return seeds.map(seed => `
        <div class="seed-card">
            <div class="seed-icon">${seed.emoji}</div>
            <div class="seed-name">${seed.name}</div>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${seed.progress}%"></div>
            </div>
            <div class="progress-text">${seed.progress}% to bloom</div>
            ${seed.status === 'growing' ? '<div class="sparkle-effect">✨</div>' : ''}
        </div>
    `).join('');
}
```

### 3. Bloom Celebration
```javascript
// When a seed blooms
function celebrateBloom(seed) {
    // Full-screen celebration
    showModal({
        type: 'celebration',
        content: `
            <div class="bloom-animation">
                <div class="seed-burst">${seed.emoji}</div>
                <h1>🎉 Your ${seed.name} Bloomed!</h1>
                <p>You unlocked: ${seed.reward.name}</p>
                <button onclick="claimReward('${seed.reward.asset}')">
                    Open Reward!
                </button>
            </div>
        `,
        animation: 'confetti'
    });
    
    // Play celebration sound
    playSound('bloom_celebration.mp3');
    
    // Update tree visual (add new decoration)
    updateTreeState();
}
```

---

## BACKEND API ENDPOINTS

### 1. Drop Seed
```python
@app.post("/api/seeds/drop")
def drop_seed(user_id: str, seed_type: str):
    """
    Drops a mystery seed for the user
    """
    # Check cooldown
    existing_seed = db.query(MysterySeeds).filter_by(
        user_id=user_id,
        seed_type=seed_type,
        status='planted'
    ).first()
    
    if existing_seed:
        return {"error": "Seed already exists for this topic"}
    
    # Create new seed
    seed = MysterySeeds(
        user_id=user_id,
        seed_type=seed_type,
        bloom_requirement=SEED_CATALOG[seed_type]['bloom_requirements'],
        reward_unlocked=SEED_CATALOG[seed_type]['reward']['name']
    )
    db.add(seed)
    db.commit()
    
    return {
        "success": True,
        "seed": {
            "id": seed.seed_id,
            "type": seed_type,
            "name": SEED_CATALOG[seed_type]['name'],
            "emoji": SEED_CATALOG[seed_type]['emoji']
        }
    }
```

### 2. Check Bloom Status
```python
@app.get("/api/seeds/check-bloom/{user_id}")
def check_bloom_status(user_id: str):
    """
    Checks all active seeds and updates their bloom status
    """
    seeds = db.query(MysterySeeds).filter_by(
        user_id=user_id,
        status__in=['planted', 'growing']
    ).all()
    
    bloomed_seeds = []
    for seed in seeds:
        progress = calculate_seed_progress(seed.seed_id, user_id)
        if seed.status == 'bloomed':
            bloomed_seeds.append(seed)
    
    return {
        "active_seeds": len(seeds),
        "bloomed_seeds": bloomed_seeds
    }
```

---

## ANALYTICS & INSIGHTS

### Metrics to Track:
1. **Seed Drop Rate**: How often are seeds being earned?
2. **Bloom Rate**: What % of seeds actually bloom?
3. **Time to Bloom**: Average time from drop to bloom
4. **Most Popular Seeds**: Which topics generate most engagement?
5. **Abandoned Seeds**: Seeds that never bloom (indicates difficulty or disinterest)

### Parent Dashboard View:
```
Your child has:
- 🌱 3 active seeds growing
- 🌸 5 bloomed rewards unlocked
- 🔥 Most curious about: Space & Ocean topics
```

---

**End of Mystery Seed System Specification**
