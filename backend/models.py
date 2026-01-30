"""
============================================
EchoMind AI - Database Models
Sprint 1: Users and Safety Logs
============================================
"""

from sqlalchemy import (
    Column, String, Integer, Boolean, DateTime, Text, 
    ForeignKey, CheckConstraint, Index, TIMESTAMP, UUID
)
from sqlalchemy.dialects.postgresql import JSONB, UUID as PG_UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime

Base = declarative_base()


class User(Base):
    """
    User table - Stores authentication and basic user information
    Supports child, parent, and educator roles
    """
    __tablename__ = "users"
    
    user_id = Column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        comment="Unique user identifier"
    )
    email = Column(
        String(255), 
        unique=True, 
        nullable=False,
        index=True,
        comment="User email address (unique)"
    )
    password_hash = Column(
        String(255), 
        nullable=False,
        comment="Bcrypt hashed password"
    )
    role = Column(
        String(20), 
        nullable=False,
        comment="User role: child, parent, or educator"
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        comment="Account creation timestamp"
    )
    last_login = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Last successful login timestamp"
    )
    is_active = Column(
        Boolean, 
        default=True,
        nullable=False,
        comment="Account active status"
    )
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    safety_logs = relationship("SafetyLog", back_populates="user", cascade="all, delete-orphan")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "role IN ('child', 'parent', 'educator')",
            name="check_user_role"
        ),
        Index("idx_users_email", "email"),
        Index("idx_users_role", "role"),
        Index("idx_users_created_at", "created_at"),
    )
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, email={self.email}, role={self.role})>"


class UserProfile(Base):
    """
    User Profile table - Extended user information
    Stores grade level, preferences, and personalization data
    """
    __tablename__ = "user_profiles"
    
    profile_id = Column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        comment="Unique profile identifier"
    )
    user_id = Column(
        PG_UUID(as_uuid=True), 
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        comment="Reference to users table"
    )
    display_name = Column(
        String(100),
        nullable=True,
        comment="User display name (can be anonymous)"
    )
    grade_level = Column(
        Integer,
        nullable=True,
        comment="Student grade level (3-7)"
    )
    preferences = Column(
        JSONB,
        default={},
        nullable=False,
        comment="User preferences and settings (JSON)"
    )
    timezone = Column(
        String(50),
        default="UTC",
        nullable=False,
        comment="User timezone"
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        comment="Profile creation timestamp"
    )
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "grade_level IS NULL OR (grade_level BETWEEN 3 AND 7)",
            name="check_grade_level_range"
        ),
        Index("idx_user_profiles_user_id", "user_id"),
        Index("idx_user_profiles_grade_level", "grade_level"),
    )
    
    def __repr__(self):
        return f"<UserProfile(profile_id={self.profile_id}, display_name={self.display_name}, grade={self.grade_level})>"


class SafetyLog(Base):
    """
    Safety Logs table - Records all safety violations and PII detection events
    Critical for monitoring and parent alerts
    """
    __tablename__ = "safety_logs"
    
    log_id = Column(
        PG_UUID(as_uuid=True), 
        primary_key=True, 
        default=uuid.uuid4,
        comment="Unique log identifier"
    )
    user_id = Column(
        PG_UUID(as_uuid=True), 
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        comment="Reference to users table"
    )
    session_id = Column(
        PG_UUID(as_uuid=True),
        nullable=True,
        comment="Session identifier (if available)"
    )
    violation_type = Column(
        String(50),
        nullable=False,
        comment="Type of violation: pii_detected, jailbreak_attempt, etc."
    )
    severity = Column(
        String(10),
        nullable=False,
        comment="Severity level: low, medium, high"
    )
    original_input = Column(
        Text,
        nullable=True,
        comment="Original user input (for audit purposes)"
    )
    scrubbed_input = Column(
        Text,
        nullable=True,
        comment="PII-scrubbed version of input"
    )
    metadata = Column(
        JSONB,
        default={},
        nullable=False,
        comment="Additional violation metadata (JSON)"
    )
    parent_alerted = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether parent was notified"
    )
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        index=True,
        comment="Log creation timestamp"
    )
    
    # Relationships
    user = relationship("User", back_populates="safety_logs")
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "severity IN ('low', 'medium', 'high')",
            name="check_severity_level"
        ),
        Index("idx_safety_logs_user_id", "user_id"),
        Index("idx_safety_logs_severity", "severity"),
        Index("idx_safety_logs_created_at", "created_at"),
        Index("idx_safety_logs_violation_type", "violation_type"),
        Index("idx_safety_logs_user_severity", "user_id", "severity"),
    )
    
    def __repr__(self):
        return f"<SafetyLog(log_id={self.log_id}, user_id={self.user_id}, violation={self.violation_type}, severity={self.severity})>"


