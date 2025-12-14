import re
from typing import Dict, List


class PlainTextLoader:
    """
    Improved plain text screenplay parser with:
    ✅ Scene detection
    ✅ Character detection
    ✅ Dialogue line detection
    ✅ Action line detection (NEW - Phase 2.4)
    """

    SCENE_PATTERN = re.compile(r"^(INT\.|EXT\.|INT/EXT\.)", re.IGNORECASE)

    def load(self, script_text: str) -> Dict:

        lines = [line.rstrip() for line in script_text.splitlines()]

        scenes: List[Dict] = []
        current_scene = None
        current_character = None
        expecting_dialogue = False

        for line in lines:
            stripped = line.strip()

            # -------------------------
            # SCENE HEADER
            # -------------------------
            if self.SCENE_PATTERN.match(stripped):
                if current_scene:
                    scenes.append(current_scene)

                current_scene = {
                    "heading": stripped,
                    "lines": [],
                    "characters": [],
                    "dialogue_lines": 0,
                    "action_lines": 0,
                }

                current_character = None
                expecting_dialogue = False
                continue

            # Ignore lines outside scenes
            if not current_scene or not stripped:
                expecting_dialogue = False
                continue

            # record raw line in scene lines
            if current_scene is not None and stripped:
                current_scene["lines"].append(stripped)

            # -------------------------
            # CHARACTER NAME (ALL CAPS)
            # -------------------------
            if stripped.isupper() and len(stripped.split()) <= 3:
                current_character = stripped
                if current_character not in current_scene["characters"]:
                    current_scene["characters"].append(current_character)
                expecting_dialogue = True
                continue

            # -------------------------
            # DIALOGUE LINE
            # -------------------------
            if expecting_dialogue:
                current_scene["dialogue_lines"] += 1
                expecting_dialogue = False
                continue

            # -------------------------
            # ACTION LINE (NEW PHASE 2.4)
            # -------------------------
            current_scene["action_lines"] += 1
            expecting_dialogue = False

        # Add final scene
        if current_scene:
            scenes.append(current_scene)

        return {
            "scene_count": len(scenes),
            "scenes": scenes,
        }



# convenience wrapper for file-router
def load_text(path_or_text):
    loader = PlainTextLoader()
    try:
        p = Path(path_or_text)
        if p.exists() and p.is_file():
            text = p.read_text(encoding='utf-8')
        else:
            text = path_or_text
    except Exception:
        text = path_or_text
    return loader.load(text)
