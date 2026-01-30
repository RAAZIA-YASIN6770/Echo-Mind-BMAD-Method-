# EchoMind AI - Backend

**Sprint 1: Infrastructure & Core Safety**  
**Status**: ✅ Ready for Development  
**Version**: 1.0

---

## 📋 Overview

This is the FastAPI backend for EchoMind AI, a Socratic learning platform for children aged 8-13.

**Sprint 1 Deliverables**:
- ✅ Project scaffolding with FastAPI
- ✅ PII Scrubbing Middleware (US-3.1) - Production Ready
- ✅ Basic Socratic Wrapper endpoint
- ✅ Database models (Users, UserProfiles, SafetyLogs)
- ✅ Configuration management
- ✅ Logging setup

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 14+
- Redis 7+ (optional for Sprint 1)
- OpenAI API key (for Sprint 2)

### Installation

1. **Create virtual environment**:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

2. **Install dependencies**:
```bash
pip install -r requirements.txt
```

3. **Download spaCy model** (for PII detection):
```bash
python -m spacy download en_core_web_sm
```

4. **Configure environment**:
```bash
# Copy example env file
cp .env.example .env

# Edit .env with your settings
# Minimum required for Sprint 1:
# - SECRET_KEY
# - DATABASE_URL
# - JWT_SECRET_KEY
# - ENCRYPTION_KEY
```

5. **Initialize database**:
```bash
# Make sure PostgreSQL is running
python init_db.py
```

6. **Run the server**:
```bash
# Development mode (with auto-reload)
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

7. **Test the API**:
```bash
# Open browser
http://localhost:8000

# API documentation
http://localhost:8000/api/docs

# Health check
curl http://localhost:8000/health
```

---

## 📁 Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── config.py               # Configuration management
├── models.py               # SQLAlchemy database models
├── init_db.py              # Database initialization script
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variables template
│
├── middleware/
│   ├── __init__.py
│   └── pii_scrubber.py     # PII detection & removal (US-3.1)
│
├── services/               # Business logic (Sprint 2+)
│   ├── __init__.py
│   ├── safety_filter.py    # Jailbreak detection (exists)
│   ├── socratic_engine.py  # Socratic AI (Sprint 2)
│   ├── llm_service.py      # OpenAI integration (Sprint 2)
│   └── ...
│
├── routers/                # API route handlers (Sprint 2+)
│   ├── __init__.py
│   ├── chat.py
│   ├── auth.py
│   └── ...
│
├── database/               # Database utilities (Sprint 2+)
│   ├── __init__.py
│   └── session.py
│
└── tests/                  # Unit tests (Sprint 2+)
    ├── __init__.py
    ├── test_pii_scrubber.py
    └── ...
```

---

## 🔧 API Endpoints

### Sprint 1 Endpoints

| Method | Endpoint | Description | Status |
|--------|----------|-------------|--------|
| GET | `/` | API information | ✅ Working |
| GET | `/health` | Health check | ✅ Working |
| POST | `/api/chat/message` | Chat with Socratic AI | ✅ Basic (Sprint 2: Full) |
| GET | `/api/test/pii-scrubber` | Test PII scrubber | ✅ Dev only |

### Example: Chat Message

**Request**:
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "123e4567-e89b-12d3-a456-426614174000",
    "session_id": "987fcdeb-51a2-43d7-9876-543210fedcba",
    "message": "What is 12 times 10?"
  }'
