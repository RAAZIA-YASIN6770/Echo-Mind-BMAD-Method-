# Eco-Mind System Architecture
**Version**: 1.0  
**Purpose**: Complete system architecture showing the "Life of a Request" from user input to database update

---

## ARCHITECTURE OVERVIEW

The Eco-Mind system follows a **layered microservices architecture** with 5 core layers:

1. **Client Layer** (React Native/Web)
2. **API Gateway** (FastAPI)
3. **Safety Layer** (Content Filter + PII Scrubber)
4. **Intelligence Layer** (Socratic Engine + LLM)
5. **Data Layer** (PostgreSQL + Redis)

---

## LIFE OF A REQUEST - MERMAID DIAGRAM

```mermaid
sequenceDiagram
    participant Child as 👦 Child User
    participant UI as 📱 React UI
    participant API as 🚪 API Gateway
    participant Safety as 🛡️ Safety Filter
    participant Socratic as 🧠 Socratic Engine
    participant LLM as 🤖 OpenAI GPT-4
    participant DB as 💾 PostgreSQL
    participant Redis as ⚡ Redis Cache
    participant Tree as 🌳 Knowledge Tree

    %% Step 1: User Input
    Child->>UI: Types question: "What is 12 times 10?"
    UI->>API: POST /api/chat/message
    Note over API: Request includes:<br/>user_id, session_id,<br/>message, timestamp

    %% Step 2: Safety Filter
    API->>Safety: analyze_input(message, user_id)
    Safety->>Safety: Check for:<br/>- Roleplay bypass<br/>- Sympathy exploit<br/>- Prompt injection<br/>- Homework dump<br/>- PII detection
    
    alt Violation Detected
        Safety->>API: {is_safe: false, recommended_response}
        API->>UI: Return canned response
        UI->>Child: "I'm Eco-Mind! Let's focus on learning..."
        Safety->>DB: Log violation to safety_logs
        Safety->>DB: Alert parent if severity=high
    else Input is Safe
        Safety->>API: {is_safe: true, scrubbed_input}
    end

    %% Step 3: Context Retrieval
    API->>Redis: Get session context (last 5 messages)
    Redis-->>API: Return conversation history
    API->>DB: Get user profile (grade, mastery_levels)
    DB-->>API: Return user_profile

    %% Step 4: Socratic Engine
    API->>Socratic: process_question(scrubbed_input, context, profile)
    Socratic->>Socratic: Analyze question type:<br/>- Math problem?<br/>- Science question?<br/>- Curiosity exploration?
    
    Socratic->>DB: Check concept_mastery table
    DB-->>Socratic: Return mastery_level for topic
    
    Socratic->>Socratic: Determine response strategy:<br/>- Confidence Ladder level?<br/>- Hint complexity?<br/>- Follow-up needed?

    %% Step 5: Build LLM Prompt
    Socratic->>Socratic: Build system prompt:<br/>- Master Socratic Prompt<br/>- User grade level<br/>- Mastery context<br/>- Conversation history

    Socratic->>LLM: ChatCompletion.create(system, user_input)
    Note over LLM: GPT-4 processes with<br/>Socratic constraints
    LLM-->>Socratic: Return Socratic response

    %% Step 6: Post-Processing
    Socratic->>Socratic: Analyze response quality:<br/>- Did it give direct answer? (FAIL)<br/>- Is it a guiding question? (PASS)
    
    alt Response Failed Quality Check
        Socratic->>Socratic: Regenerate with stricter prompt
        Socratic->>LLM: Retry with enhanced constraints
        LLM-->>Socratic: Return improved response
    end

    %% Step 7: Interaction Analysis
    Socratic->>Socratic: Analyze interaction:<br/>- Was it a follow-up question?<br/>- Did child explain reasoning?<br/>- Correct answer given?

    Socratic->>DB: Update concept_mastery table
    Note over DB: Update:<br/>- question_count++<br/>- follow_up_count (if applicable)<br/>- mastery_level calculation

    %% Step 8: Mystery Seed Logic
    Socratic->>DB: Check seed drop conditions
    DB-->>Socratic: Return active_seeds, topic_progress
    
    alt Seed Drop Triggered
        Socratic->>DB: INSERT into mystery_seeds
        Socratic->>API: Include seed_drop event in response
    end

    %% Step 9: Bloom Check
    Socratic->>DB: Check bloom status for active seeds
    DB->>DB: Run calculate_seed_progress()
    
    alt Seed Bloomed
        DB->>DB: UPDATE seed status = 'bloomed'
        DB->>DB: Unlock reward in user_rewards
        DB-->>Socratic: Return bloom_event
        Socratic->>API: Include bloom_celebration in response
    end

    %% Step 10: Knowledge Tree Update
    Socratic->>Tree: Calculate tree health score
    Tree->>DB: Get user's mastery_levels, streaks, seeds
    DB-->>Tree: Return aggregated data
    Tree->>Tree: Calculate:<br/>- Tree health (0-100)<br/>- Branch growth<br/>- Leaf count<br/>- Fruit positions

    Tree->>DB: UPDATE tree_state table
    Note over DB: Update:<br/>- health_score<br/>- visual_state JSON<br/>- last_updated

    %% Step 11: Cache Update
    API->>Redis: Update session context
    Note over Redis: Store:<br/>- Last 5 messages<br/>- Current topic<br/>- Interaction count

    %% Step 12: Response Assembly
    API->>API: Assemble final response:<br/>- AI message<br/>- Seed drop notification<br/>- Bloom celebration<br/>- Tree update data

    API->>UI: Return JSON response
    UI->>UI: Render components:<br/>- Chat message<br/>- Seed animation (if dropped)<br/>- Bloom celebration (if bloomed)<br/>- Tree growth animation

    UI->>Child: Display Socratic response + visual updates

    %% Step 13: Offline Challenge Check
    UI->>UI: Check session duration
    
    alt 20 Minutes Elapsed
        UI->>UI: Lock chat interface
        UI->>Child: Show "Offline Challenge" quest card
        Note over Child: Child must complete<br/>physical activity
    end

    %% Step 14: Analytics Logging
    API->>DB: Log interaction to analytics
    Note over DB: Store:<br/>- Question type<br/>- Response time<br/>- Engagement metrics<br/>- Learning outcomes
```

