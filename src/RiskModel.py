import random
from dataclasses import dataclass
from src.BudgetEngine import ProductionBudget


@dataclass
class RiskModel:
    budget: ProductionBudget
    contingency_rate: float = 0.12
    delay_probability: float = 0.25
    max_delay_days: int = 4

    def contingency_buffer(self) -> float:
        return self.budget.total_budget() * self.contingency_rate

    def simulate_delay_cost(self) -> float:
        if random.random() < self.delay_probability:
            extra_days = random.randint(1, self.max_delay_days)
            return self.budget.daily_total() * extra_days
        return 0

    def risk_adjusted_total(self):
        delay_cost = self.simulate_delay_cost()
        base = self.budget.total_budget()
        contingency = self.contingency_buffer()

        return {
            "base_budget": base,
            "risk_delay_cost": delay_cost,
            "contingency_buffer": contingency,
            "risk_adjusted_total": base + contingency + delay_cost
        }


# Simple compatibility wrapper used by ScriptIngest
def assess_risks(scenes):
    """Return a list of risk rows for each scene.

    Each row: {scene: str, risk_type: str, risk_level: "HIGH|MEDIUM|LOW", mitigation: str}
    """
    rows = []
    for s in scenes:
        heading = s.get('heading') or s.get('header') or 'UNKNOWN'
        action = s.get('action_lines', 0)
        dialogue = s.get('dialogue_lines', 0)
        # heuristic
        if action >= 6:
            level = 'HIGH'
        elif action >= 3:
            level = 'MEDIUM'
        else:
            level = 'LOW'
        rows.append({
            'scene': heading,
            'risk_type': 'Action-Intensity',
            'risk_level': level,
            'mitigation': 'Stunt coordination / schedule buffer' if level != 'LOW' else 'Standard precautions'
        })
    return rows