```

**Response**:
```json
{
  "response": {
    "message": "That's an interesting question! 🤔 Before I help you explore this, what do you already know about this topic?",
    "type": "socratic_question",
    "confidence": 1.0
  },
  "events": {
    "seed_drop": {
      "triggered": false
    },
    "tree_update": {
      "health_score": 50
    }
  },
  "metadata": {
    "response_time_ms": 0,
    "pii_detected": false,
    "safety_passed": true,
    "sprint": "sprint_1_basic"
  }
}
```

---

## 🛡️ Security Features (Sprint 1)

### PII Scrubbing Middleware (US-3.1)

**Automatically detects and removes**:
- ✅ Email addresses
- ✅ Phone numbers (multiple formats)
- ✅ Physical addresses
- ✅ Personal names
- ✅ Social Security Numbers
- ✅ Credit card numbers

**Test it**:
```bash
curl "http://localhost:8000/api/test/pii-scrubber?text=My%20email%20is%20john@example.com"
```

**Response**:
```json
{
  "original_text": "My email is john@example.com",
  "scrubbed_text": "My email is [EMAIL]",
  "pii_detected": true,
  "detections": {
    "emails": 1,
    "phones": 0,
    "addresses": 0,
    "ssns": 0,
    "credit_cards": 0,
    "names": 0
  },
  "total_pii_count": 1
}
```

---

## 🗄️ Database Schema (Sprint 1)

### Tables Created

1. **users** - Authentication and user management
   - user_id (UUID, PK)
   - email (unique)
   - password_hash
   - role (child/parent/educator)
   - created_at, last_login, is_active

2. **user_profiles** - Extended user information
   - profile_id (UUID, PK)
   - user_id (FK → users)
   - display_name
   - grade_level (3-7)
   - preferences (JSONB)
   - timezone

3. **safety_logs** - Security event logging
   - log_id (UUID, PK)
   - user_id (FK → users)
   - session_id
   - violation_type
   - severity (low/medium/high)
   - original_input, scrubbed_input
   - metadata (JSONB)
   - parent_alerted

---

## 🧪 Testing

### Manual Testing

1. **Test PII Scrubber**:
```bash
# Test email detection
curl "http://localhost:8000/api/test/pii-scrubber?text=Contact%20me%20at%20test@example.com"

# Test phone detection
curl "http://localhost:8000/api/test/pii-scrubber?text=Call%20me%20at%20123-456-7890"

# Test name detection
curl "http://localhost:8000/api/test/pii-scrubber?text=My%20name%20is%20John%20Smith"
```

2. **Test Chat Endpoint**:
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-123",
    "session_id": "test-session-456",
    "message": "Hello EchoMind!"
  }'
```

3. **Test PII Scrubbing in Chat**:
```bash
# Message with PII should be automatically scrubbed
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "test-user-123",
    "session_id": "test-session-456",
    "message": "My email is john@example.com and my phone is 123-456-7890"
  }'

# Check logs - you should see PII detection warning
```

### Unit Tests (Sprint 2)

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_pii_scrubber.py -v
```

---

## 📝 Environment Variables

See `.env.example` for all available configuration options.

**Required for Sprint 1**:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/echomind_db
JWT_SECRET_KEY=your-jwt-secret
ENCRYPTION_KEY=your-fernet-key
```

**Generate secrets**:
```python
# Generate SECRET_KEY and JWT_SECRET_KEY
import secrets
print(secrets.token_urlsafe(32))

# Generate ENCRYPTION_KEY (Fernet)
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
```

---

## 🚧 Sprint 2 Roadmap

**Coming Next**:
- [ ] Full Socratic Intelligence (Epic 2)
  - Question classification
  - Mastery level tracking
  - Master Socratic Prompt integration
  - OpenAI GPT-4 integration
  - Response scrubbing
  - Confidence Ladder

- [ ] Complete Safety Filter (Epic 3)
  - Jailbreak detection (integrate existing safety_filter.py)
  - AWS WAF configuration
  - Safety log database integration

- [ ] Authentication (Epic 4)
  - JWT token generation
  - User registration/login
  - COPPA compliance

---

## 📚 Documentation

- **PRD**: `../PRD-PRODUCT-REQUIREMENTS-DOCUMENT.md`
- **TDD**: `../TDD-TECHNICAL-DESIGN-DOCUMENT.md`
- **User Stories**: `../USER-STORIES-PHASE-1.md`
- **Master Socratic Prompt**: `../ai-prompts/master-socratic-prompt.md`

---

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Check PostgreSQL is running
# Windows
pg_ctl status

# Mac
brew services list | grep postgresql

# Linux
sudo systemctl status postgresql
```

### Import Errors

```bash
# Make sure you're in the virtual environment
which python  # Should point to venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use

```bash
# Kill process on port 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:8000 | xargs kill -9
```

---

## 👥 Team

**Sprint 1 Deliverables by**: AI Development Team  
**Date**: January 30, 2026  
**Status**: ✅ Ready for Testing

---

## 📄 License

Proprietary - EchoMind AI © 2026
