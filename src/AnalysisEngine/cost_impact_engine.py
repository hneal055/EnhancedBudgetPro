from collections import defaultdict
from typing import Dict


class CharacterCostImpactEngine:
    """
    Computes:
    - Approximate cost weight per character
    - Shooting day clustering recommendations
    """

    def analyze(self, character_stats: Dict, daily_cast_rates: Dict, shoot_days: int):
        """
        character_stats → output from CharacterIntelligenceEngine
        daily_cast_rates → {"JOHN": 1200, "ELIJAH": 800, ...}
        shoot_days → total shoot days
        """

        cost_impact = {}
        total_cost = 0

        # -------------------------------
        # COST IMPACT PER CHARACTER
        # -------------------------------
        for character, stats in character_stats.items():
            daily_rate = daily_cast_rates.get(character, 500)  # default fallback rate
            estimated_days = max(1, stats["scenes"])

            character_cost = daily_rate * estimated_days
            cost_impact[character] = {
                "daily_rate": daily_rate,
                "estimated_days": estimated_days,
                "estimated_total_cost": character_cost
            }

            total_cost += character_cost

        # -------------------------------
        # SHOOT DAY CLUSTERING (BY SCENES)
        # -------------------------------
        clusters = defaultdict(list)

        for character, stats in character_stats.items():
            clusters[stats["scenes"]].append(character)

        return {
            "character_costs": cost_impact,
            "total_estimated_cast_cost": total_cost,
            "shoot_clusters": dict(clusters)
        }
