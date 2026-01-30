# Parent Insights Report - Weekly Email Template
**Version**: 1.0  
**Purpose**: Transform raw data into meaningful insights for parents  
**Tone**: Encouraging, specific, actionable

---

## EMAIL TEMPLATE (HTML Version)

```html
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Your Child's Learning Journey This Week</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background: #f5f5f5; }
        .container { max-width: 600px; margin: 20px auto; background: white; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        .header { background: linear-gradient(135deg, #4CAF50, #2196F3); padding: 30px; color: white; text-align: center; }
        .section { padding: 25px; border-bottom: 1px solid #eee; }
        .metric-card { background: #f9f9f9; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #4CAF50; }
        .highlight { color: #4CAF50; font-weight: bold; font-size: 1.2em; }
        .badge { display: inline-block; background: #FFD700; color: #333; padding: 5px 12px; border-radius: 20px; font-size: 0.9em; margin: 5px; }
        .tree-visual { text-align: center; font-size: 3em; margin: 20px 0; }
        .footer { background: #f5f5f5; padding: 20px; text-align: center; font-size: 0.9em; color: #666; }
    </style>
</head>
<body>
    <div class="container">
        <!-- HEADER -->
        <div class="header">
            <h1>🌱 Eco-Mind Weekly Report</h1>
            <p>Your Child's Learning Journey</p>
            <p style="font-size: 0.9em; opacity: 0.9;">Week of January 23-29, 2026</p>
        </div>

        <!-- SECTION 1: HEADLINE INSIGHT -->
        <div class="section">
            <h2>🎉 This Week's Highlight</h2>
            <p style="font-size: 1.1em; line-height: 1.6;">
                <strong>Sarah</strong> showed <span class="highlight">exceptional curiosity</span> this week! 
                She asked <span class="highlight">23 follow-up questions</span> unprompted—that's 
                <strong>3x more than last week</strong>. This shows she's not just looking for answers, 
                but truly exploring ideas. 🌟
            </p>
        </div>

        <!-- SECTION 2: CURIOSITY METRICS -->
        <div class="section">
            <h2>🔍 Curiosity Metrics</h2>
            <p style="color: #666; margin-bottom: 15px;">
                These metrics show how deeply your child is engaging with learning, 
                not just getting correct answers.
            </p>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">📊 Follow-Up Questions</h3>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div class="highlight">23 questions</div>
                        <div style="font-size: 0.9em; color: #666;">↑ 15 from last week</div>
                    </div>
                    <div style="font-size: 2em;">📈</div>
                </div>
                <p style="margin-top: 10px; font-size: 0.95em; color: #555;">
                    <strong>What this means:</strong> Sarah is asking "Why?" and "How?" without 
                    being prompted. This is the hallmark of a curious mind!
                </p>
            </div>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">⏱️ Deep Dive Sessions</h3>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div class="highlight">4 sessions</div>
                        <div style="font-size: 0.9em; color: #666;">Avg. 12 minutes each</div>
                    </div>
                    <div style="font-size: 2em;">🕐</div>
                </div>
                <p style="margin-top: 10px; font-size: 0.95em; color: #555;">
                    <strong>What this means:</strong> Sarah spent extended time exploring topics 
                    (photosynthesis, ocean currents). This shows sustained focus and genuine interest.
                </p>
            </div>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">🌈 Topics Explored</h3>
                <div>
                    <span class="badge">🌿 Photosynthesis</span>
                    <span class="badge">🌊 Ocean Currents</span>
                    <span class="badge">🔢 Multiplication</span>
                    <span class="badge">🌙 Moon Phases</span>
                </div>
                <p style="margin-top: 10px; font-size: 0.95em; color: #555;">
                    <strong>What this means:</strong> Sarah is exploring diverse topics, showing 
                    intellectual breadth. Her strongest interest this week was <strong>Ocean Currents</strong> 
                    (9 questions asked).
                </p>
            </div>
        </div>

        <!-- SECTION 3: CRITICAL THINKING GROWTH -->
        <div class="section">
            <h2>🧠 Critical Thinking Growth</h2>
            <p style="color: #666; margin-bottom: 15px;">
                We track how well your child explains their reasoning, not just if they get the right answer.
            </p>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">💡 Explanation Quality</h3>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div class="highlight">8.2/10</div>
                        <div style="font-size: 0.9em; color: #666;">↑ 1.5 points from last week</div>
                    </div>
                    <div style="font-size: 2em;">⭐</div>
                </div>
                <p style="margin-top: 10px; font-size: 0.95em; color: #555;">
                    <strong>Example:</strong> When asked "How did you figure out 12 x 10?", 
                    Sarah said: <em>"I know 10 x 10 is 100, so I added 2 more groups of 10, 
                    which is 20. So 100 + 20 = 120!"</em> This shows she understands the 
                    <strong>process</strong>, not just the answer.
                </p>
            </div>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">🎯 Misconception Busters Completed</h3>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div class="highlight">3/3 correct</div>
                        <div style="font-size: 0.9em; color: #666;">100% success rate</div>
                    </div>
                    <div style="font-size: 2em;">✅</div>
                </div>
                <p style="margin-top: 10px; font-size: 0.95em; color: #555;">
                    <strong>What this means:</strong> Sarah successfully identified false statements 
                    (e.g., "Plants eat pizza to grow") and explained WHY they were wrong. 
                    This shows strong critical thinking!
                </p>
            </div>
        </div>

        <!-- SECTION 4: KNOWLEDGE TREE STATUS -->
        <div class="section">
            <h2>🌳 Knowledge Tree Status</h2>
            <div class="tree-visual">
                🌸<br>
                🌳<br>
                🍎 🌿 🌺
            </div>
            <div style="text-align: center;">
                <div class="highlight" style="font-size: 1.5em;">Tree Health: 87%</div>
                <div style="color: #666; margin-top: 10px;">
                    ↑ 12% from last week
                </div>
            </div>

            <div class="metric-card" style="margin-top: 20px;">
                <h3 style="margin: 0 0 10px 0;">🌱 Growth This Week</h3>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li><strong>3 new leaves</strong> (3 concepts explored)</li>
                    <li><strong>1 fruit grown</strong> (Photosynthesis mastered! 🍎)</li>
                    <li><strong>2 branches extended</strong> (Science & Math topics)</li>
                </ul>
            </div>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">🔥 Learning Streak</h3>
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div class="highlight">7 days</div>
                        <div style="font-size: 0.9em; color: #666;">Longest streak this month!</div>
                    </div>
                    <div style="font-size: 2em;">🔥</div>
                </div>
                <p style="margin-top: 10px; font-size: 0.95em; color: #555;">
                    <strong>Consistency is key!</strong> Sarah has logged in every day this week. 
                    This regular practice builds strong learning habits.
                </p>
            </div>
        </div>

        <!-- SECTION 5: MYSTERY SEEDS & REWARDS -->
        <div class="section">
            <h2>🎁 Mystery Seeds & Rewards</h2>
            <p style="color: #666; margin-bottom: 15px;">
                Seeds are earned through curiosity and bloom when concepts are mastered.
            </p>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">🌈 Prism Seed BLOOMED! 🎉</h3>
                <p style="font-size: 0.95em; color: #555; margin: 10px 0;">
                    Sarah's curiosity about <strong>light and color</strong> paid off! 
                    After asking 5 follow-up questions and explaining how rainbows form, 
                    her Prism Seed bloomed into the <strong>Rainbow Splitter Mini-Game</strong>.
                </p>
                <div style="background: #FFF9C4; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <strong>💡 Parent Tip:</strong> Ask Sarah to show you the game! 
                    It teaches light refraction through play.
                </div>
            </div>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">🪸 Coral Seed (In Progress)</h3>
                <div style="background: #E0E0E0; height: 20px; border-radius: 10px; overflow: hidden; margin: 10px 0;">
                    <div style="background: linear-gradient(90deg, #4CAF50, #2196F3); width: 68%; height: 100%;"></div>
                </div>
                <p style="font-size: 0.95em; color: #555;">
                    <strong>68% complete</strong> - Sarah is exploring ocean topics. 
                    Just 2 more questions to bloom!
                </p>
            </div>
        </div>

        <!-- SECTION 6: OFFLINE CHALLENGES -->
        <div class="section">
            <h2>🏃 Offline Challenges Completed</h2>
            <p style="color: #666; margin-bottom: 15px;">
                These physical activities balance screen time with real-world exploration.
            </p>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">✅ 5 Challenges Completed</h3>
                <ul style="margin: 10px 0; padding-left: 20px;">
                    <li>🔍 <strong>Shadow Detective</strong> - Explored light and shadows</li>
                    <li>🎨 <strong>Color Hunt</strong> - Found 3 red objects</li>
                    <li>⚖️ <strong>Balance Experiment</strong> - Tested balance with eyes closed</li>
                    <li>💧 <strong>Water Drop Race</strong> - Learned about friction</li>
                    <li>💚 <strong>Gratitude Hunt</strong> - Practiced mindfulness</li>
                </ul>
                <div style="background: #E8F5E9; padding: 10px; border-radius: 5px; margin-top: 10px;">
                    <strong>🌟 Highlight:</strong> Sarah described the Shadow Detective challenge 
                    in detail, showing she genuinely engaged with it. She discovered that moving 
                    her hand closer to the light made the shadow bigger!
                </div>
            </div>
        </div>

        <!-- SECTION 7: MASTERY LEVELS -->
        <div class="section">
            <h2>📈 Mastery Levels (By Topic)</h2>
            <p style="color: #666; margin-bottom: 15px;">
                We track learning depth across 3 levels: Exposure → Understanding → Mastery
            </p>

            <div style="margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <strong>🌿 Photosynthesis</strong>
                    <span class="badge" style="background: #4CAF50; color: white;">MASTERY</span>
                </div>
                <div style="background: #E0E0E0; height: 12px; border-radius: 6px; overflow: hidden;">
                    <div style="background: #4CAF50; width: 92%; height: 100%;"></div>
                </div>
                <p style="font-size: 0.85em; color: #666; margin-top: 5px;">
                    Sarah can explain how plants make food AND apply it to new scenarios.
                </p>
            </div>

            <div style="margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <strong>🌊 Ocean Currents</strong>
                    <span class="badge" style="background: #2196F3; color: white;">UNDERSTANDING</span>
                </div>
                <div style="background: #E0E0E0; height: 12px; border-radius: 6px; overflow: hidden;">
                    <div style="background: #2196F3; width: 68%; height: 100%;"></div>
                </div>
                <p style="font-size: 0.85em; color: #666; margin-top: 5px;">
                    Sarah can answer questions with hints and explain basic concepts.
                </p>
            </div>

            <div style="margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <strong>🔢 Multiplication</strong>
                    <span class="badge" style="background: #2196F3; color: white;">UNDERSTANDING</span>
                </div>
                <div style="background: #E0E0E0; height: 12px; border-radius: 6px; overflow: hidden;">
                    <div style="background: #2196F3; width: 55%; height: 100%;"></div>
                </div>
                <p style="font-size: 0.85em; color: #666; margin-top: 5px;">
                    Sarah is building confidence. She can solve problems but sometimes needs hints.
                </p>
            </div>

            <div style="margin: 15px 0;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
                    <strong>🌙 Moon Phases</strong>
                    <span class="badge" style="background: #9E9E9E; color: white;">EXPOSURE</span>
                </div>
                <div style="background: #E0E0E0; height: 12px; border-radius: 6px; overflow: hidden;">
                    <div style="background: #9E9E9E; width: 25%; height: 100%;"></div>
                </div>
                <p style="font-size: 0.85em; color: #666; margin-top: 5px;">
                    Sarah just started exploring this topic. Early stages of learning.
                </p>
            </div>
        </div>

        <!-- SECTION 8: SAFETY & WELLBEING -->
        <div class="section">
            <h2>🛡️ Safety & Wellbeing</h2>
            
            <div class="metric-card" style="border-left-color: #4CAF50;">
                <h3 style="margin: 0 0 10px 0;">✅ No Safety Concerns</h3>
                <p style="font-size: 0.95em; color: #555;">
                    All interactions this week were appropriate and educational. 
                    No blocked content or jailbreak attempts detected.
                </p>
            </div>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">😊 Emotional Tone: Positive</h3>
                <p style="font-size: 0.95em; color: #555;">
                    Sarah's messages showed enthusiasm and curiosity. No signs of frustration 
                    or disengagement. She used phrases like "That's cool!" and "I want to learn more!"
                </p>
            </div>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">⏱️ Screen Time Balance</h3>
                <p style="font-size: 0.95em; color: #555;">
                    <strong>Average session: 18 minutes</strong> (healthy duration)<br>
                    <strong>Offline challenges: 5 completed</strong> (excellent balance)<br>
                    Sarah is maintaining a healthy mix of digital and physical learning.
                </p>
            </div>
        </div>

        <!-- SECTION 9: CONVERSATION HIGHLIGHTS -->
        <div class="section">
            <h2>💬 Conversation Highlights</h2>
            <p style="color: #666; margin-bottom: 15px;">
                Real moments that show Sarah's thinking process:
            </p>

            <div style="background: #F5F5F5; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #2196F3;">
                <p style="margin: 0; font-style: italic; color: #555;">
                    <strong>Sarah:</strong> "Wait, if plants need sunlight to make food, 
                    do they eat at night?"
                </p>
                <p style="margin: 10px 0 0 0; font-size: 0.9em; color: #666;">
                    <strong>Why this matters:</strong> This unprompted question shows Sarah is 
                    connecting ideas and thinking critically about what she's learned.
                </p>
            </div>

            <div style="background: #F5F5F5; padding: 15px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #4CAF50;">
                <p style="margin: 0; font-style: italic; color: #555;">
                    <strong>Sarah:</strong> "I figured out 12 x 10 by thinking of it like 
                    a rectangle with 12 rows and 10 columns!"
                </p>
                <p style="margin: 10px 0 0 0; font-size: 0.9em; color: #666;">
                    <strong>Why this matters:</strong> Sarah is using visual reasoning, 
                    showing she understands multiplication as area, not just memorization.
                </p>
            </div>
        </div>

        <!-- SECTION 10: RECOMMENDATIONS FOR PARENTS -->
        <div class="section">
            <h2>💡 How You Can Support Sarah's Learning</h2>
            
            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">1. Ask Open-Ended Questions</h3>
                <p style="font-size: 0.95em; color: #555;">
                    Instead of "Did you learn anything today?", try: 
                    <strong>"What was the most interesting question you asked Eco-Mind today?"</strong>
                </p>
            </div>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">2. Explore Her Interests</h3>
                <p style="font-size: 0.95em; color: #555;">
                    Sarah is fascinated by <strong>ocean currents</strong> right now. 
                    Consider watching a documentary together or visiting an aquarium 
                    (if possible) to deepen this interest.
                </p>
            </div>

            <div class="metric-card">
                <h3 style="margin: 0 0 10px 0;">3. Celebrate the Process, Not Just Results</h3>
                <p style="font-size: 0.95em; color: #555;">
                    Say: <strong>"I love how you explained your thinking!"</strong> instead of 
                    just "Good job getting it right!" This reinforces curiosity over correctness.
                </p>
            </div>
        </div>

        <!-- FOOTER -->
        <div class="footer">
            <p>
                <strong>Questions about this report?</strong><br>
                Visit your <a href="#" style="color: #4CAF50;">Parent Dashboard</a> 
                for detailed analytics and conversation logs.
            </p>
            <p style="margin-top: 15px; font-size: 0.85em;">
                🌱 Eco-Mind · Helping children think, not just answer<br>
                <a href="#" style="color: #666;">Privacy Policy</a> · 
                <a href="#" style="color: #666;">Unsubscribe</a>
            </p>
        </div>
    </div>
</body>
</html>
```

