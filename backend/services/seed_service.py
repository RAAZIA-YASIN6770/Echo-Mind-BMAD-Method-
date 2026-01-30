"""
============================================
EchoMind AI - Mystery Seed Service
Sprint 3: Gamification Engine
============================================

This service manages the Mystery Seed system:
- Assigns a random seed type to new users
- Tracks seed growth based on learning progress
- Defines growth requirements for each seed type

User Story: US-8.1 (Mystery Seed Assignment)
"""

import random
import logging
from typing import Dict, Any, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class SeedType(Enum):
    """Mystery Seed Types - each aligned with a learning category"""
    PRISM = "prism"          # Math & Logic
    CORAL = "coral"          # Science & Nature
    MATH = "math"            # Pure Mathematics
    NEBULA = "nebula"        # Language & Creativity


class MysterySeeds:
    """
    Mystery Seed definitions with growth requirements
    """
    
    SEED_DATA = {
        SeedType.PRISM: {
            "name": "Prism Seed",
            "emoji": "💎",
            "description": "A crystalline seed that refracts light into rainbows. Grows when you solve puzzles and think logically.",
            "primary_category": "math",
            "secondary_categories": ["logic"],
            "growth_stages": [
                {"stage": 1, "name": "Tiny Crystal", "emoji": "✨", "points_required": 0},
                {"stage": 2, "name": "Growing Prism", "emoji": "💠", "points_required": 50},
                {"stage": 3, "name": "Rainbow Prism", "emoji": "🔷", "points_required": 150},
                {"stage": 4, "name": "Brilliant Prism", "emoji": "💎", "points_required": 300},
                {"stage": 5, "name": "Master Prism", "emoji": "🌟", "points_required": 500},
            ],
            "special_ability": "Reveals hidden patterns in problems",
            "fun_fact": "Prism Seeds are said to be formed from frozen starlight!"
        },
        
        SeedType.CORAL: {
            "name": "Coral Seed",
            "emoji": "🪸",
            "description": "A living seed from the ocean depths. Grows when you explore science and nature.",
            "primary_category": "science",
            "secondary_categories": ["nature", "biology"],
            "growth_stages": [
                {"stage": 1, "name": "Tiny Polyp", "emoji": "🌱", "points_required": 0},
                {"stage": 2, "name": "Growing Coral", "emoji": "🌿", "points_required": 50},
                {"stage": 3, "name": "Branching Coral", "emoji": "🌳", "points_required": 150},
                {"stage": 4, "name": "Reef Coral", "emoji": "🪸", "points_required": 300},
                {"stage": 5, "name": "Master Reef", "emoji": "🏝️", "points_required": 500},
            ],
            "special_ability": "Discovers connections between living things",
            "fun_fact": "Coral Seeds can communicate with sea creatures!"
        },
        
        SeedType.MATH: {
            "name": "Math Seed",
            "emoji": "🔢",
            "description": "A numerical seed that pulses with equations. Grows when you master numbers and calculations.",
            "primary_category": "math",
            "secondary_categories": ["arithmetic", "algebra"],
            "growth_stages": [
                {"stage": 1, "name": "Number Sprout", "emoji": "1️⃣", "points_required": 0},
                {"stage": 2, "name": "Equation Vine", "emoji": "➕", "points_required": 50},
                {"stage": 3, "name": "Formula Tree", "emoji": "🔢", "points_required": 150},
                {"stage": 4, "name": "Theorem Tower", "emoji": "📐", "points_required": 300},
                {"stage": 5, "name": "Master Calculator", "emoji": "🧮", "points_required": 500},
            ],
            "special_ability": "Solves complex equations instantly",
            "fun_fact": "Math Seeds are rumored to contain the secrets of infinity!"
        },
        
        SeedType.NEBULA: {
            "name": "Nebula Seed",
            "emoji": "🌌",
            "description": "A cosmic seed swirling with stardust. Grows when you create stories and express yourself.",
            "primary_category": "language",
            "secondary_categories": ["creativity", "writing"],
            "growth_stages": [
                {"stage": 1, "name": "Star Dust", "emoji": "✨", "points_required": 0},
                {"stage": 2, "name": "Cosmic Cloud", "emoji": "☁️", "points_required": 50},
                {"stage": 3, "name": "Swirling Nebula", "emoji": "🌀", "points_required": 150},
                {"stage": 4, "name": "Galaxy Nebula", "emoji": "🌌", "points_required": 300},
                {"stage": 5, "name": "Master Universe", "emoji": "🌠", "points_required": 500},
            ],
            "special_ability": "Weaves words into magical stories",
            "fun_fact": "Nebula Seeds are born from the dreams of ancient poets!"
        }
    }


