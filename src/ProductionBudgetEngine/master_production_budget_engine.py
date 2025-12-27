# master_production_budget_engine.py — Phase 3.0 Master Aggregator
# ---------------------------------------------------------------
# Aggregates ALL production budget engines into a single unified budget
# Phase 13.1 Week 4: Enhanced with emotion-based contingency

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
    ✅ Phase 13.1 Week 4: Emotion-based contingency adjustment
    """

    def calculate_full_budget(self, shoot_days: int, emotion_data: dict = None) -> dict:
        """
        Calculate full production budget with optional emotion-based adjustments.
        
        Phase 13.1 Week 4: High-intensity scripts get +5% contingency
        
        Args:
            shoot_days: Number of shooting days
            emotion_data: Optional emotional intelligence data
        
        Returns:
            Comprehensive budget breakdown with emotion factors
        """
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

        # Phase 13.1 Week 4: Emotion-based contingency adjustment
        emotion_contingency = 0
        emotion_factor_note = "Standard contingency"
        
        if emotion_data:
            summary = emotion_data.get("summary", {})
            avg_intensity = summary.get("average_intensity", 0)
            avg_tension = summary.get("average_tension", 0)
            
            # High-intensity scripts need extra contingency
            if avg_intensity > 60:
                emotion_contingency = core_total * 0.05  # +5%
                emotion_factor_note = f"High emotional intensity ({avg_intensity:.1f}/100) → +5% contingency"
            elif avg_tension > 60:
                emotion_contingency = core_total * 0.03  # +3%
                emotion_factor_note = f"High tension ({avg_tension:.1f}/100) → +3% contingency"

        final_total = insurance["total_with_insurance_and_contingency"] + emotion_contingency

        return {
            "crew": crew,
            "equipment": equipment,
            "locations": locations,
            "post": post,
            "insurance": insurance,
            "core_production_total": core_total,
            "emotion_contingency": emotion_contingency,
            "emotion_factor_note": emotion_factor_note,
            "final_production_budget": final_total
        }
