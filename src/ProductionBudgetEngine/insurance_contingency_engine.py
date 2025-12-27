# insurance_contingency_engine.py — Phase 3.0 Insurance & Contingency Engine
# ------------------------------------------------------------------------
# Models production insurance, bonds, liability, and contingency buffers

from typing import Dict


class InsuranceContingencyEngine:
    """
    Computes:
    ✅ Production insurance
    ✅ General liability
    ✅ Completion bond
    ✅ Contingency buffer (%)
    """

    DEFAULT_INSURANCE_COSTS = {
        "Production Insurance": 8500,
        "General Liability": 4200,
        "Completion Bond": 12000
    }

    DEFAULT_CONTINGENCY_RATE = 0.10   # 10% contingency buffer

    def calculate(
        self,
        current_budget_total: float,
        custom_insurance_costs: Dict[str, int] = None,
        contingency_rate: float = None
    ) -> Dict:

        insurance = custom_insurance_costs if custom_insurance_costs else self.DEFAULT_INSURANCE_COSTS
        contingency = contingency_rate if contingency_rate is not None else self.DEFAULT_CONTINGENCY_RATE

        insurance_breakdown = {}
        insurance_total = 0

        for item, flat_cost in insurance.items():
            insurance_breakdown[item] = {"flat_cost": flat_cost}
            insurance_total += flat_cost

        contingency_buffer = round(current_budget_total * contingency, 2)
        grand_total = current_budget_total + insurance_total + contingency_buffer

        return {
            "insurance_breakdown": insurance_breakdown,
            "insurance_total": insurance_total,
            "contingency_rate": contingency,
            "contingency_buffer": contingency_buffer,
            "total_with_insurance_and_contingency": grand_total
        }
