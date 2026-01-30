# 🧠 Sprint 2: Core Socratic Intelligence - README

## 🎯 Overview

Sprint 2 implements the "Brain" of Eco-Mind - the core Socratic Intelligence system that powers our AI tutor. This sprint delivers a fully functional AI that NEVER gives direct answers, instead guiding children through discovery using the Socratic method.

## ✅ What's Included

### 1. **OpenAI GPT-4o Integration** (`llm_service.py`)
The LLM Service connects to OpenAI's GPT-4o API and applies our Master Socratic Prompt to every interaction.

**Key Features**:
- Loads Master Socratic Prompt from `ai-prompts/master-socratic-prompt.md`
- Injects dynamic context (grade level, mastery, conversation history)
- Retry logic with exponential backoff
- Token usage and cost tracking
- Automatic model selection (GPT-3.5 vs GPT-4o based on complexity)

**Example**:
```python
from services.llm_service import get_llm_service

llm = get_llm_service()
result = llm.generate_response(
    user_message="What is 12 times 10?",
    grade_level=5,
    mastery_level="exposure",
    category="math"
)

print(result["response"])
# Output: "Great question! If you have 12 boxes with 10 pencils each, 
#          how would you count them all? 🤔"
```

---

### 2. **Confidence Ladder** (`confidence_ladder.py`)
Handles "I don't know" responses with progressive support.

**3-Tier System**:
1. **First "I don't know"**: Simpler Socratic question
2. **Second "I don't know"**: Multiple choice options (A/B/C)
3. **Third "I don't know"**: Curiosity Detour (fun fact + topic change)

**Example Flow**:
```python
from services.confidence_ladder import get_confidence_ladder

ladder = get_confidence_ladder()

# First IDK
result = ladder.handle_idk(
    message="I don't know",
    idk_count=1,
    original_question="What is photosynthesis?",
    category="science",
    grade_level=5
)
# Returns: Simpler question prompt

# Second IDK
result = ladder.handle_idk(
    message="I still don't know",
    idk_count=2,
    original_question="What is photosynthesis?",
    category="science",
    grade_level=5
)
# Returns: Multiple choice prompt

# Third IDK
result = ladder.handle_idk(
    message="I don't know",
    idk_count=3,
    original_question="What is photosynthesis?",
    category="science",
    grade_level=5
)
# Returns: Fun fact about science
```

---

### 3. **Mastery Tracking** (`mastery_service.py`)
Tracks student understanding of concepts over time.

**Mastery Levels**:
- **Exposure**: Just introduced (score 1.0-2.5)
- **Understanding**: Basic grasp (score 2.5-4.0)
- **Mastery**: Deep understanding (score 4.0-5.0)

**Example**:
```python
from services.mastery_service import get_mastery_service

mastery = get_mastery_service()

# Get current mastery
current = mastery.get_mastery(
    user_id="user-123",
    concept_name="multiplication"
)
print(current)
# {
#   "mastery_level": "exposure",
#   "confidence_score": 1.0,
#   "interaction_count": 0
# }

# Update after interaction
updated = mastery.update_mastery(
    user_id="user-123",
    concept_name="multiplication",
    interaction_quality=4,  # 1-5 score
    demonstrated_understanding=True
)
print(updated["mastery_level"])
# "understanding" (progressed!)
```

---

### 4. **Response Scrubber** (`response_scrubber.py`)
Validates that AI responses follow Socratic principles (Lock 3).

**Validation Checks**:
- ❌ No direct answers ("The answer is 120")
- ✅ Must end with "?"
- ✅ Must contain questions
- ❌ No imperative commands ("You must do this")
- ✅ Encouraging tone
- ✅ Age-appropriate length (50-300 chars)

**Example**:
```python
from services.response_scrubber import get_response_scrubber

scrubber = get_response_scrubber()

# Bad response (direct answer)
result = scrubber.scrub("The answer is 120.")
print(result["is_valid"])  # False
print(result["violations"])  # ["direct_answer", "no_question_mark"]

# Good response (Socratic)
result = scrubber.scrub("If you have 12 boxes with 10 pencils each, how many total?")
print(result["is_valid"])  # True
print(result["validation"]["score"])  # 95
```

---

### 5. **Socratic Engine** (`socratic_engine.py`)
Main orchestrator that ties everything together.

**Pipeline**:
1. Question classification (math/science/logic/language/general)
2. "I don't know" detection
3. Mastery level retrieval
4. Confidence Ladder handling
5. LLM response generation
6. Response scrubbing & validation
7. Regeneration if needed
8. Session state updates
9. Mastery tracking updates

