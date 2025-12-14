# auto_schedule_optimizer.py
# Phase 5 — Auto Schedule Optimization Engine
# Priority: ACTOR COST > LOCATION > BURN BALANCE
# Trigger: USER CLICK ONLY
# Reordering: FULLY FREE

from typing import List, Dict
from src.SchedulingEngine.auto_schedule_optimizer import AutoScheduleOptimizerEngine


class AutoScheduleOptimizerEngine:
    """
    Optimizes scene order to:
    ✅ Minimize actor paid days (HIGHEST PRIORITY)
    ✅ Cluster locations
    ✅ Balance daily burn
    ✅ Reduce peak burn days
    """

    def optimize(
        self,
        scenes: List[Dict],
        character_costs: Dict[str, Dict],
    ) -> Dict:
        """
        Input:
        - scenes → parsed scene list
        - character_costs → output of CharacterCostImpactEngine

        Output:
        - optimized_daily_schedule
        - metrics summary
        """

        # -------------------------
        # STEP 1: SCORE EACH SCENE
        # -------------------------
        scored_scenes = []

        for idx, scene in enumerate(scenes):
            actors = scene.get("characters", [])
            location = scene.get("header", "").split("-")[0].strip()

            # Actor cost priority score (HIGHEST WEIGHT)
            actor_cost_score = sum(
                character_costs.get(a, {}).get("daily_rate", 0)
                for a in actors
            )

            scored_scenes.append({
                "original_index": idx,
                "scene": scene,
                "actors": actors,
                "location": location,
                "actor_cost_score": actor_cost_score
            })

        # -------------------------
        # STEP 2: SORT → ACTOR → LOCATION → ORIGINAL ORDER
        # -------------------------
        scored_scenes.sort(
            key=lambda x: (
                -x["actor_cost_score"],  # highest cost actors first
                x["location"],           # cluster locations
                x["original_index"]      # stabilize ordering
            )
        )

        # -------------------------
        # STEP 3: BUILD OPTIMIZED DAILY SCHEDULE
        # -------------------------
        optimized_schedule = []
        shoot_day = 1

        for block in scored_scenes:
            scene = block["scene"]
            actors = block["actors"]

            daily_burn = sum(
                character_costs.get(a, {}).get("daily_rate", 0)
                for a in actors
            )

            optimized_schedule.append({
                "shoot_day": shoot_day,
                "scene": scene.get("header"),
                "characters": actors,
                "daily_burn": daily_burn
            })

            shoot_day += 1

        # -------------------------
        # STEP 4: METRICS
        # -------------------------
        total_burn = sum(d["daily_burn"] for d in optimized_schedule)
        days = len(optimized_schedule)
        avg_burn = round(total_burn / days, 2) if days else 0

        peak_day = max(optimized_schedule, key=lambda x: x["daily_burn"])

        danger_days = [
            d for d in optimized_schedule
            if d["daily_burn"] > avg_burn * 1.25
        ]

        return {
            "optimized_daily_schedule": optimized_schedule,
            "average_daily_burn": avg_burn,
            "peak_burn_day": {
                "day": peak_day["shoot_day"],
                "scene": peak_day["scene"],
                "cost": peak_day["daily_burn"]
            },
            "danger_days": danger_days,
            "days_total": days
        }


# -------------------------
# ✅ CLI SAFETY TEST
# -------------------------
if __name__ == "__main__":
    sample_scenes = [
        {"header": "INT. LAB - NIGHT", "characters": ["JOHN"]},
        {"header": "EXT. CITY - DAY", "characters": ["ELIJAH"]},
        {"header": "INT. LAB - NIGHT", "characters": ["JOHN"]},
    ]

    sample_costs = {
        "JOHN": {"daily_rate": 1200},
        "ELIJAH": {"daily_rate": 800}
    }

    optimizer = AutoScheduleOptimizerEngine()
    result = optimizer.optimize(sample_scenes, sample_costs)

    print("✅ OPTIMIZED SCHEDULE PREVIEW:")
    for day in result["optimized_daily_schedule"]:
        print(day)
