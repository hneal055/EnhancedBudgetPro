# master_production_budget_engine.py — Phase 3.0 Master Aggregator
# ---------------------------------------------------------------
# Aggregates ALL production budget engines into a single unified budget

from src.ProductionBudgetEngine.crew_budget_engine import CrewBudgetEngine
from src.ProductionBudgetEngine.equipment_budget_engine import EquipmentBudgetEngine
from src.ProductionBudgetEngine.location_budget_engine import LocationBudgetEngine
from src.ProductionBudgetEngine.post_budget_engine import PostProductionBudgetEngine
from src.ProductionBudgetEngine.insurance_contingency_engine import InsuranceContingencyEngine


class MasterProductionBudgetEngine:
    """
    Aggregates:
    ✅ Crew
    ✅ Equipment
    ✅ Locations
    ✅ Post-Production
    ✅ Insurance & Contingency
    """

    def calculate_full_budget(self, shoot_days: int) -> dict:
        crew_engine = CrewBudgetEngine()
        equipment_engine = EquipmentBudgetEngine()
        location_engine = LocationBudgetEngine()
        post_engine = PostProductionBudgetEngine()
        insurance_engine = InsuranceContingencyEngine()

        crew = crew_engine.calculate(shoot_days)
        equipment = equipment_engine.calculate(shoot_days)
        locations = location_engine.calculate(shoot_days)
        post = post_engine.calculate()

        core_total = (
            crew["total_crew_cost"]
            + equipment["total_equipment_cost"]
            + locations["total_location_cost"]
            + post["total_post_cost"]
        )

        insurance = insurance_engine.calculate(core_total)

        final_total = insurance["total_with_insurance_and_contingency"]

        return {
            "crew": crew,
            "equipment": equipment,
            "locations": locations,
            "post": post,
            "insurance": insurance,
            "core_production_total": core_total,
            "final_production_budget": final_total
        }
