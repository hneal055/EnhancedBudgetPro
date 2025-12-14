"""
EmotionEngine Analyzer Module
Phase 13.1: Scene & Character Emotion Analysis

Analyzes emotional patterns at scene and character levels:
- Scene intensity scores (0-100)
- Character emotional arcs across script
- Tension/pacing detection
"""

from typing import Dict, List
from .detector import get_detector
import logging

logger = logging.getLogger(__name__)


class EmotionAnalyzer:
    """Analyzes emotional patterns in scenes and characters."""
    
    def __init__(self):
        """Initialize analyzer with emotion detector."""
        self.detector = get_detector()
        logger.info("EmotionAnalyzer initialized")
    
    def analyze_scene(self, scene: Dict) -> Dict:
        """
        Analyze emotional content of a single scene.
        
        Args:
            scene: Scene dict with {heading, lines[], dialogue_lines, action_lines, characters[]}
            
        Returns:
            Dict with {
                "scene_heading": str,
                "dominant_emotion": str,
                "emotion_scores": Dict[str, float],
                "intensity": float (0-100),
                "tension": float (0-100),
                "dialogue_emotion_avg": Dict[str, float],
                "action_emotion_avg": Dict[str, float]
            }
        """
        heading = scene.get("heading", "UNKNOWN")
        lines = scene.get("lines", [])
        
        if not lines:
            return self._empty_scene_analysis(heading)
        
        # Separate dialogue and action lines
        # Handle both dict format (FDX, Fountain) and string format (plaintext)
        dialogue_lines = []
        action_lines = []
        
        for line in lines:
            if isinstance(line, dict):
                # Dict format: check type field
                if line.get("type") == "dialogue" and line.get("text", "").strip():
                    dialogue_lines.append(line)
                elif line.get("type") == "action" and line.get("text", "").strip():
                    action_lines.append(line)
            elif isinstance(line, str) and line.strip():
                # String format: treat all as dialogue
                dialogue_lines.append({"type": "dialogue", "text": line, "character": "UNKNOWN"})
        
        # Detect emotions in dialogue and action
        dialogue_emotions = []
        if dialogue_lines:
            dialogue_texts = [line["text"] for line in dialogue_lines]
            dialogue_emotions = self.detector.detect_batch(dialogue_texts)
        
        action_emotions = []
        if action_lines:
            action_texts = [line["text"] for line in action_lines]
            action_emotions = self.detector.detect_batch(action_texts)
        
        # Calculate average emotion scores across scene
        all_emotions = dialogue_emotions + action_emotions
        avg_emotion_scores = self._average_emotions(all_emotions)
        
        # Calculate dialogue and action averages separately
        dialogue_avg = self._average_emotions(dialogue_emotions) if dialogue_emotions else {}
        action_avg = self._average_emotions(action_emotions) if action_emotions else {}
        
        # Determine dominant emotion
        dominant = self.detector.get_dominant_emotion(avg_emotion_scores)
        
        # Calculate intensity (high-energy emotions = higher intensity)
        intensity = self._calculate_intensity(avg_emotion_scores)
        
        # Calculate tension (conflict emotions = higher tension)
        tension = self._calculate_tension(avg_emotion_scores)
        
        return {
            "scene_heading": heading,
            "dominant_emotion": dominant,
            "emotion_scores": avg_emotion_scores,
            "intensity": round(intensity, 2),
            "tension": round(tension, 2),
            "dialogue_emotion_avg": dialogue_avg,
            "action_emotion_avg": action_avg,
            "line_count": len(lines),
            "dialogue_count": len(dialogue_lines),
            "action_count": len(action_lines)
        }
    
    def analyze_character(self, character_name: str, scenes: List[Dict]) -> Dict:
        """
        Analyze a character's emotional arc across all scenes.
        
        Args:
            character_name: Character name to analyze
            scenes: List of scene dicts
            
        Returns:
            Dict with {
                "character": str,
                "total_scenes": int,
                "emotional_range": List[str],  # Unique emotions displayed
                "arc": List[Dict],  # Scene-by-scene emotion tracking
                "dominant_emotion": str,
                "emotional_volatility": float (0-100)
            }
        """
        character_scenes = [
            scene for scene in scenes 
            if character_name in scene.get("characters", [])
        ]
        
        if not character_scenes:
            return self._empty_character_analysis(character_name)
        
        # Track emotions scene-by-scene
        arc = []
        all_emotions_seen = set()
        
        for scene in character_scenes:
            # Get character's dialogue in this scene
            char_lines = []
            for line in scene.get("lines", []):
                if isinstance(line, dict):
                    if (line.get("type") == "dialogue" 
                        and line.get("character") == character_name
                        and line.get("text", "").strip()):
                        char_lines.append(line)
                elif isinstance(line, str) and line.strip():
                    # For string format, we can't filter by character
                    # This will be less accurate but still works
                    pass
            
            if char_lines:
                # Detect emotions in character's dialogue
                char_texts = [line["text"] for line in char_lines]
                char_emotions = self.detector.detect_batch(char_texts)
                avg_emotions = self._average_emotions(char_emotions)
                dominant = self.detector.get_dominant_emotion(avg_emotions)
                
                arc.append({
                    "scene": scene.get("heading", "UNKNOWN"),
                    "dominant_emotion": dominant,
                    "emotion_scores": avg_emotions,
                    "dialogue_lines": len(char_lines)
                })
                
                all_emotions_seen.add(dominant)
        
        # Calculate overall stats
        if arc:
            all_scene_emotions = [entry["emotion_scores"] for entry in arc]
            overall_avg = self._average_emotions(all_scene_emotions)
            overall_dominant = self.detector.get_dominant_emotion(overall_avg)
            
            # Emotional volatility = how much emotions change scene-to-scene
            volatility = self._calculate_volatility(arc)
        else:
            overall_dominant = "neutral"
            volatility = 0.0
        
        return {
            "character": character_name,
            "total_scenes": len(character_scenes),
            "scenes_with_dialogue": len(arc),
            "emotional_range": sorted(list(all_emotions_seen)),
            "arc": arc,
            "dominant_emotion": overall_dominant,
            "emotional_volatility": round(volatility, 2)
        }
    
    def _average_emotions(self, emotion_list: List[Dict[str, float]]) -> Dict[str, float]:
        """Average emotion scores across multiple detections."""
        if not emotion_list:
            return {}
        
        # Sum all scores
        emotion_sums = {}
        for emotions in emotion_list:
            for emotion, score in emotions.items():
                emotion_sums[emotion] = emotion_sums.get(emotion, 0.0) + score
        
        # Average
        count = len(emotion_list)
        return {emotion: score / count for emotion, score in emotion_sums.items()}
    
    def _calculate_intensity(self, emotion_scores: Dict[str, float]) -> float:
        """
        Calculate scene intensity (0-100) based on high-energy emotions.
        
        High-energy emotions: anger, fear, surprise, joy
        Low-energy emotions: sadness, disgust, neutral
        """
        if not emotion_scores:
            return 0.0
        
        high_energy = emotion_scores.get("anger", 0) + \
                      emotion_scores.get("fear", 0) + \
                      emotion_scores.get("surprise", 0) + \
                      emotion_scores.get("joy", 0)
        
        return high_energy * 100  # Convert to 0-100 scale
    
    def _calculate_tension(self, emotion_scores: Dict[str, float]) -> float:
        """
        Calculate scene tension (0-100) based on conflict emotions.
        
        High-tension emotions: anger, fear, disgust
        """
        if not emotion_scores:
            return 0.0
        
        tension_emotions = emotion_scores.get("anger", 0) + \
                           emotion_scores.get("fear", 0) + \
                           emotion_scores.get("disgust", 0)
        
        return tension_emotions * 100  # Convert to 0-100 scale
    
    def _calculate_volatility(self, arc: List[Dict]) -> float:
        """
        Calculate emotional volatility (0-100) = how much emotions change.
        
        Measures variance in dominant emotions across scenes.
        """
        if len(arc) < 2:
            return 0.0
        
        # Count emotion transitions
        transitions = 0
        for i in range(len(arc) - 1):
            if arc[i]["dominant_emotion"] != arc[i+1]["dominant_emotion"]:
                transitions += 1
        
        # Normalize to 0-100
        max_transitions = len(arc) - 1
        return (transitions / max_transitions) * 100 if max_transitions > 0 else 0.0
    
    def _empty_scene_analysis(self, heading: str) -> Dict:
        """Return empty scene analysis."""
        return {
            "scene_heading": heading,
            "dominant_emotion": "neutral",
            "emotion_scores": {},
            "intensity": 0.0,
            "tension": 0.0,
            "dialogue_emotion_avg": {},
            "action_emotion_avg": {},
            "line_count": 0,
            "dialogue_count": 0,
            "action_count": 0
        }
    
    def _empty_character_analysis(self, character_name: str) -> Dict:
        """Return empty character analysis."""
        return {
            "character": character_name,
            "total_scenes": 0,
            "scenes_with_dialogue": 0,
            "emotional_range": [],
            "arc": [],
            "dominant_emotion": "neutral",
            "emotional_volatility": 0.0
        }
