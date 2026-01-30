"""
============================================
EchoMind AI - Mastery Service
Sprint 2: Concept Mastery Tracking
============================================

This service manages student mastery levels for concepts:
- Retrieves mastery level for a given concept
- Updates mastery based on interaction quality
- Caches mastery data in Redis for performance
- Tracks interaction count and timestamps

User Story: US-2.2 (Mastery Level Retrieval)
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class MasteryLevel(str, Enum):
    """Mastery level enumeration"""
    EXPOSURE = "exposure"          # Just introduced to concept
    UNDERSTANDING = "understanding"  # Demonstrates basic understanding
    MASTERY = "mastery"            # Deep understanding, can explain

class MasteryService:
    """
    Manages concept mastery tracking and updates
    """
    
    def __init__(self, db_session=None, redis_client=None):
        """
        Initialize Mastery Service
        
        Args:
            db_session: SQLAlchemy database session (optional for Sprint 2)
            redis_client: Redis client for caching (optional for Sprint 2)
        """
        self.db = db_session
        self.redis = redis_client
        self.cache_ttl = 3600  # 1 hour cache TTL
        
        # In-memory fallback for Sprint 2 (before DB is fully connected)
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        
        logger.info("✅ Mastery Service initialized")
    
    def get_mastery(
        self,
        user_id: str,
        concept_name: str
    ) -> Dict[str, Any]:
        """
        Get mastery level for a user and concept
        
        Args:
            user_id: User UUID
            concept_name: Concept name (e.g., "multiplication", "photosynthesis")
        
        Returns:
            Dictionary with:
                - mastery_level: Current mastery level
                - interaction_count: Number of interactions
                - last_interaction: Last interaction timestamp
                - confidence_score: 1-5 score
        """
        cache_key = f"mastery:{user_id}:{concept_name}"
        
        # Try Redis cache first
        if self.redis:
            try:
                cached = self.redis.get(cache_key)
                if cached:
                    logger.info(f"✅ Mastery cache hit | user={user_id} | concept={concept_name}")
                    import json
                    return json.loads(cached)
            except Exception as e:
                logger.warning(f"Redis cache error: {e}")
        
        # Try in-memory cache (Sprint 2 fallback)
        if cache_key in self._memory_cache:
            logger.info(f"✅ Memory cache hit | user={user_id} | concept={concept_name}")
            return self._memory_cache[cache_key]
        
        # Try database
        if self.db:
            try:
                mastery_record = self._get_from_db(user_id, concept_name)
                if mastery_record:
                    self._cache_mastery(cache_key, mastery_record)
                    return mastery_record
            except Exception as e:
                logger.error(f"Database error: {e}")
        
        # No record found - create new with default values
        logger.info(f"📝 Creating new mastery record | user={user_id} | concept={concept_name}")
        new_record = self._create_default_mastery(user_id, concept_name)
        self._cache_mastery(cache_key, new_record)
        
        return new_record
    
    def update_mastery(
        self,
        user_id: str,
        concept_name: str,
        interaction_quality: int,
        demonstrated_understanding: bool = False
    ) -> Dict[str, Any]:
        """
        Update mastery level based on interaction
        
        Args:
            user_id: User UUID
            concept_name: Concept name
            interaction_quality: Quality score 1-5
                1: Struggled significantly
                2: Needed lots of help
                3: Moderate understanding
                4: Good understanding
                5: Excellent understanding
            demonstrated_understanding: Whether student explained their reasoning
        
        Returns:
            Updated mastery record
        """
        # Get current mastery
        current = self.get_mastery(user_id, concept_name)
        
        # Update interaction count
        new_interaction_count = current["interaction_count"] + 1
        
        # Calculate new confidence score (weighted average)
        current_score = current["confidence_score"]
        weight = 0.3  # Weight for new interaction
        new_score = (current_score * (1 - weight)) + (interaction_quality * weight)
        new_score = round(new_score, 2)
        
        # Determine new mastery level
        new_mastery_level = self._calculate_mastery_level(
            current_level=current["mastery_level"],
            confidence_score=new_score,
            interaction_count=new_interaction_count,
            demonstrated_understanding=demonstrated_understanding
        )
        
        # Build updated record
        updated_record = {
            "user_id": user_id,
            "concept_name": concept_name,
            "mastery_level": new_mastery_level,
            "interaction_count": new_interaction_count,
            "confidence_score": new_score,
            "last_interaction": datetime.utcnow().isoformat(),
            "level_changed": new_mastery_level != current["mastery_level"]
        }
        
        # Save to database (if available)
        if self.db:
            try:
                self._save_to_db(updated_record)
            except Exception as e:
                logger.error(f"Failed to save to database: {e}")
        
        # Update cache
        cache_key = f"mastery:{user_id}:{concept_name}"
        self._cache_mastery(cache_key, updated_record)
        
        logger.info(
            f"📊 Mastery updated | "
            f"user={user_id} | "
            f"concept={concept_name} | "
            f"level={new_mastery_level} | "
            f"score={new_score} | "
            f"count={new_interaction_count}"
        )
        
        return updated_record
    
    def _calculate_mastery_level(
        self,
        current_level: str,
        confidence_score: float,
        interaction_count: int,
        demonstrated_understanding: bool
    ) -> str:
        """
        Calculate new mastery level based on performance
        
        Args:
            current_level: Current mastery level
            confidence_score: Confidence score (1-5)
            interaction_count: Total interactions
            demonstrated_understanding: Whether student explained reasoning
        
        Returns:
            New mastery level
        """
        # Progression rules:
        # exposure -> understanding: score >= 3.5, count >= 3, demonstrated understanding
        # understanding -> mastery: score >= 4.5, count >= 5, demonstrated understanding
        
        if current_level == MasteryLevel.EXPOSURE:
            if (confidence_score >= 3.5 and 
                interaction_count >= 3 and 
                demonstrated_understanding):
                return MasteryLevel.UNDERSTANDING
        
        elif current_level == MasteryLevel.UNDERSTANDING:
            if (confidence_score >= 4.5 and 
                interaction_count >= 5 and 
                demonstrated_understanding):
                return MasteryLevel.MASTERY
        
        # Can also regress if score drops significantly
        if current_level == MasteryLevel.MASTERY and confidence_score < 3.0:
            return MasteryLevel.UNDERSTANDING
        
        if current_level == MasteryLevel.UNDERSTANDING and confidence_score < 2.0:
            return MasteryLevel.EXPOSURE
        
        return current_level
    
    def _create_default_mastery(
        self,
        user_id: str,
        concept_name: str
    ) -> Dict[str, Any]:
        """Create default mastery record for new concept"""
        return {
            "user_id": user_id,
            "concept_name": concept_name,
            "mastery_level": MasteryLevel.EXPOSURE,
            "interaction_count": 0,
            "confidence_score": 1.0,
            "last_interaction": datetime.utcnow().isoformat(),
            "level_changed": False
        }
    
    def _cache_mastery(
        self,
        cache_key: str,
        mastery_record: Dict[str, Any]
    ):
        """Cache mastery record in Redis and memory"""
        # Memory cache (always available)
        self._memory_cache[cache_key] = mastery_record
        
        # Redis cache (if available)
        if self.redis:
            try:
                import json
                self.redis.setex(
                    cache_key,
                    self.cache_ttl,
                    json.dumps(mastery_record)
                )
            except Exception as e:
                logger.warning(f"Failed to cache in Redis: {e}")
    
    def _get_from_db(
        self,
        user_id: str,
        concept_name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get mastery record from database
        
        Note: This is a placeholder for Sprint 2.
        Full database integration will be completed when DB is connected.
        """
        # TODO: Implement database query when DB is connected
        # query = self.db.query(ConceptMastery).filter_by(
        #     user_id=user_id,
        #     concept_name=concept_name
        # ).first()
        return None
    
    def _save_to_db(
        self,
        mastery_record: Dict[str, Any]
    ):
        """
        Save mastery record to database
        
        Note: This is a placeholder for Sprint 2.
        Full database integration will be completed when DB is connected.
        """
        # TODO: Implement database save when DB is connected
        # mastery = ConceptMastery(**mastery_record)
        # self.db.add(mastery)
        # self.db.commit()
        pass


# Singleton instance
_mastery_service_instance: Optional[MasteryService] = None


def get_mastery_service(db_session=None, redis_client=None) -> MasteryService:
    """
    Get or create Mastery Service singleton instance
    
    Args:
        db_session: Database session (optional)
        redis_client: Redis client (optional)
    
    Returns:
        MasteryService instance
    """
    global _mastery_service_instance
    
    if _mastery_service_instance is None:
        _mastery_service_instance = MasteryService(db_session, redis_client)
    
    return _mastery_service_instance
