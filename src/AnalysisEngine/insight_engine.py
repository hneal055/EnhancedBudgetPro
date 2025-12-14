"""
Phase 12.0 - AI Producer Mode: Insight Engine
Read-only analysis and producer-level guidance

Core Principle: OBSERVE, ANALYZE, ADVISE
No modifications. No side effects. Zero risk.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum


class InsightSeverity(Enum):
    """Insight importance levels"""
    CRITICAL = "critical"    # Red flag - immediate attention
    WARNING = "warning"      # Yellow flag - needs review
    INFO = "info"           # Blue - informational
    SUCCESS = "success"     # Green - positive indicator


class InsightCategory(Enum):
    """Types of producer insights"""
    BUDGET = "budget"
    SCHEDULE = "schedule"
    TALENT = "talent"
    RISK = "risk"
    EFFICIENCY = "efficiency"
    OPPORTUNITY = "opportunity"


@dataclass
class ProducerInsight:
    """Single insight with context"""
    category: InsightCategory
    severity: InsightSeverity
    title: str
    description: str
    data_points: Dict[str, Any]
    recommendation: Optional[str] = None
    
    def to_dict(self) -> Dict:
        return {
            "category": self.category.value,
            "severity": self.severity.value,
            "title": self.title,
            "description": self.description,
            "data_points": self.data_points,
            "recommendation": self.recommendation
        }


class InsightEngine:
    """
    Read-only producer intelligence system
    Analyzes session data and provides actionable guidance
    """
    
    def __init__(self):
        self.insights: List[ProducerInsight] = []
    
    def analyze_session(self, session_state: Dict) -> List[ProducerInsight]:
        """
        Main analysis entry point
        Returns all insights for current session data
        """
        self.insights = []
        
        # Run all analysis modules
        self._analyze_budget(session_state)
        self._analyze_schedule(session_state)
        self._analyze_talent(session_state)
        self._analyze_risk(session_state)
        self._analyze_efficiency(session_state)
        self._analyze_opportunities(session_state)
        
        return self.insights
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 1️⃣ Budget Intelligence
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def _analyze_budget(self, session_state: Dict):
        """Analyze budget patterns and risks"""
        master_budget = session_state.get("master_budget")
        schedule = session_state.get("schedule")
        cost = session_state.get("cost", {})
        
        if not master_budget:
            return
        
        total_budget = master_budget.get("total", 0)
        shoot_days = schedule.get("shoot_days", 15) if schedule else 15
        
        # Daily burn rate analysis
        daily_burn = total_budget / shoot_days if shoot_days > 0 else 0
        
        if daily_burn > 15000:
            self.insights.append(ProducerInsight(
                category=InsightCategory.BUDGET,
                severity=InsightSeverity.WARNING,
                title="High Daily Burn Rate",
                description=f"Your daily budget burn is ${daily_burn:,.0f}, which exceeds typical indie thresholds.",
                data_points={
                    "daily_burn": daily_burn,
                    "total_budget": total_budget,
                    "shoot_days": shoot_days
                },
                recommendation="Consider: extending shoot days, reducing crew size, or negotiating equipment rates."
            ))
        
        # Cast budget concentration
        cast_total = master_budget.get("cast_total", 0)
        cast_percentage = (cast_total / total_budget * 100) if total_budget > 0 else 0
        
        if cast_percentage > 25:
            self.insights.append(ProducerInsight(
                category=InsightCategory.BUDGET,
                severity=InsightSeverity.INFO,
                title="Cast-Heavy Budget",
                description=f"Cast represents {cast_percentage:.1f}% of budget (industry avg: 15-20%).",
                data_points={
                    "cast_total": cast_total,
                    "cast_percentage": cast_percentage,
                    "total_budget": total_budget
                },
                recommendation="If talent costs are high, ensure they bring equivalent box office value or distribution leverage."
            ))
        
        # Equipment vs Crew balance
        equipment_total = master_budget.get("equipment_total", 0)
        crew_total = master_budget.get("crew_total", 0)
        
        if equipment_total > crew_total * 0.6:
            self.insights.append(ProducerInsight(
                category=InsightCategory.EFFICIENCY,
                severity=InsightSeverity.INFO,
                title="Equipment-Intensive Production",
                description=f"Equipment costs (${equipment_total:,.0f}) are unusually high relative to crew (${crew_total:,.0f}).",
                data_points={
                    "equipment_total": equipment_total,
                    "crew_total": crew_total,
                    "ratio": equipment_total / crew_total if crew_total > 0 else 0
                },
                recommendation="Verify all equipment is essential. Consider owned vs rented cost analysis."
            ))
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 2️⃣ Schedule Intelligence
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def _analyze_schedule(self, session_state: Dict):
        """Analyze schedule efficiency and risk"""
        schedule = session_state.get("schedule")
        data = session_state.get("data", {})
        scenes = data.get("scenes", [])
        
        if not schedule or not scenes:
            return
        
        shoot_days = schedule.get("shoot_days", 0)
        scene_count = len(scenes)
        
        # Scenes per day analysis
        scenes_per_day = scene_count / shoot_days if shoot_days > 0 else 0
        
        if scenes_per_day > 5:
            self.insights.append(ProducerInsight(
                category=InsightCategory.SCHEDULE,
                severity=InsightSeverity.WARNING,
                title="Aggressive Scene Load",
                description=f"Averaging {scenes_per_day:.1f} scenes/day. Industry standard: 3-4 scenes/day.",
                data_points={
                    "scenes_per_day": scenes_per_day,
                    "scene_count": scene_count,
                    "shoot_days": shoot_days
                },
                recommendation="Build buffer days for overages. Complex scenes may need dedicated days."
            ))
        elif scenes_per_day < 2:
            self.insights.append(ProducerInsight(
                category=InsightCategory.EFFICIENCY,
                severity=InsightSeverity.INFO,
                title="Conservative Schedule",
                description=f"Averaging {scenes_per_day:.1f} scenes/day - you have breathing room.",
                data_points={
                    "scenes_per_day": scenes_per_day,
                    "scene_count": scene_count,
                    "shoot_days": shoot_days
                },
                recommendation="Opportunity to add complexity or reduce shoot days to save budget."
            ))
        
        # Day assignments analysis
        day_assignments = schedule.get("day_assignments", {})
        if day_assignments:
            daily_loads = [len(scenes) for scenes in day_assignments.values()]
            max_load = max(daily_loads) if daily_loads else 0
            min_load = min(daily_loads) if daily_loads else 0
            
            if max_load > min_load * 2:
                self.insights.append(ProducerInsight(
                    category=InsightCategory.SCHEDULE,
                    severity=InsightSeverity.WARNING,
                    title="Uneven Day Distribution",
                    description=f"Peak day has {max_load} scenes vs {min_load} on lightest day.",
                    data_points={
                        "max_load": max_load,
                        "min_load": min_load,
                        "imbalance_ratio": max_load / min_load if min_load > 0 else 0
                    },
                    recommendation="Rebalance to prevent crew fatigue and maintain consistent pace."
                ))
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 3️⃣ Talent Intelligence
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def _analyze_talent(self, session_state: Dict):
        """Analyze talent availability and utilization"""
        intel = session_state.get("intel", {})
        talent_overrides = session_state.get("talent_overrides", {})
        cost = session_state.get("cost", {})
        
        if not intel:
            return
        
        # Handle both dict and list formats for intel
        if isinstance(intel, list):
            # Convert list format to dict format
            intel_dict = {}
            for item in intel:
                if isinstance(item, dict):
                    char_name = item.get("character", item.get("name", "Unknown"))
                    intel_dict[char_name] = item
        else:
            intel_dict = intel
        
        if not intel_dict:
            return
        
        # Identify high-cost, low-utilization talent
        for character, char_intel in intel_dict.items():
            if not isinstance(char_intel, dict):
                continue
                
            scenes = char_intel.get("scenes", 0)
            screen_time = char_intel.get("estimated_screen_time_min", 0)
            
            # Handle cost data (could be dict or list)
            if isinstance(cost, dict):
                char_cost = cost.get(character, {})
            else:
                char_cost = {}
            
            daily_rate = char_cost.get("daily_rate", 0) if isinstance(char_cost, dict) else 0
            
            # High rate but low scenes = inefficient spend
            if daily_rate > 1000 and scenes < 3:
                self.insights.append(ProducerInsight(
                    category=InsightCategory.TALENT,
                    severity=InsightSeverity.WARNING,
                    title=f"Underutilized High-Cost Talent: {character}",
                    description=f"Paying ${daily_rate}/day but only {scenes} scenes ({screen_time} min screen time).",
                    data_points={
                        "character": character,
                        "daily_rate": daily_rate,
                        "scenes": scenes,
                        "screen_time": screen_time,
                        "cost_per_minute": daily_rate / screen_time if screen_time > 0 else 0
                    },
                    recommendation="Consider: consolidating scenes, rewriting for more screen time, or recasting."
                ))
        
        # Conflict analysis
        if talent_overrides and isinstance(talent_overrides, dict):
            try:
                conflict_count = sum(
                    len(conflicts) if isinstance(conflicts, (list, dict)) else 0 
                    for conflicts in talent_overrides.values()
                )
            except (TypeError, AttributeError):
                conflict_count = 0
            
            if conflict_count > 0:
                self.insights.append(ProducerInsight(
                    category=InsightCategory.TALENT,
                    severity=InsightSeverity.WARNING,
                    title="Talent Conflicts Detected",
                    description=f"{conflict_count} scheduling conflicts require resolution.",
                    data_points={
                        "conflict_count": conflict_count,
                        "affected_characters": [c for c, conf in talent_overrides.items() if conf]
                    },
                    recommendation="Run auto-rescheduler or manually adjust stripboard before locking schedule."
                ))
    
    def _analyze_risk(self, session_state: Dict):
        """Analyze production risks"""
        risks = session_state.get("risks", [])
        monte_carlo = session_state.get("monte_carlo", {})
        master_budget = session_state.get("master_budget", {})
        
        if not risks:
            return
        
        # Risk distribution
        high_risks = sum(1 for r in risks if r.get("risk_level") == "HIGH")
        total_risks = len(risks)
        
        if high_risks > total_risks * 0.3:
            self.insights.append(ProducerInsight(
                category=InsightCategory.RISK,
                severity=InsightSeverity.CRITICAL,
                title="High Risk Concentration",
                description=f"{high_risks}/{total_risks} scenes flagged as HIGH risk ({high_risks/total_risks*100:.0f}%).",
                data_points={
                    "high_risk_count": high_risks,
                    "total_risks": total_risks,
                    "high_risk_percentage": high_risks / total_risks * 100 if total_risks > 0 else 0
                },
                recommendation="CRITICAL: Review mitigation plans. Consider increasing contingency or eliminating high-risk scenes."
            ))
        
        # Monte Carlo analysis
        if monte_carlo:
            p10 = monte_carlo.get("p10", 0)
            p50 = monte_carlo.get("p50", 0)
            p90 = monte_carlo.get("p90", 0)
            
            budget_variance = ((p90 - p10) / p50 * 100) if p50 > 0 else 0
            
            if budget_variance > 30:
                self.insights.append(ProducerInsight(
                    category=InsightCategory.RISK,
                    severity=InsightSeverity.WARNING,
                    title="High Budget Uncertainty",
                    description=f"Monte Carlo shows {budget_variance:.0f}% variance between best/worst case.",
                    data_points={
                        "p10": p10,
                        "p50": p50,
                        "p90": p90,
                        "variance_pct": budget_variance
                    },
                    recommendation="Increase contingency to 15% or lock down variable costs through fixed-price contracts."
                ))
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 5️⃣ Efficiency Intelligence
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def _analyze_efficiency(self, session_state: Dict):
        """Identify efficiency improvements"""
        data = session_state.get("data", {})
        scenes = data.get("scenes", [])
        density = session_state.get("density", {})
        
        if not scenes:
            return
        
        # Dialogue-heavy scene clustering
        if density:
            dialogue_heavy_scenes = []
            for scene_id, scene_density in density.items():
                ratio = scene_density.get("dialogue_action_ratio", 0)
                if ratio > 2.0:  # More than 2:1 dialogue to action
                    dialogue_heavy_scenes.append(scene_id)
            
            if len(dialogue_heavy_scenes) > len(scenes) * 0.4:
                self.insights.append(ProducerInsight(
                    category=InsightCategory.EFFICIENCY,
                    severity=InsightSeverity.INFO,
                    title="Dialogue-Intensive Script",
                    description=f"{len(dialogue_heavy_scenes)}/{len(scenes)} scenes are dialogue-heavy.",
                    data_points={
                        "dialogue_heavy_count": len(dialogue_heavy_scenes),
                        "total_scenes": len(scenes),
                        "percentage": len(dialogue_heavy_scenes) / len(scenes) * 100 if scenes else 0
                    },
                    recommendation="Opportunity: Single-camera dialogue can be shot efficiently. Schedule these together to minimize lighting changes."
                ))
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # 6️⃣ Opportunity Intelligence
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def _analyze_opportunities(self, session_state: Dict):
        """Identify cost-saving or quality-improvement opportunities"""
        master_budget = session_state.get("master_budget", {})
        schedule = session_state.get("schedule")
        
        if not master_budget:
            return
        
        total_budget = master_budget.get("total", 0)
        shoot_days = schedule.get("shoot_days", 15) if schedule else 15
        
        # Budget cushion check
        contingency = master_budget.get("insurance_total", 0)
        contingency_pct = (contingency / total_budget * 100) if total_budget > 0 else 0
        
        if contingency_pct < 10:
            self.insights.append(ProducerInsight(
                category=InsightCategory.OPPORTUNITY,
                severity=InsightSeverity.WARNING,
                title="Low Contingency",
                description=f"Contingency at {contingency_pct:.1f}% (recommend 10-15%).",
                data_points={
                    "contingency": contingency,
                    "total_budget": total_budget,
                    "contingency_pct": contingency_pct
                },
                recommendation="Increase contingency to protect against overages."
            ))
        elif contingency_pct > 15:
            self.insights.append(ProducerInsight(
                category=InsightCategory.OPPORTUNITY,
                severity=InsightSeverity.SUCCESS,
                title="Healthy Contingency",
                description=f"Contingency at {contingency_pct:.1f}% provides good buffer.",
                data_points={
                    "contingency": contingency,
                    "total_budget": total_budget,
                    "contingency_pct": contingency_pct
                },
                recommendation="Well positioned for unexpected costs."
            ))
    
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    # Utility Methods
    # ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    
    def get_insights_by_category(self, category: InsightCategory) -> List[ProducerInsight]:
        """Filter insights by category"""
        return [i for i in self.insights if i.category == category]
    
    def get_insights_by_severity(self, severity: InsightSeverity) -> List[ProducerInsight]:
        """Filter insights by severity"""
        return [i for i in self.insights if i.severity == severity]
    
    def get_critical_insights(self) -> List[ProducerInsight]:
        """Get only critical insights requiring immediate attention"""
        return self.get_insights_by_severity(InsightSeverity.CRITICAL)
    
    def to_summary(self) -> Dict:
        """Generate summary statistics"""
        return {
            "total_insights": len(self.insights),
            "by_severity": {
                "critical": len(self.get_insights_by_severity(InsightSeverity.CRITICAL)),
                "warning": len(self.get_insights_by_severity(InsightSeverity.WARNING)),
                "info": len(self.get_insights_by_severity(InsightSeverity.INFO)),
                "success": len(self.get_insights_by_severity(InsightSeverity.SUCCESS))
            },
            "by_category": {
                cat.value: len(self.get_insights_by_category(cat))
                for cat in InsightCategory
            }
        }