---

## DETAILED COMPONENT BREAKDOWN

### 1. Client Layer (React Native/Web)
**Responsibilities**:
- Render chat interface
- Display Knowledge Tree visualization
- Handle Mystery Seed animations
- Trigger offline challenges
- Manage local state (typing indicators, optimistic updates)

**Technologies**:
- React Native (iOS/Android) or Next.js (Web)
- Framer Motion (animations)
- WebSocket (real-time updates)

---

### 2. API Gateway (FastAPI)
**Responsibilities**:
- Route requests to appropriate services
- Manage authentication/authorization
- Rate limiting (prevent spam)
- Request/response logging

**Endpoints**:
```python
POST   /api/chat/message          # Send user message
GET    /api/tree/state             # Get Knowledge Tree state
GET    /api/seeds/inventory        # Get user's seeds
POST   /api/challenges/complete    # Mark offline challenge done
GET    /api/parent/insights        # Parent dashboard data
```

**Technologies**:
- FastAPI (Python async framework)
- JWT authentication
- CORS middleware

---

### 3. Safety Layer
**Responsibilities**:
- Detect jailbreak attempts
- Scrub PII (Personal Identifiable Information)
- Log violations
- Trigger parent alerts

**Implementation**: `backend/safety_filter.py`

**Flow**:
```python
def process_message(message, user_id, session_id):
    # Step 1: Safety check
    safety_result = safety_filter.analyze_input(message, user_id, session_id)
    
    if not safety_result['is_safe']:
        # Return canned response, don't call LLM
        return {
            'response': safety_result['recommended_response'],
            'source': 'safety_filter',
            'violation_logged': True
        }
    
    # Step 2: Use scrubbed input
    clean_message = safety_result['scrubbed_input']
    
    # Continue to Socratic Engine...
```

---