---

## PLAIN TEXT VERSION (For Email Clients Without HTML)

```
═══════════════════════════════════════════════════════════
🌱 ECO-MIND WEEKLY REPORT
Your Child's Learning Journey
Week of January 23-29, 2026
═══════════════════════════════════════════════════════════

🎉 THIS WEEK'S HIGHLIGHT
───────────────────────────────────────────────────────────
Sarah showed EXCEPTIONAL CURIOSITY this week! She asked 23 
follow-up questions unprompted—that's 3x more than last week. 
This shows she's not just looking for answers, but truly 
exploring ideas.

🔍 CURIOSITY METRICS
───────────────────────────────────────────────────────────
📊 Follow-Up Questions: 23 (↑ 15 from last week)
   → Sarah is asking "Why?" and "How?" without being prompted

⏱️ Deep Dive Sessions: 4 sessions (Avg. 12 minutes each)
   → Extended time exploring photosynthesis and ocean currents

🌈 Topics Explored:
   • Photosynthesis 🌿
   • Ocean Currents 🌊
   • Multiplication 🔢
   • Moon Phases 🌙

🧠 CRITICAL THINKING GROWTH
───────────────────────────────────────────────────────────
💡 Explanation Quality: 8.2/10 (↑ 1.5 points)
   Example: "I know 10 x 10 is 100, so I added 2 more groups 
   of 10, which is 20. So 100 + 20 = 120!"

🎯 Misconception Busters: 3/3 correct (100% success rate)

🌳 KNOWLEDGE TREE STATUS
───────────────────────────────────────────────────────────
Tree Health: 87% (↑ 12% from last week)
🔥 Learning Streak: 7 days (Longest this month!)

Growth This Week:
• 3 new leaves (3 concepts explored)
• 1 fruit grown (Photosynthesis mastered!)
• 2 branches extended (Science & Math)

🎁 MYSTERY SEEDS & REWARDS
───────────────────────────────────────────────────────────
🌈 Prism Seed BLOOMED! 🎉
   Unlocked: Rainbow Splitter Mini-Game
   
🪸 Coral Seed: 68% complete (2 more questions to bloom!)

🏃 OFFLINE CHALLENGES COMPLETED
───────────────────────────────────────────────────────────
✅ 5 Challenges Completed:
   • Shadow Detective
   • Color Hunt
   • Balance Experiment
   • Water Drop Race
   • Gratitude Hunt

📈 MASTERY LEVELS
───────────────────────────────────────────────────────────
🌿 Photosynthesis: ████████████ MASTERY (92%)
🌊 Ocean Currents: ████████░░░░ UNDERSTANDING (68%)
🔢 Multiplication: ███████░░░░░ UNDERSTANDING (55%)
🌙 Moon Phases:    ███░░░░░░░░░ EXPOSURE (25%)

💬 CONVERSATION HIGHLIGHTS
───────────────────────────────────────────────────────────
Sarah: "Wait, if plants need sunlight to make food, do they 
eat at night?"

→ This unprompted question shows critical thinking!

💡 HOW YOU CAN SUPPORT SARAH
───────────────────────────────────────────────────────────
1. Ask: "What was the most interesting question you asked 
   Eco-Mind today?"
   
2. Sarah is fascinated by ocean currents—consider watching 
   a documentary together!
   
3. Celebrate the process: "I love how you explained your 
   thinking!"

═══════════════════════════════════════════════════════════
Questions? Visit your Parent Dashboard for detailed analytics.
🌱 Eco-Mind · Helping children think, not just answer
═══════════════════════════════════════════════════════════
```