**Example**:
```python
from socratic_engine import get_socratic_engine

engine = get_socratic_engine()

result = engine.process_message(
    user_id="user-123",
    session_id="session-456",
    message="What is 12 times 10?",
    grade_level=5,
    pii_detected=False
)

print(result["response"]["message"])
# "Great question! If you have 12 boxes with 10 pencils each, 
#  how would you count them all? 🤔"

print(result["metadata"])
# {
#   "category": "math",
#   "concept": "multiplication",
#   "mastery_level": "exposure",
#   "model_used": "gpt-4o",
#   "tokens_used": 45,
#   "cost": 0.000225,
#   "latency_ms": 1847
# }
```

---

## 🚀 Getting Started

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Set Up Environment
```bash
# Copy example env file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env
```

**Required**:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

### 3. Verify Master Socratic Prompt
Ensure the file exists:
```bash
ls -la ai-prompts/master-socratic-prompt.md
```

### 4. Start the Server
```bash
python main.py
```

Server will start at `http://localhost:8000`

---

## 🧪 Testing

### Test Basic Socratic Response
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-123",
    "session_id": "test-session-456",
    "message": "What is photosynthesis?"
  }'
```

**Expected**: Socratic question (NOT a direct answer)

### Test Confidence Ladder
```bash
# First "I don't know"
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-123",
    "session_id": "test-session-456",
    "message": "I don't know"
  }'

# Second "I don't know" (same session)
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-123",
    "session_id": "test-session-456",
    "message": "I still don't know"
  }'

# Third "I don't know" (same session)
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-123",
    "session_id": "test-session-456",
    "message": "I don't know"
  }'
```

**Expected**:
1. Simpler question
2. Multiple choice (A/B/C)
3. Fun fact + topic change

### Test Math Question
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-123",
    "session_id": "test-session-789",
    "message": "What is 12 times 10?"
  }'
```

**Expected**:
- Category: "math"
- Concept: "multiplication"
- Socratic response (NOT "120")

---

## 📊 Monitoring

### Check Logs
```bash
# Real-time logs
tail -f logs/echomind.log

# Filter for errors
grep "ERROR" logs/echomind.log

# Filter for LLM calls
grep "OpenAI" logs/echomind.log
```

### Key Metrics to Watch
- **Response Time**: Should be < 2.5s (p95)
- **Validation Score**: Should be ≥ 70
- **Token Usage**: ~50 tokens per interaction
- **Cost**: ~$0.00025 per interaction

### Cost Tracking
```bash
# Check daily cost (from logs)
grep "cost" logs/echomind.log | awk '{sum+=$NF} END {print "Total: $"sum}'
```

---

## 🐛 Troubleshooting

### Error: "OpenAI API key not found"
**Solution**: 
```bash
# Add to .env file
echo "OPENAI_API_KEY=sk-your-key-here" >> .env
```

### Error: "Master Socratic Prompt not found"
**Solution**:
```bash
# Verify file exists
ls -la ai-prompts/master-socratic-prompt.md

# If missing, check path in llm_service.py line 62
```

### Response is too slow (> 3s)
**Check**:
1. OpenAI API status: https://status.openai.com
2. Network latency
3. Model selection (use GPT-3.5 for simple questions)

**Solution**:
```python
# In .env, use faster model for simple questions
OPENAI_MODEL_GPT35=gpt-3.5-turbo
```

### AI gave a direct answer
**Check**:
1. Response Scrubber logs
2. Validation score in response metadata
3. Regeneration attempts

**Debug**:
```bash
# Check scrubber logs
grep "Response validation" logs/echomind.log
grep "Direct answer detected" logs/echomind.log
```

---

## 📁 File Structure

```
backend/
├── services/
│   ├── __init__.py
│   ├── llm_service.py          # OpenAI GPT-4o integration
│   ├── confidence_ladder.py    # "I don't know" handling
│   ├── mastery_service.py      # Concept mastery tracking
│   └── response_scrubber.py    # Socratic compliance validation
├── socratic_engine.py          # Main orchestrator
├── models.py                   # Database models (updated)
├── main.py                     # API endpoints (updated)
├── requirements.txt            # Dependencies
└── .env.example                # Environment template
```

---

## 🔧 Configuration

### Environment Variables

#### Required
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

