"""
Relationship Evolution Tracker
Tracks character relationships over time with turning point detection
"""

from typing import Dict, List, Tuple
import math


class RelationshipTracker:
    """
    Analyzes relationship dynamics between characters across scenes.
    
    Features:
    - Track relationship evolution over time
    - Identify relationship turning points
    - Calculate relationship strength/sentiment
    - Detect relationship types (ally, conflict, romantic, neutral)
    """
    
    # Emotion compatibility matrix (how emotions align in relationships)
    EMOTION_COMPATIBILITY = {
        "joy": {"joy": 1.0, "surprise": 0.6, "neutral": 0.4, "fear": -0.2, "sadness": -0.4, "anger": -0.6},
        "surprise": {"joy": 0.6, "surprise": 0.8, "neutral": 0.3, "fear": 0.2, "sadness": 0.0, "anger": -0.3},
        "neutral": {"joy": 0.4, "surprise": 0.3, "neutral": 0.5, "fear": 0.2, "sadness": 0.1, "anger": 0.0},
        "fear": {"joy": -0.2, "surprise": 0.2, "neutral": 0.2, "fear": 0.7, "sadness": 0.4, "anger": 0.3},
        "sadness": {"joy": -0.4, "surprise": 0.0, "neutral": 0.1, "fear": 0.4, "sadness": 0.6, "anger": 0.2},
        "anger": {"joy": -0.6, "surprise": -0.3, "neutral": 0.0, "fear": 0.3, "sadness": 0.2, "anger": 0.5}
    }
    
    def track_relationship(
        self, 
        char1_name: str, 
        char1_arc: Dict,
        char2_name: str,
        char2_arc: Dict
    ) -> Dict:
        """
        Track relationship evolution between two characters.
        
        Returns:
        {
            "characters": (str, str),
            "shared_scenes": [int],
            "sentiment_trajectory": [float],  # -1 to 1 per scene
            "relationship_strength": float,  # 0 to 1
            "relationship_type": str,
            "turning_points": [dict],
            "evolution_summary": str,
            "network_data": dict  # For graph visualization
        }
        """
        # Get shared scenes
        char1_scenes = set(char1_arc.get("scenes", []))
        char2_scenes = set(char2_arc.get("scenes", []))
        shared_scenes = sorted(list(char1_scenes.intersection(char2_scenes)))
        
        if not shared_scenes:
            return {
                "characters": (char1_name, char2_name),
                "shared_scenes": [],
                "sentiment_trajectory": [],
                "relationship_strength": 0.0,
                "relationship_type": "No Interaction",
                "turning_points": [],
                "evolution_summary": "Characters do not share any scenes",
                "network_data": {}
            }
        
        # Calculate sentiment for each shared scene
        char1_emotions = char1_arc.get("emotions_by_scene", {})
        char2_emotions = char2_arc.get("emotions_by_scene", {})
        
        sentiment_trajectory = []
        for scene_idx in shared_scenes:
            e1 = char1_emotions.get(scene_idx, {}).get("emotion", "neutral")
            e2 = char2_emotions.get(scene_idx, {}).get("emotion", "neutral")
            
            # Calculate compatibility score for this scene
            compatibility = self.EMOTION_COMPATIBILITY.get(e1, {}).get(e2, 0.0)
            sentiment_trajectory.append(compatibility)
        
        # Calculate overall relationship strength
        avg_sentiment = sum(sentiment_trajectory) / len(sentiment_trajectory)
        interaction_frequency = len(shared_scenes) / max(len(char1_scenes), len(char2_scenes))
        relationship_strength = (abs(avg_sentiment) + interaction_frequency) / 2
        
        # Classify relationship type
        relationship_type = self._classify_relationship(avg_sentiment, sentiment_trajectory)
        
        # Detect turning points
        turning_points = self._detect_turning_points(
            shared_scenes, 
            sentiment_trajectory,
            char1_emotions,
            char2_emotions
        )
        
        # Generate evolution summary
        evolution_summary = self._generate_evolution_summary(
            char1_name,
            char2_name,
            sentiment_trajectory,
            turning_points,
            relationship_type
        )
        
        # Prepare network graph data
        network_data = {
            "nodes": [
                {"id": char1_name, "label": char1_name, "color": "#FF6B6B"},
                {"id": char2_name, "label": char2_name, "color": "#4ECDC4"}
            ],
            "edges": [
                {
                    "from": char1_name,
                    "to": char2_name,
                    "weight": relationship_strength,
                    "sentiment": avg_sentiment,
                    "label": f"{len(shared_scenes)} scenes"
                }
            ]
        }
        
        return {
            "characters": (char1_name, char2_name),
            "shared_scenes": shared_scenes,
            "sentiment_trajectory": [round(s, 2) for s in sentiment_trajectory],
            "relationship_strength": round(relationship_strength, 2),
            "relationship_type": relationship_type,
            "turning_points": turning_points,
            "evolution_summary": evolution_summary,
            "network_data": network_data
        }
    
    def track_all_relationships(self, character_arcs: Dict) -> Dict:
        """
        Track all relationships in the script.
        
        Returns network graph data with all character relationships.
        """
        characters = list(character_arcs.keys())
        relationships = []
        
        # Calculate all pairwise relationships
        for i, char1 in enumerate(characters):
            for char2 in characters[i+1:]:
                rel = self.track_relationship(
                    char1,
                    character_arcs[char1],
                    char2,
                    character_arcs[char2]
                )
                if rel["shared_scenes"]:  # Only include if they interact
                    relationships.append(rel)
        
        # Build network graph
        nodes = [{"id": char, "label": char} for char in characters]
        edges = []
        
        for rel in relationships:
            char1, char2 = rel["characters"]
            edges.append({
                "from": char1,
                "to": char2,
                "weight": rel["relationship_strength"],
                "sentiment": sum(rel["sentiment_trajectory"]) / len(rel["sentiment_trajectory"]),
                "interactions": len(rel["shared_scenes"])
            })
        
        return {
            "nodes": nodes,
            "edges": edges,
            "relationships": relationships
        }
    
    def _classify_relationship(self, avg_sentiment: float, trajectory: List[float]) -> str:
        """Classify relationship based on sentiment patterns."""
        if not trajectory:
            return "Undefined"
        
        # Check trajectory pattern
        start_sentiment = trajectory[0]
        end_sentiment = trajectory[-1]
        volatility = self._calculate_volatility(trajectory)
        
        # Strong positive relationship
        if avg_sentiment > 0.5:
            return "Strong Alliance"
        
        # Positive trending
        elif avg_sentiment > 0.2:
            if end_sentiment > start_sentiment + 0.3:
                return "Growing Bond"
            else:
                return "Friendly Alliance"
        
        # Romantic pattern (starts neutral/positive, builds)
        elif len(trajectory) >= 3 and start_sentiment < 0.3 and end_sentiment > 0.5:
            return "Romantic Development"
        
        # Strong negative
        elif avg_sentiment < -0.4:
            return "Antagonistic"
        
        # Negative trending
        elif avg_sentiment < -0.1:
            if end_sentiment < start_sentiment - 0.3:
                return "Deteriorating Relationship"
            else:
                return "Conflict"
        
        # High volatility
        elif volatility > 0.5:
            return "Complicated/Volatile"
        
        # Neutral/stable
        else:
            return "Neutral"
    
    def _detect_turning_points(
        self, 
        scenes: List[int], 
        trajectory: List[float],
        char1_emotions: Dict,
        char2_emotions: Dict
    ) -> List[Dict]:
        """Detect significant shifts in relationship."""
        turning_points = []
        
        if len(trajectory) < 2:
            return turning_points
        
        for i in range(1, len(trajectory)):
            delta = trajectory[i] - trajectory[i-1]
            
            # Significant shift threshold
            if abs(delta) > 0.5:
                scene_idx = scenes[i]
                e1 = char1_emotions.get(scene_idx, {}).get("emotion", "neutral")
                e2 = char2_emotions.get(scene_idx, {}).get("emotion", "neutral")
                
                turning_points.append({
                    "scene": scene_idx,
                    "shift": round(delta, 2),
                    "type": "Positive Shift" if delta > 0 else "Negative Shift",
                    "emotions": (e1, e2),
                    "description": self._describe_turning_point(delta, e1, e2)
                })
        
        return turning_points
    
    def _describe_turning_point(self, delta: float, e1: str, e2: str) -> str:
        """Generate human-readable description of turning point."""
        if delta > 0:
            return f"Relationship improves ({e1} + {e2})"
        else:
            return f"Relationship deteriorates ({e1} + {e2})"
    
    def _generate_evolution_summary(
        self,
        char1: str,
        char2: str,
        trajectory: List[float],
        turning_points: List[Dict],
        rel_type: str
    ) -> str:
        """Generate narrative summary of relationship evolution."""
        if not trajectory:
            return f"{char1} and {char2} do not interact"
        
        start = trajectory[0]
        end = trajectory[-1]
        
        # Start state
        if start > 0.3:
            start_desc = "begin with a positive connection"
        elif start < -0.3:
            start_desc = "begin in conflict"
        else:
            start_desc = "start as acquaintances"
        
        # Evolution
        if len(turning_points) > 0:
            evolution_desc = f"with {len(turning_points)} significant turning point(s)"
        else:
            evolution_desc = "with a stable dynamic"
        
        # End state
        if end > 0.5:
            end_desc = "reaching a strong alliance"
        elif end > 0.2:
            end_desc = "developing a positive bond"
        elif end < -0.3:
            end_desc = "ending in antagonism"
        else:
            end_desc = "maintaining neutrality"
        
        return f"{char1} and {char2} {start_desc}, {evolution_desc}, {end_desc}."
    
    def _calculate_volatility(self, trajectory: List[float]) -> float:
        """Calculate relationship volatility (0-1)."""
        if len(trajectory) < 2:
            return 0.0
        
        # Standard deviation of changes
        changes = [abs(trajectory[i] - trajectory[i-1]) for i in range(1, len(trajectory))]
        if not changes:
            return 0.0
        
        avg_change = sum(changes) / len(changes)
        return min(avg_change * 2, 1.0)  # Scale to 0-1
