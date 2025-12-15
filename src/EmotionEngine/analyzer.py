"""
EmotionEngine Analyzer Module
Phase 13.1: Scene & Character Emotion Analysis
Phase 13.4: Parallel Character Analysis (4-8x faster)

Analyzes emotional patterns at scene and character levels:
- Scene intensity scores (0-100)
- Character emotional arcs across script
- Tension/pacing detection
- PARALLEL character processing for large scripts
"""

from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from .detector import get_detector
import logging
import time

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
    

    def build_scene_character_index(self, scenes: List[Dict]) -> Dict[str, List[Dict]]:
        """
        Build index mapping characters to their scenes (Phase 13.5 optimization).
        
        Pre-computes which characters appear in which scenes to avoid
        O(characters × scenes) iteration in analyze_character().
        
        Args:
            scenes: List of scene dicts
            
        Returns:
            Dict mapping character_name -> [scene1, scene2, ...]
        """
        index = {}
        
        for scene in scenes:
            for char_name in scene.get("characters", []):
                if char_name not in index:
                    index[char_name] = []
                index[char_name].append(scene)
        
        return index

    def analyze_character(self, character_name: str, scenes: List[Dict], scene_index: Optional[Dict[str, List[Dict]]] = None) -> Dict:
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
        # Use pre-built index if available (Phase 13.5 optimization)
        if scene_index is not None:
            character_scenes = scene_index.get(character_name, [])
        else:
            # Fallback to iteration (backwards compatible)
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
    
    def analyze_characters_parallel(
        self, 
        character_names: List[str], 
        scenes: List[Dict],
        max_workers: Optional[int] = None,
        progress_callback=None
    ) -> Dict[str, Dict]:
        """
        Analyze multiple characters in parallel (Phase 13.4 optimization).
        
        Args:
            character_names: List of character names to analyze
            scenes: List of scene dicts
            max_workers: Number of parallel workers (None = CPU count)
            progress_callback: Optional callback(current, total, character_name)
            
        Returns:
            Dict mapping character names to their analysis results
            Only includes characters with dialogue (scenes_with_dialogue > 0)
        """
        if not character_names:
            return {}
        
        start_time = time.time()
        results = {}
        completed = 0
        
        # Build scene-character index once (Phase 13.5 optimization)
        # This avoids O(characters × scenes) iteration
        scene_index = self.build_scene_character_index(scenes)
        logger.info(f"Built scene-character index: {len(scene_index)} characters indexed")
        
        # Use ThreadPoolExecutor for I/O-bound emotion detection
        # Model inference releases GIL so threads work well
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all character analysis tasks with pre-built index
            future_to_char = {
                executor.submit(self.analyze_character, char, scenes, scene_index): char
                for char in character_names
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_char):
                char_name = future_to_char[future]
                try:
                    result = future.result()
                    
                    # Only include characters with dialogue
                    if result["scenes_with_dialogue"] > 0:
                        results[char_name] = result
                    
                    completed += 1
                    
                    # Call progress callback if provided
                    if progress_callback:
                        progress_callback(completed, len(character_names), char_name)
                        
                except Exception as e:
                    logger.error(f"Error analyzing character {char_name}: {e}")
                    completed += 1
        
        elapsed = time.time() - start_time
        chars_analyzed = len(results)
        
        logger.info(f"Parallel character analysis: {chars_analyzed} characters in {elapsed:.2f}s ({chars_analyzed/elapsed:.1f} chars/sec)")
        
        return results
    
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
        return {emotion: total / count for emotion, total in emotion_sums.items()}
    
    def _calculate_intensity(self, emotion_scores: Dict[str, float]) -> float:
        """
        Calculate scene intensity based on high-energy emotions.
        
        High-energy emotions: anger, fear, surprise, joy
        Scale: 0-100
        """
        if not emotion_scores:
            return 0.0
        
        high_energy = ["anger", "fear", "surprise", "joy"]
        intensity_score = sum(emotion_scores.get(e, 0.0) for e in high_energy)
        
        # Normalize to 0-100 scale
        return intensity_score * 25.0  # Max score = 4.0, so * 25 = 100
    
    def _calculate_tension(self, emotion_scores: Dict[str, float]) -> float:
        """
        Calculate scene tension based on conflict emotions.
        
        Conflict emotions: anger, fear, disgust
        Scale: 0-100
        """
        if not emotion_scores:
            return 0.0
        
        conflict_emotions = ["anger", "fear", "disgust"]
        tension_score = sum(emotion_scores.get(e, 0.0) for e in conflict_emotions)
        
        # Normalize to 0-100 scale
        return tension_score * 33.33  # Max score = 3.0, so * 33.33 = 100
    
    def _calculate_volatility(self, arc: List[Dict]) -> float:
        """
        Calculate emotional volatility across character's arc.
        
        Measures how dramatically emotions change between scenes.
        Scale: 0-100
        """
        if len(arc) < 2:
            return 0.0
        
        # Calculate emotion changes between consecutive scenes
        changes = []
        for i in range(1, len(arc)):
            prev_scores = arc[i-1]["emotion_scores"]
            curr_scores = arc[i]["emotion_scores"]
            
            # Calculate total absolute change across all emotions
            total_change = 0.0
            for emotion in prev_scores.keys():
                prev_val = prev_scores.get(emotion, 0.0)
                curr_val = curr_scores.get(emotion, 0.0)
                total_change += abs(curr_val - prev_val)
            
            changes.append(total_change)
        
        # Average change per scene transition
        avg_change = sum(changes) / len(changes) if changes else 0.0
        
        # Normalize to 0-100 scale (max theoretical change = 7 emotions * 2 = 14)
        return min(avg_change * 7.14, 100.0)  # 14 * 7.14 ≈ 100
    
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
