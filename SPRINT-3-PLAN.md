# 🌳 Sprint 3: Gamification - Mystery Seed & Knowledge Tree

**Sprint Goal:** Implement the core gamification mechanics that make learning addictive and rewarding through visual growth and mystery unlocking.

**Duration:** 2 weeks  
**Prerequisites:** Sprint 2 Complete (Socratic Intelligence + Confidence Ladder)

---

## 🎯 Sprint Overview

Sprint 3 transforms EchoMind from a conversational AI into an engaging game-like experience. Students will:
- Plant a **Mystery Seed** that grows based on their learning progress
- Watch their **Knowledge Tree** evolve through 5 growth stages
- Unlock new branches as they master different subjects
- Discover what their seed becomes (revealed at mastery level)

---

## 📦 Epic Breakdown

### **Epic 3.1: Mystery Seed System** 🌱
**Goal:** Implement the seed planting, growth tracking, and reveal mechanics

#### User Stories:

**US-3.1.1: Seed Planting (First Session)**
- **As a** new student
- **I want to** plant a mystery seed when I first use EchoMind
- **So that** I feel excited about what it will become

**Acceptance Criteria:**
- [ ] On first login, show seed selection UI with 5 mystery seed options
- [ ] Each seed has a silhouette/mystery image (no reveal yet)
- [ ] Store seed choice in `user_profile` table
- [ ] Display confirmation: "You planted a Mystery Seed! 🌱 Keep learning to see what it becomes!"

**Technical Notes:**
- Add `mystery_seed_id` and `seed_planted_date` to `users` table
- Create `mystery_seeds` table with seed types (Oak, Cherry Blossom, Cactus, Willow, Rainbow)
- Frontend: Create `SeedSelection.jsx` component with animated seed cards

---

**US-3.1.2: Growth Stage Tracking**
- **As a** student
- **I want to** see my seed grow as I learn
- **So that** I feel motivated to keep going

**Acceptance Criteria:**
- [ ] Track 5 growth stages: Seed → Sprout → Sapling → Young Tree → Mature Tree
- [ ] Growth based on total mastery points across all subjects
- [ ] Stage thresholds: 0-10 (Seed), 11-30 (Sprout), 31-60 (Sapling), 61-100 (Young), 100+ (Mature)
- [ ] Visual changes at each stage with smooth animations

**Technical Notes:**
- Create `growth_service.py` to calculate current stage
- Add `current_growth_stage` to `users` table
- Frontend: Create `TreeVisualization.jsx` with SVG/Canvas animations
- Use CSS transitions for smooth growth animations

---

**US-3.1.3: Mystery Reveal**
- **As a** student who reaches mastery
- **I want to** discover what my mystery seed became
- **So that** I feel a sense of achievement and surprise

**Acceptance Criteria:**
- [ ] At stage 5 (Mature Tree), trigger reveal animation
- [ ] Show full-color, detailed tree illustration
- [ ] Display tree name and fun fact (e.g., "Your Oak Tree can live 1000 years!")
- [ ] Award "Tree Master" badge
- [ ] Option to plant a new seed and start over

**Technical Notes:**
- Create reveal animation sequence (fade-in, sparkle effects)
- Store `tree_revealed` boolean and `reveal_date` in database
- Generate certificate/achievement card for sharing

---

### **Epic 3.2: Knowledge Tree Visualization** 🌳
**Goal:** Create an interactive, beautiful tree visualization that shows learning progress

#### User Stories:

**US-3.2.1: Tree Dashboard**
- **As a** student
- **I want to** see my Knowledge Tree on my dashboard
- **So that** I can track my progress visually

**Acceptance Criteria:**
- [ ] Display tree in center of dashboard
- [ ] Show current growth stage with percentage to next stage
- [ ] Display total mastery points earned
- [ ] Animate tree gently (leaves rustling, subtle sway)
- [ ] Mobile-responsive design

