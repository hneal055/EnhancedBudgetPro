from typing import Dict, Any, List


class ScriptRiskAnalysisEngine:
    """
    Lightweight heuristic risk engine.

    Inputs:
      - scenes: list of scene dicts (from loader)
      - scene_density: list from SceneDensityEngine.analyze()["scene_density"]
      - character_costs: dict from CharacterCostImpactEngine.analyze()["character_costs"]

    Output:
      {
        "scene_risk_profiles": [
          {
            "scene": str,
            "characters": [str],
            "risk_score": float,
            "risk_classification": "Low"|"Medium"|"High",
            "scene_cost": float,
          }, ...
        ],
        "high_risk_scene_count": int
      }
    """

    def analyze(
        self,
        scenes: List[Dict[str, Any]],
        scene_density: List[Dict[str, Any]],
        character_costs: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        density_by_header = {
            d["header"]: d for d in scene_density
        }

        profiles = []
        high_risk_count = 0

        for idx, scene in enumerate(scenes, start=1):
            header = scene.get("heading") or scene.get("header") or f"Scene {idx}"
            chars = scene.get("characters", []) or []

            density_info = density_by_header.get(header, {})
            classification = density_info.get("classification", "Balanced")

            # base risk
            base = 0.5
            if classification == "Dialogue-Heavy":
                base += 0.1
            elif classification == "Action-Heavy":
                base += 0.2

            # cost weighting
            scene_cost = 0.0
            for c in chars:
                if c in character_costs:
                    scene_cost += character_costs[c].get("daily_rate", 0.0)

            if scene_cost > 0:
                if scene_cost > 100000:
                    base += 0.3
                elif scene_cost > 50000:
                    base += 0.2
                elif scene_cost > 20000:
                    base += 0.1

            risk_score = max(0.0, min(1.0, base))

            if risk_score >= 0.75:
                label = "High"
                high_risk_count += 1
            elif risk_score >= 0.5:
                label = "Medium"
            else:
                label = "Low"

            profiles.append(
                {
                    "scene": header,
                    "characters": chars,
                    "risk_score": risk_score,
                    "risk_classification": label,
                    "scene_cost": scene_cost,
                }
            )

        return {
            "scene_risk_profiles": profiles,
            "high_risk_scene_count": high_risk_count,
        }

