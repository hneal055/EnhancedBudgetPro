# location_budget_engine.py — Phase 3.0 Location Budget Engine
# -----------------------------------------------------------
# Models all location-based production costs

from typing import Dict


class LocationBudgetEngine:
    """
    Computes:
    ✅ Location rental fees
    ✅ Permits
    ✅ Location management
    ✅ Security
    ✅ Holding & staging
    ✅ Global location budget
    """

    DEFAULT_LOCATIONS = {
        "Studio Stage": 5000,
        "Urban Exterior": 3500,
        "Residential Interior": 3000,
        "Warehouse / Industrial": 4000,
        "Rural Exterior": 2500,
    }

    DEFAULT_SUPPORT_COSTS = {
        "Permits": 800,
        "Location Manager": 1200,
        "Security": 1000,
        "Holding & Staging": 900,
    }

    def calculate(
        self,
        shoot_days: int,
        custom_locations: Dict[str, int] = None,
        custom_support_costs: Dict[str, int] = None,
    ) -> Dict:

        locations = custom_locations if custom_locations else self.DEFAULT_LOCATIONS
        support = (
            custom_support_costs if custom_support_costs else self.DEFAULT_SUPPORT_COSTS
        )

        location_breakdown = {}
        support_breakdown = {}
        total = 0

        # Core location fees
        for loc, daily_rate in locations.items():
            loc_total = daily_rate * shoot_days
            location_breakdown[loc] = {
                "daily_rate": daily_rate,
                "shoot_days": shoot_days,
                "total_cost": loc_total,
            }
            total += loc_total

        # Support costs
        for item, daily_rate in support.items():
            item_total = daily_rate * shoot_days
            support_breakdown[item] = {
                "daily_rate": daily_rate,
                "shoot_days": shoot_days,
                "total_cost": item_total,
            }
            total += item_total

        return {
            "location_breakdown": location_breakdown,
            "support_breakdown": support_breakdown,
            "total_location_cost": total,
        }
