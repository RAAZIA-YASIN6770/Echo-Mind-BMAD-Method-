"""
============================================
EchoMind AI - Main Application
Sprint 1: Infrastructure & Core Safety
============================================

This is the main FastAPI application entry point.
It includes:
- PII Scrubbing Middleware (US-3.1)
- Basic Socratic Engine endpoint (Hello World)
- Health check endpoint
- CORS configuration
- Logging setup

Future sprints will add:
- Full Socratic Intelligence (Epic 2)
- Complete Safety Filter (Epic 3)
- Authentication (Epic 4)
- Chat Interface (Epic 5)
"""

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging
from datetime import datetime
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

from config import settings
from middleware.pii_scrubber import PIIScrubberMiddleware
from socratic_engine import get_socratic_engine

# ============================================
# Logging Configuration
# ============================================

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        # File handler will be added in production
    ]
)

logger = logging.getLogger(__name__)

# ============================================
# FastAPI Application
# ============================================

app = FastAPI(
    title=settings.APP_NAME,
    description="Socratic AI Learning Platform for Children (Ages 8-13)",
    version=settings.API_VERSION,
    debug=settings.DEBUG,
    docs_url="/api/docs" if settings.DEBUG else None,
    redoc_url="/api/redoc" if settings.DEBUG else None,
)

# ============================================
# Middleware Configuration
# ============================================

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# PII Scrubber Middleware (US-3.1)
app.add_middleware(
    PIIScrubberMiddleware,
    enabled=settings.PII_DETECTION_ENABLED
)

logger.info(f"🚀 {settings.APP_NAME} starting in {settings.APP_ENV} mode")
logger.info(f"🛡️ PII Detection: {'ENABLED' if settings.PII_DETECTION_ENABLED else 'DISABLED'}")

# ============================================
# Request/Response Models
# ============================================

class ChatMessageRequest(BaseModel):
    """Request model for chat messages"""
    user_id: str = Field(..., description="User UUID")
    session_id: str = Field(..., description="Session UUID")
    message: str = Field(..., min_length=1, max_length=500, description="User message")
    timestamp: Optional[str] = Field(default=None, description="Client timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "123e4567-e89b-12d3-a456-426614174000",
                "session_id": "987fcdeb-51a2-43d7-9876-543210fedcba",
                "message": "What is 12 times 10?",
                "timestamp": "2026-01-30T19:30:00Z"
            }
        }


class ChatMessageResponse(BaseModel):
    """Response model for chat messages"""
    response: Dict[str, Any] = Field(..., description="AI response")
    events: Optional[Dict[str, Any]] = Field(default=None, description="Game events (seeds, tree updates)")
    metadata: Dict[str, Any] = Field(..., description="Response metadata")
    
    class Config:
        json_schema_extra = {
            "example": {
                "response": {
                    "message": "Great question! If you have 12 boxes with 10 pencils each, how would you count them all? 🤔",
                    "type": "socratic_question",
                    "confidence": 0.92
                },
                "events": {
                    "seed_drop": {
                        "triggered": False
                    },
                    "tree_update": {
                        "health_score": 67
                    }
                },
                "metadata": {
                    "response_time_ms": 1847,
                    "pii_detected": False,
                    "safety_passed": True
                }
            }
        }


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    version: str
    environment: str
    services: Dict[str, str]


# ============================================
# API Endpoints
# ============================================

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint - API information"""
    return {
        "name": settings.APP_NAME,
        "version": settings.API_VERSION,
        "status": "running",
        "environment": settings.APP_ENV,
        "docs": "/api/docs" if settings.DEBUG else "disabled",
        "message": "Welcome to EchoMind AI - Socratic Learning Platform 🌱"
    }


@app.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint
    Used by load balancers and monitoring systems
    """
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version=settings.API_VERSION,
        environment=settings.APP_ENV,
        services={
            "api": "healthy",
            "database": "not_connected",  # Will be updated in Sprint 2
            "redis": "not_connected",     # Will be updated in Sprint 2
            "llm": "not_connected"        # Will be updated in Sprint 2
        }
    )


