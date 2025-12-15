"""
Phase 13.2: Character Interaction Heatmap
NxN matrix showing character co-occurrence in scenes
"""

from typing import Dict, List


class InteractionHeatmap:
    """
    Generate character interaction heatmap:
    - NxN matrix of character co-occurrences
    - Scene-level interaction tracking
    - Relationship intensity visualization
    """
    
    def generate_heatmap(self, emotion_data: Dict[str, Dict]) -> Dict:
        """
        Generate interaction heatmap from emotion data.
        
        Args:
            emotion_data: Character emotional progression data
        
        Returns:
            Dictionary with matrix and character list
        """
        if not emotion_data:
            return {
                "characters": [],
                "matrix": [],
                "total_interactions": 0
            }
        
        characters = sorted(emotion_data.keys())
        n = len(characters)
        
        # Initialize NxN matrix
        matrix = [[0 for _ in range(n)] for _ in range(n)]
        
        # Build scene-to-characters mapping
        scene_chars = {}
        for char_name, char_data in emotion_data.items():
            for scene in char_data.get("scenes", []):
                if scene not in scene_chars:
                    scene_chars[scene] = []
                scene_chars[scene].append(char_name)
        
        # Count co-occurrences
        for scene, chars_in_scene in scene_chars.items():
            for i, char1 in enumerate(characters):
                for j, char2 in enumerate(characters):
                    if i != j and char1 in chars_in_scene and char2 in chars_in_scene:
                        matrix[i][j] += 1
        
        # Calculate total interactions
        total_interactions = sum(sum(row) for row in matrix) // 2
        
        # Build character pairs with interaction counts
        pairs = []
        for i, char1 in enumerate(characters):
            for j, char2 in enumerate(characters):
                if i < j and matrix[i][j] > 0:
                    pairs.append({
                        "characters": [char1, char2],
                        "scenes_together": matrix[i][j],
                        "interaction_strength": self._calculate_strength(
                            matrix[i][j], scene_chars
                        )
                    })
        
        # Sort by interaction count
        pairs.sort(key=lambda x: x["scenes_together"], reverse=True)
        
        return {
            "characters": characters,
            "matrix": matrix,
            "total_interactions": total_interactions,
            "top_pairs": pairs[:5],  # Top 5 most interactive pairs
            "scene_breakdown": self._analyze_scene_breakdown(scene_chars)
        }
    
    def _calculate_strength(self, shared_scenes: int, all_scenes: Dict) -> str:
        """Calculate interaction strength category"""
        total_scenes = len(all_scenes)
        percentage = (shared_scenes / total_scenes) * 100 if total_scenes > 0 else 0
        
        if percentage >= 75:
            return "Very Strong"
        elif percentage >= 50:
            return "Strong"
        elif percentage >= 25:
            return "Moderate"
        else:
            return "Weak"
    
    def _analyze_scene_breakdown(self, scene_chars: Dict) -> Dict:
        """Analyze scene composition statistics"""
        scene_sizes = [len(chars) for chars in scene_chars.values()]
        
        return {
            "total_scenes": len(scene_chars),
            "avg_characters_per_scene": sum(scene_sizes) / len(scene_sizes) if scene_sizes else 0,
            "max_characters_in_scene": max(scene_sizes) if scene_sizes else 0,
            "min_characters_in_scene": min(scene_sizes) if scene_sizes else 0,
            "solo_scenes": sum(1 for size in scene_sizes if size == 1),
            "ensemble_scenes": sum(1 for size in scene_sizes if size >= 4)
        }


