# 🧪 Sprint 2: Testing Guide

## 🎯 Overview

This guide provides step-by-step instructions for testing all Sprint 2 features.

---

## ⚙️ Prerequisites

### 1. Environment Setup
```bash
# Navigate to backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Edit .env and add your OpenAI API key
nano .env
```

**Required in `.env`**:
```bash
OPENAI_API_KEY=sk-your-api-key-here
```

### 2. Verify Files
```bash
# Check Master Socratic Prompt exists
ls -la ../ai-prompts/master-socratic-prompt.md

# Check all services exist
ls -la services/

# Expected output:
# - llm_service.py
# - confidence_ladder.py
# - mastery_service.py
# - response_scrubber.py
```

### 3. Start Server
```bash
python main.py
```

**Expected output**:
```
🚀 EchoMind AI v1.0
🌍 Environment: development
🛡️ PII Detection: ENABLED
🔒 Jailbreak Detection: ENABLED
✅ LLM Service initialized with model: gpt-4o
✅ Confidence Ladder service initialized
✅ Mastery Service initialized
✅ Response Scrubber initialized
✅ Socratic Engine initialized
INFO:     Uvicorn running on http://0.0.0.0:8000
```

---

## 🧪 Test Suite

### Test 1: Basic Socratic Response ✅

**Objective**: Verify AI responds with questions, not direct answers

**Test Case 1.1: Math Question**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-001",
    "session_id": "test-session-001",
    "message": "What is 12 times 10?"
  }'
```

**Expected Response**:
```json
{
  "response": {
    "message": "Great question! If you have 12 boxes with 10 pencils each, how would you count them all? 🤔",
    "type": "socratic_question",
    "confidence": 0.9
  },
  "metadata": {
    "category": "math",
    "concept": "multiplication",
    "mastery_level": "exposure",
    "model_used": "gpt-4o",
    "validation_score": 95
  }
}
```

**Validation**:
- ✅ Response is a question (ends with "?")
- ✅ No direct answer ("120" not mentioned)
- ✅ Category is "math"
- ✅ Concept is "multiplication"
- ✅ Validation score ≥ 70

---

**Test Case 1.2: Science Question**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-002",
    "session_id": "test-session-002",
    "message": "What is photosynthesis?"
  }'
```

**Expected**:
- ✅ Socratic question (not a definition)
- ✅ Category: "science"
- ✅ Concept: "photosynthesis"
- ✅ No direct answer

---

### Test 2: Confidence Ladder ✅

**Objective**: Verify 3-tier progressive support for "I don't know"

**Test Case 2.1: Level 1 (First "I don't know")**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-003",
    "session_id": "test-session-003",
    "message": "I don't know"
  }'
```

**Expected Response**:
```json
{
  "response": {
    "message": "That's totally okay! 🌱 Let's start small. [simpler question]",
    "type": "socratic_question"
  },
  "metadata": {
    "idk_count": 1
  }
}
```

**Validation**:
- ✅ Contains "That's totally okay! 🌱"
- ✅ Provides simpler question
- ✅ idk_count = 1

---

**Test Case 2.2: Level 2 (Second "I don't know")**
```bash
# Use SAME session_id as Test 2.1
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-003",
    "session_id": "test-session-003",
    "message": "I still don't know"
  }'
```

**Expected Response**:
```json
{
  "response": {
    "message": "No worries! Let me give you 3 choices...\nA) [option]\nB) [option]\nC) [option]",
    "type": "socratic_question"
  },
  "metadata": {
    "idk_count": 2
  }
}
```

**Validation**:
- ✅ Contains "No worries!"
- ✅ Provides 3 choices (A/B/C)
- ✅ idk_count = 2

---

**Test Case 2.3: Level 3 (Third "I don't know")**
```bash
# Use SAME session_id as Test 2.1 and 2.2
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-003",
    "session_id": "test-session-003",
    "message": "I don't know"
  }'
```

**Expected Response**:
```json
{
  "response": {
    "message": "I can see this is tricky! Let's take a break. Did you know [fun fact]? Want to try a different topic?",
    "type": "curiosity_detour"
  },
  "metadata": {
    "idk_count": 3
  }
}
```

**Validation**:
- ✅ Contains fun fact
- ✅ Suggests topic change
- ✅ idk_count = 3

---

### Test 3: Mastery Tracking ✅

**Objective**: Verify mastery levels are tracked and updated

**Test Case 3.1: First Interaction (Exposure)**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-004",
    "session_id": "test-session-004",
    "message": "What is 5 plus 5?"
  }'
```

**Expected**:
```json
{
  "metadata": {
    "concept": "addition",
    "mastery_level": "exposure"
  }
}
```

**Validation**:
- ✅ mastery_level = "exposure" (first time)
- ✅ Concept extracted correctly

---

**Test Case 3.2: Multiple Interactions (Progression)**
```bash
# Send 5 more messages about addition with SAME user_id
for i in {1..5}; do
  curl -X POST http://localhost:8000/api/chat/message \
    -H "Content-Type: application/json" \
    -d "{
      \"user_id\": \"test-user-004\",
      \"session_id\": \"test-session-004-$i\",
      \"message\": \"What is $i plus $i?\"
    }"
  sleep 2
done
```

**Expected** (after 5 interactions):
```json
{
  "metadata": {
    "mastery_level": "understanding"  // Progressed!
  }
}
```