#### Optional
```bash
# Model selection
LLM_DEFAULT_MODEL=gpt-4o
LLM_FALLBACK_MODEL=gpt-3.5-turbo

# API parameters
OPENAI_MAX_TOKENS=150
OPENAI_TEMPERATURE=0.7

# Cost alerts
DAILY_COST_ALERT_THRESHOLD=10.00

# Caching
REDIS_CACHE_TTL=3600
```

---

## 📚 API Reference

### POST /api/chat/message

**Request**:
```json
{
  "user_id": "string (UUID)",
  "session_id": "string (UUID)",
  "message": "string (1-500 chars)",
  "timestamp": "string (ISO 8601, optional)"
}
```

**Response**:
```json
{
  "response": {
    "message": "string (Socratic question)",
    "type": "socratic_question | multiple_choice | curiosity_detour",
    "confidence": "float (0-1)"
  },
  "events": {
    "seed_drop": {"triggered": "boolean"},
    "tree_update": {"health_score": "integer"}
  },
  "metadata": {
    "category": "math | science | logic | language | general",
    "concept": "string",
    "mastery_level": "exposure | understanding | mastery",
    "idk_count": "integer",
    "model_used": "gpt-4o | gpt-3.5-turbo",
    "tokens_used": "integer",
    "cost": "float (USD)",
    "pii_detected": "boolean",
    "validation_score": "integer (0-100)",
    "latency_ms": "integer"
  }
}
```

---

## 🎓 How It Works

### Full Pipeline Flow

```
1. User sends message
   ↓
2. PII Scrubber (middleware) removes sensitive data
   ↓
3. Socratic Engine receives clean message
   ↓
4. Question Classification (keyword-based)
   ↓
5. "I don't know" Detection
   ↓
6. Mastery Level Retrieval (from cache/DB)
   ↓
7. Confidence Ladder Check
   ├─ If triggered → Use ladder prompt
   └─ If not → Use original message
   ↓
8. Build LLM Prompt
   ├─ Master Socratic Prompt
   ├─ Context (grade, mastery, history)
   └─ User message
   ↓
9. Call OpenAI API (with retry logic)
   ↓
10. Response Scrubbing
    ├─ Validate Socratic compliance
    ├─ Check for direct answers
    └─ Verify tone and length
    ↓
11. Validation Failed?
    ├─ Yes → Regenerate (max 2 attempts)
    └─ No → Continue
    ↓
12. Update Session State
    ├─ Add to conversation history
    └─ Update IDK count
    ↓
13. Update Mastery
    ├─ Calculate new score
    └─ Check for level progression
    ↓
14. Return Final Response
```

---

## 🚀 Next Steps

### Immediate (Testing Phase)
1. ⚠️ Set OpenAI API key
2. ⚠️ Test all endpoints
3. ⚠️ Verify Confidence Ladder flows
4. ⚠️ Check performance metrics
5. ⚠️ Monitor costs

### Sprint 3 (Future)
1. Connect to PostgreSQL database
2. Implement Redis caching for LLM responses
3. Add ML-based question classification
4. Implement emotional state detection
5. Add Mystery Seed drop system
6. Build parent dashboard integration

---

## 📖 Documentation

- **Sprint 2 Complete**: `SPRINT-2-COMPLETE.md`
- **Quick Reference**: `SPRINT-2-QUICK-REFERENCE.md`
- **User Stories**: `USER-STORIES-PHASE-1.md` (Epic 2)
- **Master Socratic Prompt**: `ai-prompts/master-socratic-prompt.md`

---

## 🎉 Success Criteria

Sprint 2 is considered successful when:

- ✅ AI NEVER gives direct answers
- ✅ Confidence Ladder works for "I don't know"
- ✅ Mastery tracking updates correctly
- ✅ Response validation catches direct answers
- ✅ Response time < 2.5s (p95)
- ✅ Cost < $0.001 per interaction
- ✅ All tests pass

---

## 💡 Tips

### For Developers
- Check logs frequently during testing
- Monitor token usage to control costs
- Use GPT-3.5 for simple questions
- Cache frequently asked questions
- Test edge cases ("I don't know" x3)

### For Testing
- Use different session IDs to reset state
- Test with various grade levels
- Try different question categories
- Test the Confidence Ladder flow
- Verify no direct answers are given

---

## 📞 Support

For issues or questions:
1. Check `SPRINT-2-COMPLETE.md` for detailed info
2. Review logs in `logs/echomind.log`
3. Verify environment variables in `.env`
4. Check OpenAI API status
5. Review code comments in service files

---

**Sprint 2: Core Socratic Intelligence** 🧠  
**Status**: ✅ COMPLETE  
**Ready for**: Testing and Sprint 3 🚀
