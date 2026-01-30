"""
============================================
EchoMind AI - Knowledge Tree Health Service
Sprint 3: Gamification Engine
============================================

This service manages the Knowledge Tree visualization:
- Calculates Tree Health based on concept mastery
- Tracks branch growth per category
- Provides visual state for frontend rendering

User Story: US-7.1 (Knowledge Tree State)
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum

logger = logging.getLogger(__name__)


class MasteryLevel(Enum):
    """Mastery levels for concepts"""
    EXPOSURE = "exposure"           # 0-25%
    DEVELOPING = "developing"       # 26-50%
    PROFICIENT = "proficient"       # 51-75%
    MASTERY = "mastery"            # 76-100%


class TreeHealthService:
    """
    Service for calculating and managing Knowledge Tree health
    """
    
    # Category-to-Branch mapping
    CATEGORY_BRANCHES = {
        "math": {
            "name": "Mathematics Branch",
            "emoji": "🔢",
            "color": "#4A90E2",  # Blue
            "description": "Numbers, equations, and logical thinking"
        },
        "science": {
            "name": "Science Branch",
            "emoji": "🔬",
            "color": "#50C878",  # Green
            "description": "Experiments, nature, and discovery"
        },
        "logic": {
            "name": "Logic Branch",
            "emoji": "🧩",
            "color": "#9B59B6",  # Purple
            "description": "Puzzles, reasoning, and problem-solving"
        },
        "language": {
            "name": "Language Branch",
            "emoji": "📚",
            "color": "#E74C3C",  # Red
            "description": "Words, stories, and communication"
        },
        "general": {
            "name": "General Knowledge Branch",
            "emoji": "🌍",
            "color": "#F39C12",  # Orange
            "description": "Curiosity and exploration"
        }
    }
    
    def __init__(self):
        """Initialize Tree Health Service"""
        logger.info("✅ Tree Health Service initialized")
    
    def calculate_tree_health(
        self,
        concept_mastery_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate overall tree health from concept mastery data
        
        Args:
            concept_mastery_data: List of concept mastery records
                Each record should have:
                - concept_id: str
                - category: str
                - mastery_score: float (0-100)
                - attempts: int
                - last_interaction: datetime
        
        Returns:
            Tree health data with overall health and branch details
        """
        if not concept_mastery_data:
            return self._get_empty_tree_state()
        
        # Group concepts by category
        category_data = self._group_by_category(concept_mastery_data)
        
        # Calculate branch health for each category
        branches = {}
        total_health = 0
        total_concepts = 0
        
        for category, concepts in category_data.items():
            branch_health = self._calculate_branch_health(concepts)
            branches[category] = {
                **self.CATEGORY_BRANCHES.get(category, self.CATEGORY_BRANCHES["general"]),
                **branch_health
            }
            total_health += branch_health["health_score"]
            total_concepts += len(concepts)
        
        # Calculate overall tree health (average of all branches)
        num_branches = len(branches)
        overall_health = total_health / num_branches if num_branches > 0 else 0
        
        # Determine tree state
        tree_state = self._determine_tree_state(overall_health)
        
        return {
            "overall_health": round(overall_health, 2),
            "tree_state": tree_state,
            "total_concepts": total_concepts,
            "total_branches": num_branches,
            "branches": branches,
            "last_updated": datetime.utcnow().isoformat(),
            "growth_tips": self._get_growth_tips(branches, overall_health)
        }
    
    def _group_by_category(
        self,
        concept_mastery_data: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Group concept mastery data by category
        
        Args:
            concept_mastery_data: List of concept mastery records
        
        Returns:
            Dictionary mapping category to list of concepts
        """
        grouped = {}
        for concept in concept_mastery_data:
            category = concept.get("category", "general")
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(concept)
        return grouped
    
    def _calculate_branch_health(
        self,
        concepts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Calculate health metrics for a single branch
        
        Args:
            concepts: List of concepts in this category
        
        Returns:
            Branch health metrics
        """
        if not concepts:
            return {
                "health_score": 0,
                "concept_count": 0,
                "mastery_distribution": {
                    "exposure": 0,
                    "developing": 0,
                    "proficient": 0,
                    "mastery": 0
                },
                "average_mastery": 0,
                "growth_stage": "seedling"
            }
        
        # Calculate average mastery
        total_mastery = sum(c.get("mastery_score", 0) for c in concepts)
        avg_mastery = total_mastery / len(concepts)
        
        # Count mastery distribution
        mastery_dist = {
            "exposure": 0,
            "developing": 0,
            "proficient": 0,
            "mastery": 0
        }
        
        for concept in concepts:
            score = concept.get("mastery_score", 0)
            level = self._get_mastery_level(score)
            mastery_dist[level.value] += 1
        
        # Calculate health score (0-100)
        # Weighted: mastery concepts worth more than exposure
        health_score = (
            mastery_dist["exposure"] * 25 +
            mastery_dist["developing"] * 50 +
            mastery_dist["proficient"] * 75 +
            mastery_dist["mastery"] * 100
        ) / len(concepts)
        
        # Determine growth stage
        growth_stage = self._determine_growth_stage(health_score)
        
        return {
            "health_score": round(health_score, 2),
            "concept_count": len(concepts),
            "mastery_distribution": mastery_dist,
            "average_mastery": round(avg_mastery, 2),
            "growth_stage": growth_stage,
            "growth_stage_emoji": self._get_growth_stage_emoji(growth_stage)
        }
    
    def _get_mastery_level(self, score: float) -> MasteryLevel:
        """
        Convert mastery score to mastery level
        
        Args:
            score: Mastery score (0-100)
        
        Returns:
            MasteryLevel enum
        """
        if score < 25:
            return MasteryLevel.EXPOSURE
        elif score < 50:
            return MasteryLevel.DEVELOPING
        elif score < 75:
            return MasteryLevel.PROFICIENT
        else:
            return MasteryLevel.MASTERY
    
    def _determine_growth_stage(self, health_score: float) -> str:
        """
        Determine branch growth stage based on health score
        
        Args:
            health_score: Branch health score (0-100)
        
        Returns:
            Growth stage name
        """
        if health_score < 20:
            return "seedling"
        elif health_score < 40:
            return "sprout"
        elif health_score < 60:
            return "sapling"
        elif health_score < 80:
            return "young_tree"
        else:
            return "mighty_tree"
    
    def _get_growth_stage_emoji(self, growth_stage: str) -> str:
        """
        Get emoji for growth stage
        
        Args:
            growth_stage: Growth stage name
        
        Returns:
            Emoji representing the stage
        """
        emojis = {
            "seedling": "🌱",
            "sprout": "🌿",
            "sapling": "🌳",
            "young_tree": "🌲",
            "mighty_tree": "🌳✨"
        }
        return emojis.get(growth_stage, "🌱")
    
    def _determine_tree_state(self, overall_health: float) -> str:
        """
        Determine overall tree state
        
        Args:
            overall_health: Overall tree health (0-100)
        
        Returns:
            Tree state description
        """
        if overall_health < 20:
            return "Just planted! 🌱"
        elif overall_health < 40:
            return "Growing strong! 🌿"
        elif overall_health < 60:
            return "Flourishing! 🌳"
        elif overall_health < 80:
            return "Thriving! 🌲"
        else:
            return "Magnificent! ✨🌳✨"
    
    def _get_growth_tips(
        self,
        branches: Dict[str, Any],
        overall_health: float
    ) -> List[str]:
        """
        Generate personalized growth tips
        
        Args:
            branches: Branch health data
            overall_health: Overall tree health
        
        Returns:
            List of growth tips
        """
        tips = []
        
        # Find weakest branch
        if branches:
            weakest_branch = min(
                branches.items(),
                key=lambda x: x[1]["health_score"]
            )
            
            if weakest_branch[1]["health_score"] < 50:
                tips.append(
                    f"💡 Your {weakest_branch[1]['name']} needs some love! "
                    f"Try exploring more {weakest_branch[0]} topics."
                )
        
        # Find strongest branch
        if branches:
            strongest_branch = max(
                branches.items(),
                key=lambda x: x[1]["health_score"]
            )
            
            if strongest_branch[1]["health_score"] > 70:
                tips.append(
                    f"🌟 Amazing work on {strongest_branch[1]['name']}! "
                    f"You're becoming a master!"
                )
        
        # Overall encouragement
        if overall_health < 30:
            tips.append("🌱 Keep going! Every question helps your tree grow!")
        elif overall_health > 70:
            tips.append("✨ Your Knowledge Tree is thriving! Keep up the great work!")
        
        return tips
    
    def _get_empty_tree_state(self) -> Dict[str, Any]:
        """
        Get initial empty tree state for new users
        
        Returns:
            Empty tree state
        """
        return {
            "overall_health": 0,
            "tree_state": "Ready to grow! 🌱",
            "total_concepts": 0,
            "total_branches": 0,
            "branches": {},
            "last_updated": datetime.utcnow().isoformat(),
            "growth_tips": [
                "🌱 Welcome! Ask your first question to start growing your Knowledge Tree!",
                "💡 The more you explore, the stronger your tree becomes!",
                "🎯 Try questions in different categories to grow all your branches!"
            ]
        }
    
    def get_branch_visualization_data(
        self,
        category: str,
        concepts: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Get visualization data for a specific branch
        
        Args:
            category: Category name
            concepts: List of concepts in this category
        
        Returns:
            Visualization-ready data for frontend
        """
        branch_info = self.CATEGORY_BRANCHES.get(category, self.CATEGORY_BRANCHES["general"])
        branch_health = self._calculate_branch_health(concepts)
        
        return {
            "category": category,
            "name": branch_info["name"],
            "emoji": branch_info["emoji"],
            "color": branch_info["color"],
            "description": branch_info["description"],
            **branch_health,
            "concepts": [
                {
                    "concept_id": c.get("concept_id"),
                    "mastery_score": c.get("mastery_score", 0),
                    "mastery_level": self._get_mastery_level(c.get("mastery_score", 0)).value,
                    "attempts": c.get("attempts", 0)
                }
                for c in concepts
            ]
        }


# Singleton instance
_tree_health_service_instance: Optional[TreeHealthService] = None


def get_tree_health_service() -> TreeHealthService:
    """
    Get or create Tree Health Service singleton instance
    
    Returns:
        TreeHealthService instance
    """
    global _tree_health_service_instance
    
    if _tree_health_service_instance is None:
        _tree_health_service_instance = TreeHealthService()
    
    return _tree_health_service_instance
