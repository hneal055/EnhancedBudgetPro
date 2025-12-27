# post_budget_engine.py — Phase 3.0 Post-Production Budget Engine
# --------------------------------------------------------------
# Models all post-production cost categories

from typing import Dict


class PostProductionBudgetEngine:
    """
    Computes:
    ✅ Editorial
    ✅ Sound design
    ✅ Music
    ✅ VFX
    ✅ Color grading
    ✅ Deliverables
    """

    DEFAULT_POST_COSTS = {
        "Picture Edit": 4500,
        "Sound Design & Mix": 6000,
        "Music Score": 5000,
        "VFX": 8000,
        "Color Grading": 3500,
        "Masters & Deliverables": 2500
    }

    def calculate(
        self,
        custom_post_costs: Dict[str, int] = None
    ) -> Dict:

        costs = custom_post_costs if custom_post_costs else self.DEFAULT_POST_COSTS

        post_breakdown = {}
        total = 0

        for item, flat_cost in costs.items():
            post_breakdown[item] = {
                "flat_cost": flat_cost
            }
            total += flat_cost

        return {
            "post_breakdown": post_breakdown,
            "total_post_cost": total
        }