class SeedService:
    """
    Service for managing Mystery Seeds
    """
    
    def __init__(self):
        """Initialize Seed Service"""
        logger.info("✅ Seed Service initialized")
    
    def assign_random_seed(self, user_id: int) -> Dict[str, Any]:
        """
        Assign a random Mystery Seed to a new user
        
        Args:
            user_id: User's ID
        
        Returns:
            Dictionary with seed assignment details
        """
        # Randomly select a seed type
        seed_type = random.choice(list(SeedType))
        seed_data = MysterySeeds.SEED_DATA[seed_type]
        
        logger.info(f"🌱 Assigned {seed_data['name']} to user {user_id}")
        
        return {
            "user_id": user_id,
            "seed_type": seed_type.value,
            "seed_name": seed_data["name"],
            "seed_emoji": seed_data["emoji"],
            "description": seed_data["description"],
            "current_stage": 1,
            "current_stage_name": seed_data["growth_stages"][0]["name"],
            "current_stage_emoji": seed_data["growth_stages"][0]["emoji"],
            "total_points": 0,
            "next_stage_points": seed_data["growth_stages"][1]["points_required"],
            "special_ability": seed_data["special_ability"],
            "fun_fact": seed_data["fun_fact"],
            "assigned_at": datetime.utcnow().isoformat()
        }
    
    def get_seed_info(self, seed_type: str) -> Dict[str, Any]:
        """
        Get complete information about a seed type
        
        Args:
            seed_type: Seed type (prism/coral/math/nebula)
        
        Returns:
            Complete seed data
        """
        try:
            seed_enum = SeedType(seed_type)
            return MysterySeeds.SEED_DATA[seed_enum]
        except ValueError:
            logger.error(f"❌ Invalid seed type: {seed_type}")
            return None
    
    def calculate_growth_stage(
        self,
        seed_type: str,
        total_points: int
    ) -> Dict[str, Any]:
        """
        Calculate current growth stage based on points
        
        Args:
            seed_type: Seed type
            total_points: Total points earned
        
        Returns:
            Current stage information
        """
        seed_data = self.get_seed_info(seed_type)
        if not seed_data:
            return None
        
        # Find current stage
        current_stage = 1
        for stage in seed_data["growth_stages"]:
            if total_points >= stage["points_required"]:
                current_stage = stage["stage"]
            else:
                break
        
        # Get current and next stage info
        current_stage_data = seed_data["growth_stages"][current_stage - 1]
        next_stage_data = None
        if current_stage < len(seed_data["growth_stages"]):
            next_stage_data = seed_data["growth_stages"][current_stage]
        
        return {
            "current_stage": current_stage,
            "current_stage_name": current_stage_data["name"],
            "current_stage_emoji": current_stage_data["emoji"],
            "total_points": total_points,
            "next_stage_name": next_stage_data["name"] if next_stage_data else "MAX LEVEL",
            "next_stage_points": next_stage_data["points_required"] if next_stage_data else total_points,
            "points_to_next_stage": (next_stage_data["points_required"] - total_points) if next_stage_data else 0,
            "progress_percentage": self._calculate_progress_percentage(
                total_points,
                current_stage_data["points_required"],
                next_stage_data["points_required"] if next_stage_data else total_points
            ),
            "is_max_level": current_stage == len(seed_data["growth_stages"])
        }
    
    def _calculate_progress_percentage(
        self,
        current_points: int,
        stage_start: int,
        stage_end: int
    ) -> float:
        """
        Calculate progress percentage within current stage
        
        Args:
            current_points: Current total points
            stage_start: Points required for current stage
            stage_end: Points required for next stage
        
        Returns:
            Progress percentage (0-100)
        """
        if stage_end == stage_start:
            return 100.0
        
        points_in_stage = current_points - stage_start
        points_needed = stage_end - stage_start
        
        percentage = (points_in_stage / points_needed) * 100
        return min(max(percentage, 0.0), 100.0)
    
    def award_points(
        self,
        seed_type: str,
        current_points: int,
        points_to_add: int,
        reason: str
    ) -> Dict[str, Any]:
        """
        Award points and check for level up
        
        Args:
            seed_type: Seed type
            current_points: Current total points
            points_to_add: Points to award
            reason: Reason for awarding points
        
        Returns:
            Award result with level up info
        """
        old_stage = self.calculate_growth_stage(seed_type, current_points)
        new_total = current_points + points_to_add
        new_stage = self.calculate_growth_stage(seed_type, new_total)
        
        leveled_up = new_stage["current_stage"] > old_stage["current_stage"]
        
        logger.info(
            f"🎁 Awarded {points_to_add} points | "
            f"Reason: {reason} | "
            f"Level up: {leveled_up}"
        )
        
        return {
            "points_awarded": points_to_add,
            "new_total_points": new_total,
            "reason": reason,
            "leveled_up": leveled_up,
            "old_stage": old_stage["current_stage"],
            "new_stage": new_stage["current_stage"],
            "new_stage_name": new_stage["current_stage_name"],
            "new_stage_emoji": new_stage["current_stage_emoji"],
            "celebration_message": self._get_celebration_message(
                new_stage["current_stage_name"]
            ) if leveled_up else None
        }
    
    def _get_celebration_message(self, stage_name: str) -> str:
        """
        Get celebration message for level up
        
        Args:
            stage_name: Name of new stage
        
        Returns:
            Celebration message
        """
        messages = [
            f"🎉 Amazing! Your seed grew into a {stage_name}!",
            f"🌟 Incredible growth! You've reached {stage_name}!",
            f"✨ Wow! Your seed evolved into a {stage_name}!",
            f"🎊 Fantastic! Welcome to the {stage_name} stage!",
        ]
        return random.choice(messages)


# Singleton instance
_seed_service_instance: Optional[SeedService] = None


def get_seed_service() -> SeedService:
    """
    Get or create Seed Service singleton instance
    
    Returns:
        SeedService instance
    """
    global _seed_service_instance
    
    if _seed_service_instance is None:
        _seed_service_instance = SeedService()
    
    return _seed_service_instance
