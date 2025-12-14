"""Validation helpers for parsed script data."""

from typing import Dict, Any, List
from src.errors import ParseError

# The loader may produce "heading" but some engines expect "header".
# We unify everything to "heading".
NORMALIZED_SCENE_KEYS = {"heading", "lines", "characters"}


def _normalize_scene(scene: Any, index: int) -> Dict[str, Any]:
    """
    Normalize a scene into a dict with guaranteed:
        heading: str
        lines: list[str]
        characters: list[str]
        dialogue_lines: int
        action_lines: int
    """

    # ----------------------------------------------------
    # CASE 1 — Scene is a raw string (fallback from loader)
    # ----------------------------------------------------
    if isinstance(scene, str):
        text = scene.strip()
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        return {
            "heading": f"Scene {index}",
            "lines": lines,
            "characters": [],
            "dialogue_lines": 0,
            "action_lines": 0,
        }

    # ----------------------------------------------------
    # CASE 2 — Scene should be a dict
    # ----------------------------------------------------
    if not isinstance(scene, dict):
        raise ParseError(f"Scene at index {index} must be dict or string, not {type(scene)}")

    normalized = {}

    # Accept both "header" and "heading"
    heading = scene.get("heading") or scene.get("header")
    if not heading:
        raise ParseError(f"Scene {index} missing required 'heading' or 'header' field")
    if not isinstance(heading, str):
        raise ParseError(f"Scene {index} heading is not a string")

    normalized["heading"] = heading

    # Normalize lines
    raw_lines = scene.get("lines", [])
    if isinstance(raw_lines, list):
        clean_lines: List[str] = []
        for ln in raw_lines:
            if isinstance(ln, dict):
                clean_lines.append(str(ln.get("text", "")).strip())
            else:
                clean_lines.append(str(ln).strip())
        normalized["lines"] = clean_lines
    else:
        raise ParseError(f"Scene {index} 'lines' must be a list")

    # Characters always a list
    chars = scene.get("characters", [])
    if not isinstance(chars, list):
        raise ParseError(f"Scene {index} 'characters' must be list")
    normalized["characters"] = chars

    # Compute dialogue/action counts if missing
    dcount = scene.get("dialogue_lines")
    acount = scene.get("action_lines")

    if dcount is None or acount is None:
        d = 0
        a = 0
        for ln in normalized["lines"]:
            if ln and ln.isupper() and len(ln.split()) <= 4:
                d += 1
            else:
                a += 1
        normalized["dialogue_lines"] = d
        normalized["action_lines"] = a
    else:
        normalized["dialogue_lines"] = int(dcount)
        normalized["action_lines"] = int(acount)

    return normalized


def validate_parsed_script(data: Dict[str, Any]) -> bool:
    """Validate and normalize loader output."""

    if not isinstance(data, dict):
        raise ParseError("Parsed script must be a dict.")

    scenes = data.get("scenes")
    if not isinstance(scenes, list):
        raise ParseError("Parsed script missing 'scenes' list.")

    normalized_scenes = []

    for i, scene in enumerate(scenes, start=1):
        normalized = _normalize_scene(scene, i)
        normalized_scenes.append(normalized)

    # Replace scenes with normalized version
    data["scenes"] = normalized_scenes

    # Optional characters list at root
    chars = data.get("characters")
    if chars is not None and not isinstance(chars, list):
        raise ParseError("'characters' must be list if present.")

    return True
