# burn_rate_engine.py — Phase 2.6 Scheduling & Burn Rate Forecasting

from typing import Dict, List


class BurnRateForecastEngine:
    """
    Computes:
    ✅ Per-scene cost
    ✅ Estimated daily burn rate
    ✅ Peak burn day
    ✅ Budget volatility risk days
    """

    def analyze(
        self,
        scenes: List[Dict],
        character_costs: Dict
    ) -> Dict:

        daily_schedule = []
        total_cost = 0
        peak_day = {"day": 0, "scene": None, "cost": 0}

        for day_index, scene in enumerate(scenes, start=1):

            day_cost = 0
            day_characters = scene["characters"]

            for character in day_characters:
                if character in character_costs:
                    day_cost += character_costs[character]["estimated_total_cost"]

            daily_schedule.append({
                "shoot_day": day_index,
                "scene": scene.get("heading", scene.get("header", "<unknown>")),
                "characters": day_characters,
                "daily_burn": day_cost
            })

            total_cost += day_cost

            if day_cost > peak_day["cost"]:
                peak_day = {
                    "day": day_index,
                    "scene": scene.get("heading", scene.get("header", "<unknown>")),
                    "cost": day_cost
                }

        avg_daily_burn = round(total_cost / max(1, len(daily_schedule)), 2)

        danger_days = [
            day for day in daily_schedule
            if day["daily_burn"] >= avg_daily_burn * 1.25
        ]

        return {
            "daily_schedule": daily_schedule,
            "average_daily_burn": avg_daily_burn,
            "peak_burn_day": peak_day,
            "danger_days": danger_days,
        }
