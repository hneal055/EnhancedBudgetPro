# equipment_budget_engine.py — Phase 3.0 Equipment Budget Engine
# -------------------------------------------------------------
# Models camera, sound, lighting, grip, and special equipment packages

from typing import Dict


class EquipmentBudgetEngine:
    """
    Computes:
    ✅ Equipment package daily costs
    ✅ Department-level totals
    ✅ Global equipment budget total
    """

    DEFAULT_EQUIPMENT = {
        "Camera Package (A-Cam)": 2500,
        "Sound Kit (Full)": 900,
        "Lighting Truck": 1800,
        "Grip Truck": 1500,
        "Drone Unit": 1200,
        "Steadicam Rig": 1000,
        "Specialty Rigs / FX": 2000
    }

    def calculate(
        self,
        shoot_days: int,
        custom_equipment: Dict[str, int] = None
    ) -> Dict:

        equipment = custom_equipment if custom_equipment else self.DEFAULT_EQUIPMENT
        equipment_breakdown = {}
        total = 0

        for item, daily_rate in equipment.items():
            item_total = daily_rate * shoot_days
            equipment_breakdown[item] = {
                "daily_rate": daily_rate,
                "shoot_days": shoot_days,
                "total_cost": item_total
            }
            total += item_total

        return {
            "equipment_breakdown": equipment_breakdown,
            "total_equipment_cost": total
        }
