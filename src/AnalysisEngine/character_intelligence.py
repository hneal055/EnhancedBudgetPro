from collections import defaultdict
from typing import Dict


class CharacterIntelligenceEngine:
    """
    Computes advanced character analytics for:
    - Scene frequency
    - Dialogue density
    - Estimated screen time
    - Cast weight rankings
    """

    def analyze(self, parsed_data: Dict) -> Dict:
        scenes = parsed_data.get("scenes", [])

        character_stats = defaultdict(lambda: {
            "scenes": 0,
            "dialogue_lines": 0,
            "estimated_screen_time_min": 0.0
        })

        for scene_index, scene in enumerate(scenes, start=1):
            characters = scene.get("characters", [])
            dialogue_lines = scene.get("dialogue_lines", 0)

            for character in characters:
                character_stats[character]["scenes"] += 1
                character_stats[character]["dialogue_lines"] += dialogue_lines

        # Estimate screen time (rule: ~15 dialogue lines ≈ 1 minute)
        for character, stats in character_stats.items():
            stats["estimated_screen_time_min"] = round(
                stats["dialogue_lines"] / 15, 2
            )

        # Rank characters by importance
        rankings = sorted(
            character_stats.items(),
            key=lambda x: (x[1]["scenes"], x[1]["dialogue_lines"]),
            reverse=True
        )

        return {
            "character_stats": dict(character_stats),
            "top_characters": rankings[:5]
        }
