from typing import Dict, List


class ProductionSchedulerEngine:
    """
    Converts scene + cost data into a structured shooting schedule.
    """

    def generate_schedule(
        self,
        scenes: List[Dict],
        character_costs: Dict[str, Dict]
    ) -> Dict:

        schedule = []
        total_burn = 0
        peak = {"day": 0, "cost": 0}
        danger_days = []

        shoot_day = 1

        for scene in scenes:

            scene_cost = 0
            for char in scene["characters"]:
                if char in character_costs:
                    scene_cost += character_costs[char]["daily_rate"]

            schedule.append({
                "shoot_day": shoot_day,
                "scene": scene.get("heading", scene.get("header", "<unknown>")),
                "characters": scene["characters"],
                "daily_burn": scene_cost
            })

            total_burn += scene_cost

            if scene_cost > peak["cost"]:
                peak = {
                    "day": shoot_day,
                    "scene": scene.get("heading", scene.get("header", "<unknown>")),
                    "cost": scene_cost
                }

            shoot_day += 1

        average_burn = round(total_burn / len(schedule), 2) if schedule else 0

        for day in schedule:
            if day["daily_burn"] > average_burn * 1.25:
                danger_days.append(day)

        return {
            "daily_schedule": schedule,
            "average_daily_burn": average_burn,
            "peak_burn_day": peak,
            "danger_days": danger_days
        }