@app.post("/api/chat/message", response_model=ChatMessageResponse, tags=["Chat"])
async def chat_message(request: ChatMessageRequest, raw_request: Request):
    """
    Main chat endpoint - Socratic Wrapper Hook
    
    This is a basic implementation for Sprint 1.
    Full Socratic Intelligence will be added in Sprint 2.
    
    Current features:
    - PII scrubbing (via middleware)
    - Basic response generation
    - Metadata tracking
    
    Future features (Sprint 2):
    - Question classification
    - Mastery level retrieval
    - Master Socratic Prompt integration
    - LLM API integration
    - Response scrubbing
    - Confidence Ladder
    """
    
    # Get PII scrub result from middleware (if available)
    pii_scrub_result = getattr(raw_request.state, 'pii_scrub_result', None)
    pii_detected = pii_scrub_result['pii_detected'] if pii_scrub_result else False
    
    logger.info(
        f"Chat message received | "
        f"user_id={request.user_id} | "
        f"session_id={request.session_id} | "
        f"message_length={len(request.message)} | "
        f"pii_detected={pii_detected}"
    )
    
    # ============================================
    # SPRINT 2: Full Socratic Intelligence
    # Using the Socratic Engine orchestrator
    # ============================================
    
    try:
        # Get Socratic Engine instance
        socratic_engine = get_socratic_engine()
        
        # Process message through full Socratic pipeline
        result = socratic_engine.process_message(
            user_id=request.user_id,
            session_id=request.session_id,
            message=request.message,
            grade_level=5,  # Default, will be retrieved from user profile in future
            pii_detected=pii_detected
        )
        
        # Build response
        response = ChatMessageResponse(
            response=result["response"],
            events=result.get("events"),
            metadata=result.get("metadata", {})
        )
        
        logger.info(
            f"✅ Socratic response sent | "
            f"user_id={request.user_id} | "
            f"latency={result['metadata'].get('latency_ms', 0)}ms | "
            f"tokens={result['metadata'].get('tokens_used', 0)}"
        )
        
        return response
    
    except Exception as e:
        logger.error(f"❌ Error in chat endpoint: {e}", exc_info=True)
        
        # Fallback response
        return ChatMessageResponse(
            response={
                "message": "That's a great question! 🤔 What do you already know about this topic?",
                "type": "fallback",
                "confidence": 1.0
            },
            events={
                "seed_drop": {"triggered": False},
                "tree_update": {"health_score": 50}
            },
            metadata={
                "pii_detected": pii_detected,
                "safety_passed": True,
                "error": str(e),
                "sprint": "sprint_2_error_fallback"
            }
        )


@app.get("/api/test/pii-scrubber", tags=["Testing"])
async def test_pii_scrubber(text: str):
    """
    Test endpoint for PII scrubber
    Only available in development mode
    
    Example: /api/test/pii-scrubber?text=My email is john@example.com
    """
    if not settings.DEBUG:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Test endpoints are only available in development mode"
        )
    
    from middleware.pii_scrubber import scrub_pii
    result = scrub_pii(text)
    
    return {
        "original_text": text,
        "scrubbed_text": result['scrubbed_text'],
        "pii_detected": result['pii_detected'],
        "detections": result['detections'],
        "total_pii_count": result['total_pii_count']
    }


# ============================================
# Error Handlers
# ============================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": exc.status_code,
                "message": exc.detail,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error" if not settings.DEBUG else str(exc),
                "timestamp": datetime.utcnow().isoformat()
            }
        }
    )


# ============================================
# Startup/Shutdown Events
# ============================================

@app.on_event("startup")
async def startup_event():
    """Application startup tasks"""
    logger.info("=" * 60)
    logger.info(f"🚀 {settings.APP_NAME} v{settings.API_VERSION}")
    logger.info(f"🌍 Environment: {settings.APP_ENV}")
    logger.info(f"🛡️ PII Detection: {'ENABLED' if settings.PII_DETECTION_ENABLED else 'DISABLED'}")
    logger.info(f"🔒 Jailbreak Detection: {'ENABLED' if settings.JAILBREAK_DETECTION_ENABLED else 'DISABLED'}")
    logger.info(f"📝 Debug Mode: {settings.DEBUG}")
    logger.info(f"🌐 CORS Origins: {settings.cors_origins_list}")
    logger.info("=" * 60)
    
    # Future: Initialize database connection
    # Future: Initialize Redis connection
    # Future: Load Master Socratic Prompt
    # Future: Initialize LLM client


@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown tasks"""
    logger.info("🛑 Shutting down EchoMind AI...")
    
    # Future: Close database connections
    # Future: Close Redis connections
    # Future: Cleanup resources


# ============================================
# Main Entry Point
# ============================================

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
        access_log=True
    )