### 4. Intelligence Layer (Socratic Engine + LLM)

#### 4.1 Socratic Engine
**Responsibilities**:
- Analyze question type and complexity
- Retrieve user's mastery context
- Build appropriate LLM prompt
- Validate LLM response (ensure no direct answers)
- Update mastery tracking

**Core Logic**:
```python
class SocraticEngine:
    def process_question(self, question, user_profile, conversation_history):
        # 1. Classify question
        question_type = self.classify_question(question)
        
        # 2. Get mastery context
        mastery_level = db.get_concept_mastery(
            user_id=user_profile['id'],
            concept=question_type['concept']
        )
        
        # 3. Build system prompt
        system_prompt = self.build_prompt(
            base_prompt=MASTER_SOCRATIC_PROMPT,
            grade_level=user_profile['grade'],
            mastery_level=mastery_level,
            conversation_history=conversation_history
        )
        
        # 4. Call LLM
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": question}
            ],
            temperature=0.7,
            max_tokens=200
        )
        
        # 5. Validate response
        if self.contains_direct_answer(response):
            # Regenerate with stricter constraints
            response = self.regenerate_stricter(question, system_prompt)
        
        # 6. Update mastery
        self.update_mastery(user_profile['id'], question_type, response)
        
        return response
```

#### 4.2 LLM Integration
**Provider**: OpenAI GPT-4 (or Anthropic Claude 3)

**Prompt Structure**:
```
SYSTEM: [Master Socratic Prompt + User Context]
USER: [Scrubbed question]
ASSISTANT: [Socratic response - never direct answer]
```

**Quality Assurance**:
- Regex check: Does response contain "the answer is"? → FAIL
- Sentiment analysis: Is tone encouraging? → PASS
- Question detection: Does response end with "?"? → PASS

---

### 5. Data Layer

#### 5.1 PostgreSQL (Persistent Storage)
**Tables**:
1. `users` - User profiles, grade levels, settings
2. `concept_mastery` - Learning progress per topic
3. `mystery_seeds` - Seed inventory and bloom status
4. `tree_state` - Knowledge Tree visual state
5. `safety_logs` - Violation tracking
6. `parent_alerts` - Notifications for parents
7. `analytics` - Interaction metrics

**Schema Example**:
```sql
-- Concept Mastery Table
CREATE TABLE concept_mastery (
    mastery_id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(user_id),
    concept_name VARCHAR(100) NOT NULL,
    topic_category VARCHAR(50),
    mastery_level VARCHAR(20), -- 'exposure', 'understanding', 'mastery'
    question_count INTEGER DEFAULT 0,
    correct_count INTEGER DEFAULT 0,
    follow_up_count INTEGER DEFAULT 0,
    explanation_quality_avg FLOAT,
    last_interaction TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for fast lookups
CREATE INDEX idx_user_concept ON concept_mastery(user_id, concept_name);
```

#### 5.2 Redis (Session Cache)
**Cached Data**:
- Conversation history (last 5 messages)
- Current topic context
- Session duration (for offline challenge trigger)
- Temporary interaction counts

**TTL**: 24 hours (auto-expire)

**Example**:
```python
# Store session context
redis.setex(
    f"session:{session_id}",
    86400,  # 24 hours
    json.dumps({
        'messages': last_5_messages,
        'current_topic': 'multiplication',
        'interaction_count': 12,
        'session_start': timestamp
    })
)
```

---

## DATA FLOW DIAGRAMS

### Diagram 1: Mystery Seed Drop Flow
```mermaid
flowchart TD
    A[Child Asks Question] --> B{Is it a Follow-Up?}
    B -->|Yes| C[follow_up_count++]
    B -->|No| D[question_count++]
    
    C --> E{Check Drop Conditions}
    D --> E
    
    E --> F{Conditions Met?}
    F -->|No| G[Continue Normal Flow]
    F -->|Yes| H[Select Seed Type]
    
    H --> I[Create Seed in DB]
    I --> J[Add to User Inventory]
    J --> K[Trigger Drop Animation]
    K --> L[Show Notification]
    
    L --> M[Continue Chat]
    G --> M
```