---

## DATA SOURCES (Backend Implementation)

### SQL Queries to Generate Report

```sql
-- 1. Curiosity Metrics
SELECT 
    COUNT(*) FILTER (WHERE is_followup = TRUE) as followup_count,
    COUNT(DISTINCT DATE(created_at)) as active_days,
    AVG(session_duration_minutes) as avg_session_duration
FROM interactions
WHERE user_id = :user_id 
  AND created_at >= NOW() - INTERVAL '7 days';

-- 2. Topics Explored
SELECT 
    topic_category,
    COUNT(*) as question_count,
    AVG(mastery_level_numeric) as avg_mastery
FROM concept_mastery
WHERE user_id = :user_id
  AND last_interaction >= NOW() - INTERVAL '7 days'
GROUP BY topic_category
ORDER BY question_count DESC;

-- 3. Explanation Quality
SELECT 
    AVG(explanation_quality_score) as avg_quality,
    COUNT(*) FILTER (WHERE explanation_quality = 'complete') as complete_count
FROM interactions
WHERE user_id = :user_id
  AND created_at >= NOW() - INTERVAL '7 days';

-- 4. Mystery Seeds
SELECT 
    seed_type,
    status,
    progress,
    bloomed_at
FROM mystery_seeds
WHERE user_id = :user_id
  AND (status = 'bloomed' AND bloomed_at >= NOW() - INTERVAL '7 days')
     OR status IN ('planted', 'growing');

-- 5. Offline Challenges
SELECT 
    challenge_name,
    completed_at,
    description_quality
FROM offline_challenges
WHERE user_id = :user_id
  AND completed_at >= NOW() - INTERVAL '7 days'
ORDER BY completed_at DESC;
```

