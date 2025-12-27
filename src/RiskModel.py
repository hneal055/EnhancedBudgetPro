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
def assess_risks(scenes, emotion_data=None):
    """
    Return a list of risk rows for each scene.
    
    Phase 13.1 Week 4: Enhanced with emotional intelligence factors
    High-tension scenes = higher risk scores

    Each row: {scene: str, risk_type: str, risk_level: "HIGH|MEDIUM|LOW", mitigation: str}
    
    Args:
        scenes: List of scene dictionaries
        emotion_data: Optional emotion analysis data with scene-level metrics
    """
    rows = []
    
    # Build emotion lookup if available
    emotion_by_heading = {}
    if emotion_data and emotion_data.get("scenes"):
        for scene_emotion in emotion_data["scenes"]:
            heading = scene_emotion.get("heading", "")
            emotion_by_heading[heading] = scene_emotion
    
    for s in scenes:
        heading = s.get('heading') or s.get('header') or 'UNKNOWN'
        action = s.get('action_lines', 0)
        dialogue = s.get('dialogue_lines', 0)
        
        # Base action-intensity risk
        if action >= 6:
            base_level = 'HIGH'
        elif action >= 3:
            base_level = 'MEDIUM'
        else:
            base_level = 'LOW'
        
        # Phase 13.1 Week 4: Adjust risk based on emotional tension
        adjusted_level = base_level
        emotion_factor = ""
        
        if heading in emotion_by_heading:
            scene_emotion = emotion_by_heading[heading]
            tension = scene_emotion.get("tension", 0)
            intensity = scene_emotion.get("intensity", 0)
            
            # High tension increases risk
            if tension > 70:
                # Upgrade risk level
                if base_level == 'LOW':
                    adjusted_level = 'MEDIUM'
                elif base_level == 'MEDIUM':
                    adjusted_level = 'HIGH'
                emotion_factor = " (High Tension +10% risk)"
            elif tension > 50 and base_level == 'LOW':
                adjusted_level = 'MEDIUM'
                emotion_factor = " (Moderate Tension)"
            
            # High intensity also increases complexity risk
            if intensity > 80 and adjusted_level != 'HIGH':
                adjusted_level = 'HIGH'
                emotion_factor = " (High Emotional Intensity)"
        
        # Determine mitigation
        if adjusted_level == 'HIGH':
            mitigation = f'Stunt coordination / schedule buffer / actor support{emotion_factor}'
        elif adjusted_level == 'MEDIUM':
            mitigation = f'Extra rehearsal time / emotional prep{emotion_factor}'
        else:
            mitigation = 'Standard precautions'
        
        rows.append({
            'scene': heading,
            'risk_type': 'Action-Intensity' if not emotion_factor else 'Action-Emotion Risk',
            'risk_level': adjusted_level,
            'mitigation': mitigation
        })
    
    return rows