### Diagram 2: Bloom Check Flow
```mermaid
flowchart TD
    A[After Each Interaction] --> B[Get Active Seeds]
    B --> C{Any Active Seeds?}
    C -->|No| D[Skip Bloom Check]
    C -->|Yes| E[For Each Seed]
    
    E --> F[Calculate Progress]
    F --> G[Get Mastery Data]
    G --> H[Score Requirements]
    
    H --> I{Progress >= 100%?}
    I -->|No| J[Update Progress Bar]
    I -->|Yes| K[Mark as Bloomed]
    
    K --> L[Unlock Reward]
    L --> M[Trigger Celebration]
    M --> N[Update Tree Visual]
    
    J --> O[Continue]
    N --> O
    D --> O
```

### Diagram 3: Knowledge Tree Update Flow
```mermaid
flowchart TD
    A[Interaction Complete] --> B[Aggregate Data]
    B --> C[Get Mastery Levels]
    B --> D[Get Active Streaks]
    B --> E[Get Bloomed Seeds]
    
    C --> F[Calculate Health Score]
    D --> F
    E --> F
    
    F --> G{Health Score}
    G -->|0-30| H[Wilted State]
    G -->|31-70| I[Growing State]
    G -->|71-100| J[Thriving State]
    
    H --> K[Update Visual JSON]
    I --> K
    J --> K
    
    K --> L[Save to tree_state]
    L --> M[Send to Frontend]
    M --> N[Animate Tree Growth]
```

---

## SCALABILITY CONSIDERATIONS

### Load Balancing
```mermaid
flowchart LR
    A[Users] --> B[Load Balancer]
    B --> C[API Server 1]
    B --> D[API Server 2]
    B --> E[API Server 3]
    
    C --> F[PostgreSQL Primary]
    D --> F
    E --> F
    
    F --> G[PostgreSQL Replica 1]
    F --> H[PostgreSQL Replica 2]
    
    C --> I[Redis Cluster]
    D --> I
    E --> I
```

### Caching Strategy
1. **L1 Cache** (Redis): Session data, conversation history
2. **L2 Cache** (CDN): Static assets, tree visualizations
3. **Database Query Cache**: Frequently accessed mastery data

### Performance Targets
- **API Response Time**: < 500ms (p95)
- **LLM Response Time**: < 2.5 seconds (p95)
- **Database Query Time**: < 50ms (p95)
- **Tree Render Time**: < 100ms

---

## SECURITY LAYERS

### Layer 1: Input Validation
- Sanitize all user input
- Limit message length (500 chars)
- Rate limiting (10 messages/minute)

### Layer 2: Safety Filter
- PII scrubbing before LLM
- Jailbreak detection
- Content filtering

### Layer 3: Authentication
- JWT tokens (15-minute expiry)
- Refresh tokens (7-day expiry)
- Parent PIN for dashboard access

### Layer 4: Data Encryption
- TLS 1.3 for all API calls
- Encrypted database fields (PII)
- Encrypted backups

---

## MONITORING & OBSERVABILITY

### Metrics to Track
1. **System Health**:
   - API uptime (target: 99.9%)
   - Database connection pool usage
   - Redis hit rate

2. **Performance**:
   - Request latency (p50, p95, p99)
   - LLM response time
   - Database query performance

3. **Business Metrics**:
   - Daily Active Users (DAU)
   - Average session duration
   - Mystery Seed drop rate
   - Bloom conversion rate

### Alerting
- **Critical**: API down, database unreachable
- **Warning**: High latency (>3s), low Redis hit rate
- **Info**: Unusual traffic patterns, new violation types

---

## DISASTER RECOVERY

### Backup Strategy
- **Database**: Automated daily backups (retained 30 days)
- **Redis**: Persistence enabled (AOF + RDB)
- **User Data**: Encrypted backups to S3

### Recovery Time Objectives
- **RTO** (Recovery Time Objective): 1 hour
- **RPO** (Recovery Point Objective): 15 minutes

---

**End of System Architecture Document**
