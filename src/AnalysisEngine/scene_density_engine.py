import re
from typing import Any, Dict, List


class SceneDensityEngine:
    """
    Computes dialogue vs action density for each scene.

    The engine is intentionally lenient and accepts:

    1) scenes as full dict objects:
        {
          "header": str,
          "lines": [str OR {"text":str, ...}],
          "characters": [str]
        }

    2) scenes as plain strings:
        "INT. LAB - NIGHT\nJohn enters..."

    Output is always stable.
    """

    def analyze(self, data: Dict[str, Any]) -> Dict[str, Any]:
        scenes = data.get("scenes", []) or []
        results = []

        total_dialogue = 0
        total_action = 0

        for idx, scene in enumerate(scenes, start=1):

            # ---------------------------------------------------------
            # NORMALIZATION LAYER — prevents `.get` crashes
            # ---------------------------------------------------------
            if isinstance(scene, dict):
                header = scene.get("header") or f"Scene {idx}"
                characters = scene.get("characters", []) or []

                raw_lines = scene.get("lines", []) or []
                normalized_lines: List[str] = []

                for ln in raw_lines:
                    if isinstance(ln, dict):
                        normalized_lines.append(str(ln.get("text", "")).strip())
                    else:
                        normalized_lines.append(str(ln).strip())

            else:
                # Scene is a simple string → split lines
                header = f"Scene {idx}"
                characters = []
                normalized_lines = [
                    line.strip() for line in str(scene).splitlines()
                ]

            # ---------------------------------------------------------
            # CLASSIFICATION
            # ---------------------------------------------------------
            dialogue = 0
            action = 0

            for line in normalized_lines:
                if not line:
                    continue

                # Heuristic: uppercase short-ish lines → likely dialogue blocks
                if re.match(r"^[A-Z0-9 .'\-()]{3,}$", line) and len(line.split()) <= 6:
                    dialogue += 1
                else:
                    action += 1

            total_dialogue += dialogue
            total_action += action

            total = dialogue + action
            ratio = (dialogue / total) if total > 0 else 0.0

            if ratio > 0.7:
                classification = "Dialogue-Heavy"
            elif ratio < 0.3:
                classification = "Action-Heavy"
            else:
                classification = "Balanced"

            results.append(
                {
                    "header": header,
                    "characters": characters,
                    "dialogue_lines": dialogue,
                    "action_lines": action,
                    "dialogue_density_ratio": ratio,
                    "classification": classification,
                }
            )

        # ---------------------------------------------------------
        # FINAL RETURN BLOCK (stable structure)
        # ---------------------------------------------------------
        return {
            "scene_density": results,
            "totals": {
                "total_dialogue_lines": total_dialogue,
                "total_action_lines": total_action,
            },
        }