---

## PYTHON REPORT GENERATOR

```python
from datetime import datetime, timedelta
from jinja2 import Template

class WeeklyReportGenerator:
    def __init__(self, user_id, week_start_date):
        self.user_id = user_id
        self.week_start = week_start_date
        self.week_end = week_start_date + timedelta(days=7)
    
    def generate_report(self):
        """Generate complete weekly report"""
        data = {
            'child_name': self.get_child_name(),
            'week_range': f"{self.week_start.strftime('%B %d')}-{self.week_end.strftime('%d, %Y')}",
            'curiosity_metrics': self.get_curiosity_metrics(),
            'critical_thinking': self.get_critical_thinking_metrics(),
            'tree_status': self.get_tree_status(),
            'mystery_seeds': self.get_mystery_seeds(),
            'offline_challenges': self.get_offline_challenges(),
            'mastery_levels': self.get_mastery_levels(),
            'conversation_highlights': self.get_conversation_highlights(),
            'recommendations': self.generate_recommendations()
        }
        
        # Render HTML template
        template = Template(HTML_TEMPLATE)
        html_report = template.render(**data)
        
        return html_report
    
    def get_curiosity_metrics(self):
        """Calculate curiosity-based metrics"""
        current_week = db.query("""
            SELECT 
                COUNT(*) FILTER (WHERE is_followup = TRUE) as followup_count,
                COUNT(*) as total_questions,
                COUNT(DISTINCT session_id) FILTER (WHERE session_duration_minutes >= 10) as deep_dive_sessions,
                AVG(session_duration_minutes) FILTER (WHERE session_duration_minutes >= 10) as avg_deep_dive_duration
            FROM interactions
            WHERE user_id = :user_id 
              AND created_at BETWEEN :week_start AND :week_end
        """, user_id=self.user_id, week_start=self.week_start, week_end=self.week_end).first()
        
        last_week = db.query("""
            SELECT COUNT(*) FILTER (WHERE is_followup = TRUE) as followup_count
            FROM interactions
            WHERE user_id = :user_id 
              AND created_at BETWEEN :last_week_start AND :last_week_end
        """, user_id=self.user_id, 
             last_week_start=self.week_start - timedelta(days=7),
             last_week_end=self.week_start).first()
        
        return {
            'followup_count': current_week.followup_count,
            'followup_change': current_week.followup_count - last_week.followup_count,
            'deep_dive_sessions': current_week.deep_dive_sessions,
            'avg_deep_dive_duration': round(current_week.avg_deep_dive_duration, 1)
        }
    
    def generate_recommendations(self):
        """Generate personalized recommendations based on data"""
        mastery_data = self.get_mastery_levels()
        
        # Find strongest interest
        strongest_topic = max(mastery_data, key=lambda x: x['question_count'])
        
        recommendations = [
            {
                'title': 'Ask Open-Ended Questions',
                'description': f'Instead of "Did you learn anything today?", try: "What was the most interesting question you asked Eco-Mind today?"'
            },
            {
                'title': 'Explore Their Interests',
                'description': f'{self.get_child_name()} is fascinated by {strongest_topic["name"]} right now. Consider finding related activities or resources to deepen this interest.'
            },
            {
                'title': 'Celebrate the Process',
                'description': 'Say "I love how you explained your thinking!" instead of just "Good job getting it right!"'
            }
        ]
        
        return recommendations
```

---

**End of Parent Insights Report Template**