**Technical Notes:**
- Create `TreeDashboard.jsx` component
- Use SVG for scalable tree graphics
- Implement CSS animations for organic movement
- Add progress bar showing "38% to Sapling"

---

**US-3.2.2: Subject Branches**
- **As a** student
- **I want to** see different branches for different subjects
- **So that** I know which areas I'm strong in

**Acceptance Criteria:**
- [ ] Tree has 4 main branches: Math, Science, Logic, Language
- [ ] Each branch grows based on subject-specific mastery
- [ ] Branches have different colors/styles (Math=Blue, Science=Green, etc.)
- [ ] Clicking a branch shows subject-specific stats
- [ ] Branches unlock at different stages (Math at Sprout, Science at Sapling, etc.)

**Technical Notes:**
- Query `concept_mastery` table grouped by category
- Calculate branch thickness based on mastery level
- Create interactive SVG paths for each branch
- Add hover effects and click handlers

---

**US-3.2.3: Fruit/Flower Rewards**
- **As a** student who masters a concept
- **I want to** see fruits or flowers appear on my tree
- **So that** I feel rewarded for my achievements

**Acceptance Criteria:**
- [ ] When a concept reaches "mastery" level, add a fruit/flower to that branch
- [ ] Different subjects have different rewards (Math=Stars, Science=Leaves, etc.)
- [ ] Animate reward appearance (pop-in, sparkle)
- [ ] Clicking a reward shows which concept it represents
- [ ] Maximum 20 rewards visible at once (oldest fade out)

**Technical Notes:**
- Create `RewardIcon.jsx` component
- Store rewards in `tree_rewards` table
- Use absolute positioning for dynamic placement
- Implement z-index layering for depth

---

### **Epic 3.3: Growth Mechanics** ⚡
**Goal:** Define how students earn growth points and progress their tree

#### User Stories:

**US-3.3.1: Mastery Points System**
- **As a** student
- **I want to** earn points for learning activities
- **So that** I can grow my tree

**Point Awards:**
- Ask a question: +1 point
- Answer a Socratic question: +2 points
- Reach "understanding" level: +5 points
- Reach "mastery" level: +10 points
- Daily streak (3+ days): +5 bonus points
- Complete a learning session (10+ exchanges): +3 points

**Technical Notes:**
- Create `points_service.py` to handle point calculations
- Add `total_mastery_points` to `users` table
- Create `points_history` table to track all point awards
- Emit real-time events for point awards (for animations)

---

**US-3.3.2: Level-Up Animations**
- **As a** student
- **I want to** see exciting animations when my tree grows
- **So that** I feel celebrated and motivated

**Acceptance Criteria:**
- [ ] When crossing a growth threshold, trigger "Level Up!" animation
- [ ] Show before/after tree comparison
- [ ] Display points earned and new stage name
- [ ] Play celebratory sound effect (optional, can be muted)
- [ ] Show confetti or sparkle effects

**Technical Notes:**
- Use `framer-motion` for React animations
- Create `LevelUpModal.jsx` component
- Add sound effects using Web Audio API
- Store animation preferences in localStorage

---

**US-3.3.3: Daily Growth Nudges**
- **As a** student
- **I want to** be reminded to water my tree
- **So that** I stay engaged daily

**Acceptance Criteria:**
- [ ] If no activity for 24 hours, show "Your tree misses you!" message
- [ ] Display days since last activity
- [ ] Show preview of next growth stage as motivation
- [ ] Send optional email reminder (parent consent required)

**Technical Notes:**
- Create background job to check last activity
- Add `last_active_date` to `users` table
- Create notification system (in-app only for MVP)
- Respect user notification preferences

---

## 🛠️ Technical Architecture

### **New Database Tables**