# ============================================
# Sprint 2 Models: Socratic Intelligence
# ============================================

class ConceptMastery(Base):
    """
    Concept Mastery table - Tracks student understanding of concepts
    Used for adaptive difficulty and personalized learning paths
    """
    __tablename__ = "concept_mastery"
    
    mastery_id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique mastery record identifier"
    )
    user_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        comment="Reference to users table"
    )
    concept_name = Column(
        String(100),
        nullable=False,
        comment="Concept name (e.g., 'multiplication', 'photosynthesis')"
    )
    mastery_level = Column(
        String(20),
        nullable=False,
        default="exposure",
        comment="Mastery level: exposure, understanding, mastery"
    )
    interaction_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of interactions with this concept"
    )
    confidence_score = Column(
        Integer,
        default=1,
        nullable=False,
        comment="Confidence score (1-5)"
    )
    last_interaction = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Last interaction timestamp"
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Record creation timestamp"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint(
            "mastery_level IN ('exposure', 'understanding', 'mastery')",
            name="check_mastery_level"
        ),
        CheckConstraint(
            "confidence_score BETWEEN 1 AND 5",
            name="check_confidence_score"
        ),
        Index("idx_concept_mastery_user_id", "user_id"),
        Index("idx_concept_mastery_concept", "concept_name"),
        Index("idx_concept_mastery_user_concept", "user_id", "concept_name", unique=True),
    )
    
    def __repr__(self):
        return f"<ConceptMastery(user_id={self.user_id}, concept={self.concept_name}, level={self.mastery_level})>"


class Session(Base):
    """
    Sessions table - Tracks chat sessions and conversation context
    Stores conversation history and session metadata
    """
    __tablename__ = "sessions"
    
    session_id = Column(
        PG_UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Unique session identifier"
    )
    user_id = Column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        comment="Reference to users table"
    )
    started_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        comment="Session start timestamp"
    )
    ended_at = Column(
        DateTime(timezone=True),
        nullable=True,
        comment="Session end timestamp"
    )
    message_count = Column(
        Integer,
        default=0,
        nullable=False,
        comment="Number of messages in session"
    )
    metadata = Column(
        JSONB,
        default={},
        nullable=False,
        comment="Session metadata (JSON): idk_count, current_topic, etc."
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Whether session is currently active"
    )
    
    # Constraints
    __table_args__ = (
        Index("idx_sessions_user_id", "user_id"),
        Index("idx_sessions_started_at", "started_at"),
        Index("idx_sessions_is_active", "is_active"),
    )
    
    def __repr__(self):
        return f"<Session(session_id={self.session_id}, user_id={self.user_id}, active={self.is_active})>"


# Additional models for future sprints (commented for now)
"""
class MysterySeed(Base):
    # Sprint 2: Mystery Seed System
    pass

class TreeState(Base):
    # Sprint 2: Knowledge Tree Visualization
    pass

class Analytics(Base):
    # Sprint 3: Analytics & Monitoring
    pass

class ParentAlert(Base):
    # Sprint 3: Parent Dashboard
    pass
"""
