"""
EmotionEngine Arc Tracker Module
Phase 13.1: Character Emotional Journey Tracking

Tracks character emotional journeys and identifies key moments:
- Emotional turning points
- Character transformation detection
- Relationship dynamics
"""

from typing import Dict, List, Tuple
import logging

logger = logging.getLogger(__name__)


class ArcTracker:
    """Tracks character emotional arcs and identifies key story moments."""
    
    def identify_turning_points(self, character_arc: Dict) -> List[Dict]:
        """
        Identify emotional turning points in a character's arc.
        
        Turning points = scenes where emotion significantly changes from previous scene.
        
        Args:
            character_arc: Output from EmotionAnalyzer.analyze_character()
            
        Returns:
            List of turning point dicts with {
                "scene": str,
                "from_emotion": str,
                "to_emotion": str,
                "impact": float (0-100)
            }
        """
        arc = character_arc.get("arc", [])
        
        if len(arc) < 2:
            return []
        
        turning_points = []
        
        for i in range(1, len(arc)):
            prev_scene = arc[i-1]
            curr_scene = arc[i]
            
            prev_emotion = prev_scene["dominant_emotion"]
            curr_emotion = curr_scene["dominant_emotion"]
            
            # Turning point if emotion changed
            if prev_emotion != curr_emotion:
                # Calculate impact = how different the emotions are
                impact = self._calculate_emotion_distance(
                    prev_scene["emotion_scores"],
                    curr_scene["emotion_scores"]
                )
                
                turning_points.append({
                    "scene": curr_scene["scene"],
                    "from_emotion": prev_emotion,
                    "to_emotion": curr_emotion,
                    "impact": round(impact, 2)
                })
        
        # Sort by impact (highest first)
        turning_points.sort(key=lambda x: x["impact"], reverse=True)
        
        return turning_points
    
    def detect_character_transformation(self, character_arc: Dict) -> Dict:
        """
        Detect if character undergoes major emotional transformation.
        
        Transformation = significant difference between start and end emotions.
        
        Args:
            character_arc: Output from EmotionAnalyzer.analyze_character()
            
        Returns:
            Dict with {
                "transformed": bool,
                "start_emotion": str,
                "end_emotion": str,
                "transformation_degree": float (0-100),
                "journey_type": str  # "positive", "negative", "cyclical", "stable"
            }
        """
        arc = character_arc.get("arc", [])
        
        if len(arc) < 2:
            return {
                "transformed": False,
                "start_emotion": "neutral",
                "end_emotion": "neutral",
                "transformation_degree": 0.0,
                "journey_type": "stable"
            }
        
        start_scene = arc[0]
        end_scene = arc[-1]
        
        start_emotion = start_scene["dominant_emotion"]
        end_emotion = end_scene["dominant_emotion"]
        
        # Calculate transformation degree
        transformation_degree = self._calculate_emotion_distance(
            start_scene["emotion_scores"],
            end_scene["emotion_scores"]
        )
        
        # Significant transformation if > 30% change
        transformed = transformation_degree > 30
        
        # Determine journey type
        journey_type = self._classify_journey(start_emotion, end_emotion, arc)
        
        return {
            "transformed": transformed,
            "start_emotion": start_emotion,
            "end_emotion": end_emotion,
            "transformation_degree": round(transformation_degree, 2),
            "journey_type": journey_type
        }
    
    def analyze_relationship_dynamics(
        self, 
        char1_arc: Dict, 
        char2_arc: Dict
    ) -> Dict:
        """
        Analyze emotional dynamics between two characters.
        
        Tracks how characters' emotions align or conflict across shared scenes.
        
        Args:
            char1_arc: Character 1's emotional arc
            char2_arc: Character 2's emotional arc
            
        Returns:
            Dict with {
                "shared_scenes": int,
                "emotional_alignment": float (0-100),  # How similar emotions are
                "conflict_moments": List[Dict],  # Scenes with opposing emotions
                "harmony_moments": List[Dict],  # Scenes with aligned emotions
                "relationship_type": str  # "supportive", "antagonistic", "complex", "distant"
            }
        """
        arc1 = {scene["scene"]: scene for scene in char1_arc.get("arc", [])}
        arc2 = {scene["scene"]: scene for scene in char2_arc.get("arc", [])}
        
        # Find shared scenes
        shared_scene_headings = set(arc1.keys()) & set(arc2.keys())
        
        if not shared_scene_headings:
            return {
                "shared_scenes": 0,
                "emotional_alignment": 0.0,
                "conflict_moments": [],
                "harmony_moments": [],
                "relationship_type": "distant"
            }
        
        conflict_moments = []
        harmony_moments = []
        alignment_scores = []
        
        for scene_heading in shared_scene_headings:
            scene1 = arc1[scene_heading]
            scene2 = arc2[scene_heading]
            
            # Calculate alignment (0=opposite, 100=identical)
            alignment = self._calculate_emotion_similarity(
                scene1["emotion_scores"],
                scene2["emotion_scores"]
            )
            alignment_scores.append(alignment)
            
            # High conflict if opposing emotions
            if alignment < 40:
                conflict_moments.append({
                    "scene": scene_heading,
                    "char1_emotion": scene1["dominant_emotion"],
                    "char2_emotion": scene2["dominant_emotion"],
                    "conflict_level": round(100 - alignment, 2)
                })
            
            # High harmony if similar emotions
            elif alignment > 70:
                harmony_moments.append({
                    "scene": scene_heading,
                    "char1_emotion": scene1["dominant_emotion"],
                    "char2_emotion": scene2["dominant_emotion"],
                    "harmony_level": round(alignment, 2)
                })
        
        # Calculate average alignment
        avg_alignment = sum(alignment_scores) / len(alignment_scores)
        
        # Classify relationship
        relationship_type = self._classify_relationship(
            avg_alignment, 
            len(conflict_moments), 
            len(harmony_moments)
        )
        
        return {
            "shared_scenes": len(shared_scene_headings),
            "emotional_alignment": round(avg_alignment, 2),
            "conflict_moments": sorted(conflict_moments, key=lambda x: x["conflict_level"], reverse=True),
            "harmony_moments": sorted(harmony_moments, key=lambda x: x["harmony_level"], reverse=True),
            "relationship_type": relationship_type
        }
    
    def _calculate_emotion_distance(
        self, 
        emotions1: Dict[str, float], 
        emotions2: Dict[str, float]
    ) -> float:
        """
        Calculate distance between two emotion distributions (0-100).
        
        Uses Euclidean distance normalized to 0-100 scale.
        """
        if not emotions1 or not emotions2:
            return 0.0
        
        # Get all emotion keys
        all_emotions = set(emotions1.keys()) | set(emotions2.keys())
        
        # Calculate squared differences
        squared_diffs = []
        for emotion in all_emotions:
            score1 = emotions1.get(emotion, 0.0)
            score2 = emotions2.get(emotion, 0.0)
            squared_diffs.append((score1 - score2) ** 2)
        
        # Euclidean distance
        distance = (sum(squared_diffs) ** 0.5)
        
        # Normalize to 0-100 (max possible distance is sqrt(2) ≈ 1.414 for probabilities)
        normalized = (distance / 1.414) * 100
        
        return min(normalized, 100.0)
    
    def _calculate_emotion_similarity(
        self, 
        emotions1: Dict[str, float], 
        emotions2: Dict[str, float]
    ) -> float:
        """
        Calculate similarity between two emotion distributions (0-100).
        
        100 = identical, 0 = completely different
        """
        distance = self._calculate_emotion_distance(emotions1, emotions2)
        return 100 - distance
    
    def _classify_journey(self, start: str, end: str, arc: List[Dict]) -> str:
        """
        Classify character's emotional journey type.
        
        Types:
        - positive: Moves from negative to positive emotions
        - negative: Moves from positive to negative emotions
        - cyclical: Ends where it started
        - stable: Minimal emotional change
        """
        if start == end:
            return "cyclical"
        
        positive_emotions = {"joy", "surprise"}
        negative_emotions = {"anger", "fear", "sadness", "disgust"}
        
        start_valence = "positive" if start in positive_emotions else "negative"
        end_valence = "positive" if end in positive_emotions else "negative"
        
        if start_valence == "negative" and end_valence == "positive":
            return "positive"
        elif start_valence == "positive" and end_valence == "negative":
            return "negative"
        else:
            return "stable"
    
    def _classify_relationship(
        self, 
        avg_alignment: float, 
        conflict_count: int, 
        harmony_count: int
    ) -> str:
        """
        Classify relationship type based on emotional patterns.
        
        Types:
        - supportive: High alignment, many harmony moments
        - antagonistic: Low alignment, many conflict moments
        - complex: Mix of conflict and harmony
        - distant: Few shared emotional moments
        """
        if avg_alignment > 70 and harmony_count > conflict_count:
            return "supportive"
        elif avg_alignment < 40 and conflict_count > harmony_count:
            return "antagonistic"
        elif conflict_count > 0 and harmony_count > 0:
            return "complex"
        else:
            return "distant"