```sql
-- Mystery Seeds
CREATE TABLE mystery_seeds (
    id SERIAL PRIMARY KEY,
    seed_type VARCHAR(50) NOT NULL,  -- 'oak', 'cherry', 'cactus', etc.
    name VARCHAR(100),
    description TEXT,
    silhouette_image_url VARCHAR(255),
    revealed_image_url VARCHAR(255),
    fun_fact TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Tree Rewards (fruits/flowers)
CREATE TABLE tree_rewards (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    concept_id INTEGER REFERENCES concepts(id),
    reward_type VARCHAR(50),  -- 'star', 'leaf', 'flower', 'fruit'
    branch VARCHAR(50),  -- 'math', 'science', 'logic', 'language'
    position_x FLOAT,  -- For visual placement
    position_y FLOAT,
    earned_at TIMESTAMP DEFAULT NOW()
);

-- Points History
CREATE TABLE points_history (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    points_earned INTEGER,
    reason VARCHAR(100),  -- 'question_asked', 'mastery_achieved', etc.
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Add to users table
ALTER TABLE users ADD COLUMN mystery_seed_id INTEGER REFERENCES mystery_seeds(id);
ALTER TABLE users ADD COLUMN seed_planted_date TIMESTAMP;
ALTER TABLE users ADD COLUMN current_growth_stage INTEGER DEFAULT 1;
ALTER TABLE users ADD COLUMN total_mastery_points INTEGER DEFAULT 0;
ALTER TABLE users ADD COLUMN tree_revealed BOOLEAN DEFAULT FALSE;
ALTER TABLE users ADD COLUMN reveal_date TIMESTAMP;
```

### **New Backend Services**

1. **`growth_service.py`**
   - Calculate current growth stage
   - Determine points needed for next stage
   - Handle stage transitions

2. **`points_service.py`**
   - Award points for activities
   - Track point history
   - Calculate daily streaks

3. **`tree_service.py`**
   - Generate tree visualization data
   - Calculate branch growth
   - Manage rewards placement

### **New Frontend Components**

1. **`SeedSelection.jsx`** - Mystery seed picker
2. **`TreeDashboard.jsx`** - Main tree visualization
3. **`TreeVisualization.jsx`** - SVG tree renderer
4. **`BranchComponent.jsx`** - Individual subject branches
5. **`RewardIcon.jsx`** - Fruits/flowers/stars
6. **`LevelUpModal.jsx`** - Growth celebration
7. **`ProgressBar.jsx`** - Points to next stage
8. **`TreeStats.jsx`** - Detailed statistics panel

---

## 📊 Success Metrics

**Engagement Metrics:**
- [ ] 80%+ of students plant a seed in first session
- [ ] Average 5+ daily interactions to grow tree
- [ ] 60%+ of students reach Sprout stage within 1 week
- [ ] 40%+ of students reach Sapling within 2 weeks

**Retention Metrics:**
- [ ] 70%+ return rate after planting seed
- [ ] 50%+ 7-day retention
- [ ] 30%+ 30-day retention

**Delight Metrics:**
- [ ] 90%+ positive reactions to level-up animations
- [ ] 80%+ students check tree daily
- [ ] 95%+ want to plant another seed after reveal

---

## 🎨 Visual Design Guidelines

### **Tree Art Style**
- **Aesthetic:** Whimsical, hand-drawn, watercolor-inspired
- **Colors:** Vibrant but not overwhelming (pastel palette)
- **Animation:** Smooth, organic, natural movement
- **Accessibility:** High contrast, colorblind-friendly branch colors

### **Growth Stages Visual Progression**

1. **Stage 1: Seed** 🌰
   - Small brown seed in soil
   - Subtle glow effect
   - Particle effects (sparkles)

2. **Stage 2: Sprout** 🌱
   - Two small leaves emerging
   - Light green color
   - Gentle upward animation

3. **Stage 3: Sapling** 🌿
   - Small trunk with 2-3 branches
   - First subject branch appears
   - Leaves start to fill in

4. **Stage 4: Young Tree** 🌳
   - All 4 subject branches visible
   - Fuller foliage
   - First fruits/flowers appear

