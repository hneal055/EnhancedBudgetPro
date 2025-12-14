"""
Phase 13.2: Arc Type Classification Engine
Automatically identify character arc patterns based on emotional trajectories
"""

from typing import Dict, List, Optional, Tuple
import math


class ArcClassifier:
    """
    Classifies character arcs into standard storytelling patterns:
    - Hero's Journey (transformation arc)
    - Redemption Arc (negative to positive)
    - Fall from Grace (positive to negative)
    - Coming of Age (growth arc)
    - Steadfast Arc (consistent despite pressure)
    - Flat Arc (minimal change)
    """
    
    # Arc type definitions with pattern signatures
    ARC_TYPES = {
        "hero_journey": {
            "name": "Hero's Journey",
            "description": "Transformation through challenge (Campbell's monomyth)",
            "pattern": "stable → crisis → growth → return",
            "emoji": "🦸"
        },
        "redemption": {
            "name": "Redemption Arc",
            "description": "Negative to positive transformation",
            "pattern": "flawed → crisis → growth → redemption",
            "emoji": "✨"
        },
        "fall": {
            "name": "Fall from Grace",
            "description": "Positive to negative corruption",
            "pattern": "noble → temptation → corruption → downfall",
            "emoji": "⚡"
        },
        "coming_of_age": {
            "name": "Coming of Age",
            "description": "Growth from innocence to maturity",
            "pattern": "innocent → trial → maturity → self-discovery",
            "emoji": "🌱"
        },
        "steadfast": {
            "name": "Steadfast Arc",
            "description": "Consistent values despite pressure",
            "pattern": "stable → pressure → resistance → triumph",
            "emoji": "🛡️"
        },
        "flat": {
            "name": "Flat Arc",
            "description": "Minimal character change (changes world instead)",
            "pattern": "consistent throughout",
            "emoji": "⚖️"
        }
    }
    
    def classify_arc(self, character_arc: Dict) -> Dict:
        """
        Classify a character's arc based on emotional trajectory.
        
        Args:
            character_arc: Character arc data from EmotionEngine
                {
                    "total_scenes": int,
                    "emotional_volatility": float,
                    "dominant_emotion": str,
                    "emotional_range": List[str],
                    "arc": List[Dict]  # Scene-by-scene emotions
                }
        
        Returns:
            {
                "arc_type": str,
                "arc_name": str,
                "confidence": float (0-100),
                "description": str,
                "pattern": str,
                "emoji": str,
                "metrics": Dict
            }
        """
        arc_scenes = character_arc.get("arc", [])
        
        if len(arc_scenes) < 3:
            return self._insufficient_data_result()
        
        # Calculate arc metrics
        metrics = self._calculate_arc_metrics(arc_scenes, character_arc)
        
        # Score each arc type
        scores = {
            "hero_journey": self._score_hero_journey(metrics),
            "redemption": self._score_redemption(metrics),
            "fall": self._score_fall(metrics),
            "coming_of_age": self._score_coming_of_age(metrics),
            "steadfast": self._score_steadfast(metrics),
            "flat": self._score_flat(metrics)
        }
        
        # Get best match
        best_arc_type = max(scores, key=scores.get)
        confidence = min(scores[best_arc_type], 100)
        
        arc_info = self.ARC_TYPES[best_arc_type]
        
        return {
            "arc_type": best_arc_type,
            "arc_name": arc_info["name"],
            "confidence": confidence,
            "description": arc_info["description"],
            "pattern": arc_info["pattern"],
            "emoji": arc_info["emoji"],
            "metrics": metrics,
            "all_scores": scores
        }
    
    def _calculate_arc_metrics(self, arc_scenes: List[Dict], character_arc: Dict) -> Dict:
        """Calculate key metrics for arc classification"""
        
        # Extract intensities over time
        intensities = [s.get("intensity", 0) for s in arc_scenes]
        tensions = [s.get("tension", 0) for s in arc_scenes]
        
        # Calculate trajectory (direction of change)
        first_third_intensity = sum(intensities[:len(intensities)//3]) / max(len(intensities)//3, 1)
        last_third_intensity = sum(intensities[-len(intensities)//3:]) / max(len(intensities)//3, 1)
        intensity_delta = last_third_intensity - first_third_intensity
        
        # Tension trajectory
        first_third_tension = sum(tensions[:len(tensions)//3]) / max(len(tensions)//3, 1)
        last_third_tension = sum(tensions[-len(tensions)//3:]) / max(len(tensions)//3, 1)
        tension_delta = last_third_tension - first_third_tension
        
        # Volatility (from character arc)
        volatility = character_arc.get("emotional_volatility", 0)
        
        # Emotional range (diversity of emotions)
        emotional_range = character_arc.get("emotional_range", [])
        range_diversity = len(emotional_range)
        
        # Dominant emotion
        dominant = character_arc.get("dominant_emotion", "neutral")
        
        # Peak intensity location (early, middle, late)
        if intensities:
            peak_idx = intensities.index(max(intensities))
            peak_location = peak_idx / len(intensities)  # 0.0-1.0
        else:
            peak_location = 0.5
        
        return {
            "intensity_delta": intensity_delta,
            "tension_delta": tension_delta,
            "volatility": volatility,
            "range_diversity": range_diversity,
            "dominant_emotion": dominant,
            "peak_location": peak_location,
            "avg_intensity": sum(intensities) / len(intensities) if intensities else 0,
            "avg_tension": sum(tensions) / len(tensions) if tensions else 0
        }
    
    def _score_hero_journey(self, metrics: Dict) -> float:
        """
        Hero's Journey: High volatility, peak in middle, positive intensity delta
        """
        score = 0.0
        
        # High volatility (transformation)
        if metrics["volatility"] > 50:
            score += 30
        elif metrics["volatility"] > 30:
            score += 15
        
        # Peak in middle (crisis/ordeal)
        if 0.3 < metrics["peak_location"] < 0.7:
            score += 25
        
        # Positive intensity delta (growth)
        if metrics["intensity_delta"] > 10:
            score += 20
        elif metrics["intensity_delta"] > 0:
            score += 10
        
        # Emotional range (diverse experiences)
        if metrics["range_diversity"] >= 4:
            score += 15
        elif metrics["range_diversity"] >= 3:
            score += 10
        
        # Moderate tension increase
        if 0 < metrics["tension_delta"] < 20:
            score += 10
        
        return score
    
    def _score_redemption(self, metrics: Dict) -> float:
        """
        Redemption: Negative start emotions, high volatility, positive delta
        """
        score = 0.0
        
        # Negative dominant emotion
        negative_emotions = ["anger", "sadness", "disgust", "fear"]
        if metrics["dominant_emotion"] in negative_emotions:
            score += 25
        
        # Strong positive intensity delta
        if metrics["intensity_delta"] > 20:
            score += 30
        elif metrics["intensity_delta"] > 10:
            score += 15
        
        # High volatility (major change)
        if metrics["volatility"] > 60:
            score += 25
        elif metrics["volatility"] > 40:
            score += 15
        
        # Tension decrease (resolution)
        if metrics["tension_delta"] < -10:
            score += 15
        
        # Emotional range (transformation)
        if metrics["range_diversity"] >= 4:
            score += 5
        
        return score
    
    def _score_fall(self, metrics: Dict) -> float:
        """
        Fall from Grace: Positive start, negative delta, increasing tension
        """
        score = 0.0
        
        # Positive dominant emotion initially
        positive_emotions = ["joy", "surprise"]
        if metrics["dominant_emotion"] in positive_emotions:
            score += 20
        
        # Negative intensity delta (corruption)
        if metrics["intensity_delta"] < -20:
            score += 30
        elif metrics["intensity_delta"] < -10:
            score += 15
        
        # Increasing tension (conflict)
        if metrics["tension_delta"] > 15:
            score += 25
        elif metrics["tension_delta"] > 5:
            score += 10
        
        # High volatility
        if metrics["volatility"] > 50:
            score += 15
        
        # Range diversity
        if metrics["range_diversity"] >= 4:
            score += 10
        
        return score
    
    def _score_coming_of_age(self, metrics: Dict) -> float:
        """
        Coming of Age: Moderate volatility, growth pattern, peak late
        """
        score = 0.0
        
        # Moderate volatility (gradual growth)
        if 30 < metrics["volatility"] < 60:
            score += 25
        
        # Positive intensity delta (maturation)
        if metrics["intensity_delta"] > 10:
            score += 25
        elif metrics["intensity_delta"] > 5:
            score += 15
        
        # Peak in latter half (climax/realization)
        if metrics["peak_location"] > 0.6:
            score += 20
        
        # Emotional range (learning experiences)
        if metrics["range_diversity"] >= 3:
            score += 15
        
        # Moderate tension
        if 20 < metrics["avg_tension"] < 60:
            score += 15
        
        return score
    
    def _score_steadfast(self, metrics: Dict) -> float:
        """
        Steadfast: Low volatility, consistent tension, minimal delta
        """
        score = 0.0
        
        # Low volatility (consistency)
        if metrics["volatility"] < 30:
            score += 35
        elif metrics["volatility"] < 50:
            score += 20
        
        # Minimal intensity delta
        if abs(metrics["intensity_delta"]) < 10:
            score += 25
        
        # High sustained tension (external pressure)
        if metrics["avg_tension"] > 50:
            score += 20
        
        # Low emotional range (focus)
        if metrics["range_diversity"] <= 3:
            score += 15
        
        # Peak early or consistent (not transformative)
        if metrics["peak_location"] < 0.3 or metrics["peak_location"] > 0.7:
            score += 5
        
        return score
    
    def _score_flat(self, metrics: Dict) -> float:
        """
        Flat Arc: Very low volatility, minimal change, consistent emotions
        """
        score = 0.0
        
        # Very low volatility
        if metrics["volatility"] < 20:
            score += 40
        elif metrics["volatility"] < 35:
            score += 25
        
        # Minimal intensity delta
        if abs(metrics["intensity_delta"]) < 5:
            score += 30
        
        # Minimal tension delta
        if abs(metrics["tension_delta"]) < 5:
            score += 15
        
        # Low emotional range
        if metrics["range_diversity"] <= 2:
            score += 15
        
        return score
    
    def _insufficient_data_result(self) -> Dict:
        """Return default result when insufficient data"""
        return {
            "arc_type": "insufficient_data",
            "arc_name": "Insufficient Data",
            "confidence": 0,
            "description": "Not enough scenes to classify arc",
            "pattern": "N/A",
            "emoji": "❓",
            "metrics": {},
            "all_scores": {}
        }
    
    def classify_all_characters(self, character_arcs: Dict[str, Dict]) -> Dict[str, Dict]:
        """
        Classify arcs for all characters
        
        Args:
            character_arcs: Dictionary of character arc data
        
        Returns:
            Dictionary mapping character name to classification result
        """
        classifications = {}
        
        for character, arc_data in character_arcs.items():
            classifications[character] = self.classify_arc(arc_data)
        
        return classifications
