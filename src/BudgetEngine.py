from dataclasses import dataclass, field
from typing import Dict


@dataclass
class CostCategory:
    name: str
    daily_rate: float
    quantity: int = 1

    def daily_cost(self) -> float:
        return self.daily_rate * self.quantity


@dataclass
class ProductionBudget:
    shoot_days: int
    crew: Dict[str, CostCategory] = field(default_factory=dict)
    equipment: Dict[str, CostCategory] = field(default_factory=dict)
    locations: Dict[str, CostCategory] = field(default_factory=dict)

    def add_crew(self, name: str, rate: float, qty: int = 1):
        self.crew[name] = CostCategory(name, rate, qty)

    def add_equipment(self, name: str, rate: float, qty: int = 1):
        self.equipment[name] = CostCategory(name, rate, qty)

    def add_location_cost(self, name: str, rate: float, qty: int = 1):
        self.locations[name] = CostCategory(name, rate, qty)

    def daily_total(self) -> float:
        return (
            sum(c.daily_cost() for c in self.crew.values()) +
            sum(e.daily_cost() for e in self.equipment.values()) +
            sum(l.daily_cost() for l in self.locations.values())
        )

    def total_budget(self) -> float:
        return self.daily_total() * self.shoot_days


# High-level helper used by ScriptIngest and CLI
from src.ProductionBudgetEngine.master_production_budget_engine import MasterProductionBudgetEngine
import math


def estimate_budget(scenes: list) -> tuple:
    """Estimate a production budget from scenes.

    Simple heuristic:
      - scenes_per_day = 3 (default)
      - shoot_days = ceil(len(scenes) / scenes_per_day)

    Returns: (budget_summary: dict, budget_rows: list)
    """
    scenes_count = len(scenes or [])
    scenes_per_day = 3
    shoot_days = max(1, math.ceil(scenes_count / scenes_per_day))

    master = MasterProductionBudgetEngine()
    result = master.calculate_full_budget(shoot_days)

    total_budget = result.get('final_production_budget', 0.0)
    average_cost_per_scene = total_budget / max(1, scenes_count)

    budget_summary = {
        'shoot_days': shoot_days,
        'scenes': scenes_count,
        'total_budget': total_budget,
        'average_cost_per_scene': average_cost_per_scene,
        'currency': 'USD'
    }

    # build budget_rows (flatten key parts for basic CSV)
    rows = []
    for k in ('crew', 'equipment', 'locations', 'post', 'insurance'):
        part = result.get(k)
        if isinstance(part, dict):
            for name, val in part.items():
                if isinstance(val, dict):
                    # try to capture totals
                    total = val.get('total_%s_cost' % k[:-1], None) if k.endswith('s') else None
                    rows.append({'category': k, 'item': name, 'details': val, 'total': total})
    return budget_summary, rows


# High-level helper used by ScriptIngest and CLI
from src.ProductionBudgetEngine.master_production_budget_engine import MasterProductionBudgetEngine
import math


def estimate_budget(scenes: list) -> tuple:
    """Estimate a production budget from scenes.

    Simple heuristic:
      - scenes_per_day = 3 (default)
      - shoot_days = ceil(len(scenes) / scenes_per_day)

    Returns: (budget_summary: dict, budget_rows: list)
    """
    scenes_count = len(scenes or [])
    scenes_per_day = 3
    shoot_days = max(1, math.ceil(scenes_count / scenes_per_day))

    master = MasterProductionBudgetEngine()
    result = master.calculate_full_budget(shoot_days)

    total_budget = result.get('final_production_budget', 0.0)
    average_cost_per_scene = total_budget / max(1, scenes_count)

    budget_summary = {
        'shoot_days': shoot_days,
        'scenes': scenes_count,
        'total_budget': total_budget,
        'average_cost_per_scene': average_cost_per_scene,
        'currency': 'USD'
    }

    # build budget_rows (flatten breakdowns into canonical fields)
    rows = []
    # crew
    crew = result.get('crew', {})
    crew_breakdown = crew.get('crew_breakdown', {})
    for name, v in crew_breakdown.items():
        rows.append({
            'category': 'crew',
            'item': name,
            'rate': v.get('daily_rate'),
            'quantity': v.get('shoot_days'),
            'total_cost': v.get('total_cost')
        })

    # equipment
    equipment = result.get('equipment', {})
    equipment_breakdown = equipment.get('equipment_breakdown', {})
    for name, v in equipment_breakdown.items():
        rows.append({
            'category': 'equipment',
            'item': name,
            'rate': v.get('daily_rate'),
            'quantity': v.get('shoot_days'),
            'total_cost': v.get('total_cost')
        })

    # locations
    locations = result.get('locations', {})
    loc_breakdown = locations.get('location_breakdown', {})
    for name, v in loc_breakdown.items():
        rows.append({
            'category': 'locations',
            'item': name,
            'rate': v.get('daily_rate'),
            'quantity': v.get('days', shoot_days),
            'total_cost': v.get('total_cost')
        })

    # post
    post = result.get('post', {})
    if post:
        # post likely has total_post_cost
        rows.append({
            'category': 'post',
            'item': 'post_production',
            'rate': post.get('rate', None),
            'quantity': 1,
            'total_cost': post.get('total_post_cost', None)
        })

    # insurance
    insurance = result.get('insurance', {})
    if insurance:
        rows.append({
            'category': 'insurance',
            'item': 'insurance_and_contingency',
            'rate': None,
            'quantity': 1,
            'total_cost': insurance.get('total_with_insurance_and_contingency')
        })

    return budget_summary, rows