5. **Stage 5: Mature Tree** 🌲
   - Full, majestic tree
   - Rich detail and color
   - Mystery reveal animation

---

## 🚀 Implementation Phases

### **Phase 1: Backend Foundation (Days 1-3)**
- [ ] Create database migrations for new tables
- [ ] Implement `growth_service.py`
- [ ] Implement `points_service.py`
- [ ] Create seed data for `mystery_seeds` table
- [ ] Write unit tests for growth calculations

### **Phase 2: Basic Tree Visualization (Days 4-6)**
- [ ] Create `TreeVisualization.jsx` with SVG
- [ ] Implement 5 growth stages (static first)
- [ ] Add basic CSS animations
- [ ] Create `TreeDashboard.jsx` layout
- [ ] Integrate with backend API

### **Phase 3: Seed Selection & Planting (Days 7-8)**
- [ ] Build `SeedSelection.jsx` UI
- [ ] Create seed selection flow
- [ ] Implement seed planting API endpoint
- [ ] Add confirmation animations
- [ ] Test first-time user experience

### **Phase 4: Points & Growth (Days 9-10)**
- [ ] Integrate points system with chat interactions
- [ ] Implement real-time point awards
- [ ] Create level-up detection logic
- [ ] Build `LevelUpModal.jsx`
- [ ] Add celebration animations

### **Phase 5: Subject Branches & Rewards (Days 11-12)**
- [ ] Implement branch growth calculations
- [ ] Create `BranchComponent.jsx`
- [ ] Add fruit/flower rewards
- [ ] Implement reward placement algorithm
- [ ] Add interactive branch clicks

### **Phase 6: Polish & Testing (Days 13-14)**
- [ ] Add sound effects (optional)
- [ ] Optimize animations for performance
- [ ] Mobile responsiveness testing
- [ ] User acceptance testing
- [ ] Bug fixes and refinements

---

## 🧪 Testing Strategy

### **Unit Tests**
- Growth stage calculations
- Points award logic
- Branch growth algorithms
- Reward placement

### **Integration Tests**
- Seed planting flow
- Points → Growth → Animation pipeline
- Database updates on level-up
- API endpoints

### **User Testing**
- First-time seed selection experience
- Level-up animation impact
- Tree visualization clarity
- Mobile usability

---

## 🎁 Bonus Features (If Time Permits)

- [ ] **Tree Customization:** Let students change tree colors/style
- [ ] **Seasonal Themes:** Halloween, Winter, Spring themes
- [ ] **Tree Gallery:** See other students' trees (anonymized)
- [ ] **Achievement Badges:** Special badges for milestones
- [ ] **Parent Dashboard:** Parents can see their child's tree
- [ ] **Tree Export:** Download tree as image to share

---

## 📝 Next Steps After Sprint 3

**Sprint 4: Social & Sharing**
- Parent progress reports
- Achievement sharing
- Leaderboards (optional)
- Multi-student classrooms

**Sprint 5: Advanced Learning**
- Adaptive difficulty
- Personalized learning paths
- Concept recommendations
- Study reminders

---

## 🎯 Sprint 3 Definition of Done

- [ ] Students can plant a mystery seed
- [ ] Tree grows through 5 stages based on learning
- [ ] Subject branches appear and grow independently
- [ ] Rewards (fruits/flowers) appear on mastery
- [ ] Level-up animations are delightful
- [ ] Mystery reveal works at stage 5
- [ ] All features work on mobile
- [ ] 90%+ test coverage on core logic
- [ ] Performance: Tree renders in <100ms
- [ ] Documentation updated

---

## 💡 Key Design Principles

1. **Visual Feedback:** Every action should have visible impact on the tree
2. **Progressive Disclosure:** Don't overwhelm - reveal features gradually
3. **Celebration:** Make achievements feel special
4. **Clarity:** Students should always know how to grow their tree
5. **Delight:** Surprise and delight at every stage

---

**Ready to grow some knowledge trees? Let's make learning magical! 🌳✨**
