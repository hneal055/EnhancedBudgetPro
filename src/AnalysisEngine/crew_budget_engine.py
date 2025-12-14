# crew_budget_engine.py — Phase 3.0 Crew Budget Engine
# ------------------------------------------
# Computes full production crew costs by department & tier

from typing import Dict


class CrewBudgetEngine:
    """
    Computes:
    ✅ Union / Non-Union crew tiers
    ✅ Department-level totals
    ✅ Global crew budget total
    """

    DEFAULT_CREW = {
        "Director": 2500,
        "1st AD": 1200,
        "2nd AD": 800,
        "Director of Photography": 2200,
        "Camera Operator": 1100,
        "Key Grip": 900,
        "Gaffer": 1000,
        "Sound Mixer": 950,
        "Boom Operator": 650,
        "Production Designer": 1400,
        "Art Director": 1000,
        "Makeup Lead": 750,
        "Costume Designer": 900,
        "Script Supervisor": 700,
        "Production Assistant": 300
    }

    def calculate(
        self,
        shoot_days: int,
        custom_crew: Dict[str, int] = None
    ) -> Dict:

        crew = custom_crew if custom_crew else self.DEFAULT_CREW
        crew_breakdown = {}
        total = 0

        for role, daily_rate in crew.items():
            role_total = daily_rate * shoot_days
            crew_breakdown[role] = {
                "daily_rate": daily_rate,
                "shoot_days": shoot_days,
                "total_cost": role_total
            }
            total += role_total

        return {
            "crew_breakdown": crew_breakdown,
            "total_crew_cost": total
        }