**Validation**:
- ✅ mastery_level progresses from "exposure" to "understanding"
- ✅ interaction_count increases

---

### Test 4: Response Scrubber ✅

**Objective**: Verify direct answers are caught and regenerated

**Test Case 4.1: Manual Scrubber Test**
```python
# In Python console
from backend.services.response_scrubber import get_response_scrubber

scrubber = get_response_scrubber()

# Test direct answer (should fail)
result = scrubber.scrub("The answer is 120.")
print(result["is_valid"])  # Should be False
print(result["violations"])  # Should include "direct_answer"

# Test Socratic response (should pass)
result = scrubber.scrub("If you have 12 boxes with 10 pencils each, how many total?")
print(result["is_valid"])  # Should be True
print(result["validation"]["score"])  # Should be ≥ 70
```

**Validation**:
- ✅ Direct answers are detected
- ✅ Socratic responses pass validation
- ✅ Score ≥ 70 for valid responses

---

### Test 5: Question Classification ✅

**Objective**: Verify questions are classified correctly

**Test Case 5.1: Math**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-005",
    "session_id": "test-session-005",
    "message": "What is 7 times 8?"
  }'
```
**Expected**: `"category": "math"`

---

**Test Case 5.2: Science**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-005",
    "session_id": "test-session-006",
    "message": "Why do plants need sunlight?"
  }'
```
**Expected**: `"category": "science"`

---

**Test Case 5.3: Logic**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-005",
    "session_id": "test-session-007",
    "message": "If all dogs are animals, and Spot is a dog, what can we say about Spot?"
  }'
```
**Expected**: `"category": "logic"`

---

### Test 6: Performance ✅

**Objective**: Verify response time is < 2.5s (p95)

**Test Case 6.1: Response Time**
```bash
# Run 10 requests and measure time
for i in {1..10}; do
  time curl -X POST http://localhost:8000/api/chat/message \
    -H "Content-Type: application/json" \
    -d "{
      \"user_id\": \"test-user-006\",
      \"session_id\": \"test-session-perf-$i\",
      \"message\": \"What is $i plus $i?\"
    }"
done
```

**Expected**:
- ✅ 95% of requests complete in < 2.5s
- ✅ Check `latency_ms` in response metadata

---

### Test 7: Cost Tracking ✅

**Objective**: Verify cost is < $0.001 per interaction

**Test Case 7.1: Token Usage**
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-007",
    "session_id": "test-session-007",
    "message": "What is gravity?"
  }'
```

**Check Response**:
```json
{
  "metadata": {
    "tokens_used": 45,
    "cost": 0.000225,
    "model_used": "gpt-4o"
  }
}
```

**Validation**:
- ✅ tokens_used < 100
- ✅ cost < $0.001
- ✅ model_used is appropriate for complexity

---

## 📊 Test Results Template

### Test Summary
```
Test 1: Basic Socratic Response
  ✅ Test 1.1: Math Question - PASS
  ✅ Test 1.2: Science Question - PASS

Test 2: Confidence Ladder
  ✅ Test 2.1: Level 1 - PASS
  ✅ Test 2.2: Level 2 - PASS
  ✅ Test 2.3: Level 3 - PASS

Test 3: Mastery Tracking
  ✅ Test 3.1: First Interaction - PASS
  ✅ Test 3.2: Progression - PASS

Test 4: Response Scrubber
  ✅ Test 4.1: Validation - PASS

Test 5: Question Classification
  ✅ Test 5.1: Math - PASS
  ✅ Test 5.2: Science - PASS
  ✅ Test 5.3: Logic - PASS

Test 6: Performance
  ✅ Test 6.1: Response Time - PASS

Test 7: Cost Tracking
  ✅ Test 7.1: Token Usage - PASS

TOTAL: 12/12 tests passed (100%)
```

---

## 🐛 Troubleshooting

### Issue: "OpenAI API key not found"
**Solution**:
```bash
# Add to .env
echo "OPENAI_API_KEY=sk-your-key-here" >> .env

# Restart server
python main.py
```

### Issue: Response is too slow
**Check**:
```bash
# Check OpenAI API status
curl https://status.openai.com/api/v2/status.json

# Check logs
tail -f logs/echomind.log | grep "latency"
```

### Issue: Direct answer was given
**Debug**:
```bash
# Check scrubber logs
grep "Response validation" logs/echomind.log
grep "Direct answer detected" logs/echomind.log

# Check validation score
grep "validation_score" logs/echomind.log
```

---

## 📝 Logging

### View Real-Time Logs
```bash
tail -f logs/echomind.log
```

### Filter for Specific Events
```bash
# LLM calls
grep "OpenAI" logs/echomind.log

# Confidence Ladder
grep "Confidence Ladder" logs/echomind.log

# Mastery updates
grep "Mastery updated" logs/echomind.log

# Validation failures
grep "validation failed" logs/echomind.log
```

---

## ✅ Acceptance Criteria

Sprint 2 testing is complete when:

- ✅ All 12 tests pass
- ✅ No direct answers are given
- ✅ Confidence Ladder works for all 3 levels
- ✅ Mastery tracking updates correctly
- ✅ Response time < 2.5s (p95)
- ✅ Cost < $0.001 per interaction
- ✅ Validation score ≥ 70 for all responses

---

## 🎉 Success!

If all tests pass, Sprint 2 is **COMPLETE** and ready for production! 🚀

**Next**: Sprint 3 - Triple-Lock Safety System
