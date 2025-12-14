"""
Arc Completion Predictor
Forecasts missing emotional beats and identifies incomplete character transformations
"""

from typing import Dict, List, Tuple


class ArcPredictor:
    """
    Predicts arc completion and identifies missing narrative elements.
    
    Features:
    - Forecast missing emotional beats
    - Identify incomplete transformations
    - Suggest narrative fixes
    - Confidence scoring
    """
    
    # Expected emotional progression patterns for each arc type
    ARC_TEMPLATES = {
        "Hero's Journey": ["fear", "neutral", "surprise", "joy", "sadness", "anger", "joy"],
        "Redemption Arc": ["sadness", "anger", "neutral", "fear", "surprise", "joy"],
        "Fall from Grace": ["joy", "neutral", "surprise", "anger", "sadness", "fear"],
        "Coming of Age": ["fear", "surprise", "neutral", "sadness", "joy"],
        "Tragic Arc": ["joy", "neutral", "sadness", "anger", "fear"],
        "Transformation": ["neutral", "surprise", "fear", "anger", "neutral", "joy"],
        "Corruption Arc": ["neutral", "surprise", "joy", "anger", "sadness"],
        "Rags to Riches": ["sadness", "fear", "neutral", "surprise", "joy"],
        "Love Story": ["surprise", "joy", "sadness", "fear", "joy"],
        "Flat Arc": ["neutral", "neutral", "neutral", "neutral", "neutral"]
    }
    
    def predict_completion(self, character_name: str, character_arc: Dict, arc_type: str) -> Dict:
        """
        Analyze arc and predict missing elements.
        
        Returns:
        {
            "character": str,
            "arc_type": str,
            "completion_percentage": float,
            "missing_beats": [str],
            "present_beats": [str],
            "pacing_assessment": str,
            "transformation_status": str,
            "suggestions": [str],
            "confidence": float
        }
        """
        emotions_by_scene = character_arc.get("emotions_by_scene", {})
        
        # Extract emotion sequence
        scene_indices = sorted(emotions_by_scene.keys())
        actual_emotions = [
            emotions_by_scene[idx].get("emotion", "neutral") 
            for idx in scene_indices
        ]
        
        # Get expected template
        expected_template = self.ARC_TEMPLATES.get(arc_type, ["neutral"] * 5)
        
        # Calculate completion
        present_beats = set(actual_emotions)
        expected_beats = set(expected_template)
        missing_beats = expected_beats - present_beats
        
        completion = (len(present_beats) / len(expected_beats) * 100) if expected_beats else 0
        
        # Assess pacing
        pacing = self._assess_pacing(actual_emotions, scene_indices, arc_type)
        
        # Assess transformation
        transformation = self._assess_transformation(actual_emotions, arc_type)
        
        # Generate suggestions
        suggestions = self._generate_suggestions(
            missing_beats, 
            pacing, 
            transformation, 
            arc_type,
            len(actual_emotions)
        )
        
        # Calculate confidence (based on scene count and arc length)
        confidence = self._calculate_confidence(len(actual_emotions), len(expected_template))
        
        return {
            "character": character_name,
            "arc_type": arc_type,
            "completion_percentage": round(completion, 1),
            "missing_beats": sorted(list(missing_beats)),
            "present_beats": sorted(list(present_beats)),
            "pacing_assessment": pacing,
            "transformation_status": transformation,
            "suggestions": suggestions,
            "confidence": round(confidence, 2)
        }
    
    def _assess_pacing(self, emotions: List[str], scene_indices: List[int], arc_type: str) -> str:
        """Assess if emotional progression is too fast, too slow, or appropriate."""
        if len(emotions) < 3:
            return "Insufficient data (need 3+ scenes)"
        
        # Count unique emotions
        unique_emotions = len(set(emotions))
        
        # Assess based on arc type expectations
        if arc_type in ["Hero's Journey", "Redemption Arc", "Fall from Grace"]:
            # Complex arcs need more emotional variety
            if unique_emotions < 3:
                return "Too Fast - Limited emotional variety for complex arc"
            elif unique_emotions >= 5 and len(emotions) < 6:
                return "Too Fast - Too many emotional shifts in short span"
            elif unique_emotions >= 4 and len(emotions) >= 6:
                return "Well Paced - Good emotional progression"
            else:
                return "Too Slow - Arc may need more emotional development"
        
        elif arc_type == "Flat Arc":
            # Flat arcs should be consistent
            if unique_emotions <= 2:
                return "Appropriate - Consistent emotional baseline"
            else:
                return "Inconsistent - Too much variation for flat arc"
        
        else:
            # Medium complexity arcs
            if unique_emotions >= 3 and len(emotions) >= 4:
                return "Well Paced"
            elif unique_emotions < 2:
                return "Too Slow - Needs more emotional variety"
            else:
                return "Moderate Pacing"
    
    def _assess_transformation(self, emotions: List[str], arc_type: str) -> str:
        """Assess if character has undergone expected transformation."""
        if len(emotions) < 3:
            return "Insufficient data"
        
        start_emotion = emotions[0]
        end_emotion = emotions[-1]
        
        # Define expected transformations
        transformations = {
            "Hero's Journey": ("fear", "joy"),
            "Redemption Arc": (["sadness", "anger"], "joy"),
            "Fall from Grace": ("joy", ["sadness", "fear"]),
            "Coming of Age": ("fear", "joy"),
            "Rags to Riches": ("sadness", "joy"),
            "Love Story": (["neutral", "surprise"], "joy"),
            "Tragic Arc": ("joy", ["sadness", "fear"]),
            "Corruption Arc": ("neutral", ["anger", "sadness"])
        }
        
        if arc_type not in transformations:
            return "Unknown arc pattern"
        
        expected_start, expected_end = transformations[arc_type]
        
        # Handle list of acceptable emotions
        if isinstance(expected_start, list):
            start_matches = start_emotion in expected_start
        else:
            start_matches = start_emotion == expected_start
        
        if isinstance(expected_end, list):
            end_matches = end_emotion in expected_end
        else:
            end_matches = end_emotion == expected_end
        
        if start_matches and end_matches:
            return "Complete - Full transformation achieved"
        elif end_matches:
            return "Partial - Reached destination but unusual starting point"
        elif start_matches:
            return "Incomplete - Started correctly but hasn't reached expected conclusion"
        else:
            return "Divergent - Non-standard emotional journey for this arc type"
    
    def _generate_suggestions(
        self, 
        missing_beats: set, 
        pacing: str, 
        transformation: str,
        arc_type: str,
        scene_count: int
    ) -> List[str]:
        """Generate actionable narrative suggestions."""
        suggestions = []
        
        # Missing beats suggestions
        if missing_beats:
            beats_str = ", ".join(sorted(missing_beats))
            suggestions.append(f"Add scenes exploring {beats_str} to complete emotional range")
        
        # Pacing suggestions
        if "Too Fast" in pacing:
            suggestions.append("Slow down character development with more transitional scenes")
            suggestions.append("Add introspective moments between major emotional shifts")
        elif "Too Slow" in pacing:
            suggestions.append("Accelerate emotional progression with higher-stakes conflicts")
            suggestions.append("Consider combining or removing redundant scenes")
        
        # Transformation suggestions
        if "Incomplete" in transformation:
            if arc_type == "Hero's Journey":
                suggestions.append("Add triumphant resolution scene showing hero's victory")
            elif arc_type == "Redemption Arc":
                suggestions.append("Include redemptive moment showing character's change")
            elif arc_type == "Fall from Grace":
                suggestions.append("Deepen the character's downfall with darker consequences")
        
        if "Divergent" in transformation:
            suggestions.append(f"Consider reframing as different arc type if intentional departure from {arc_type}")
        
        # Scene count suggestions
        if scene_count < 3:
            suggestions.append("Add more scenes to establish clear character arc (minimum 3-4 scenes recommended)")
        
        if not suggestions:
            suggestions.append("Arc is well-structured with strong emotional progression")
        
        return suggestions
    
    def _calculate_confidence(self, actual_scenes: int, expected_beats: int) -> float:
        """
        Calculate confidence score for predictions.
        Based on scene count and data completeness.
        """
        # More scenes = higher confidence
        scene_factor = min(actual_scenes / max(expected_beats, 5), 1.0)
        
        # Penalize very short arcs
        if actual_scenes < 3:
            scene_factor *= 0.5
        
        # Base confidence: 60-95%
        confidence = 0.60 + (scene_factor * 0.35)
        
        return confidence
