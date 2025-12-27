import re
from .shared_utils import clean_text, extract_characters


class FountainLoader:
    """
    Class-based Fountain screenplay loader.
    """

    def load(self, text: str):
        lines = [clean_text(l) for l in text.split("\n") if l.strip()]

        scenes = []
        current_scene = {
            "header": None,
            "characters": set(),
            "dialogue_lines": 0,
            "action_lines": 0
        }

        for line in lines:
            if line.startswith(("INT.", "EXT.", "INT/EXT.")):
                if current_scene.get("heading", current_scene.get("header", "<unknown>")):
                    scenes.append(self._finalize_scene(current_scene))

                current_scene = {
                    "header": line,
                    "characters": set(),
                    "dialogue_lines": 0,
                    "action_lines": 0
                }
                continue

            if re.match(r"^[A-Z][A-Z0-9 ]{1,30}$", line):
                current_scene["characters"].add(line)
                continue

            if line.endswith((".", "!", "?")):
                current_scene["dialogue_lines"] += 1
            else:
                current_scene["action_lines"] += 1

        if current_scene.get("heading", current_scene.get("header", "<unknown>")):
            scenes.append(self._finalize_scene(current_scene))

        total_lines = sum(s["dialogue_lines"] + s["action_lines"] for s in scenes)
        page_estimate = max(1, int(total_lines / 55))

        return {
            "page_estimate": page_estimate,
            "scene_count": len(scenes),
            "scenes": scenes
        }

    def _finalize_scene(self, scene):
        return {
            "header": scene.get("heading", scene.get("header", "<unknown>")),
            "characters": list(scene["characters"]),
            "dialogue_lines": scene["dialogue_lines"],
            "action_lines": scene["action_lines"]
        }


def load_fountain(path_or_text):
    loader = FountainLoader()
    # if path_or_text is a path to a file, read its contents
    try:
        p = Path(path_or_text)
        if p.exists() and p.is_file():
            text = p.read_text(encoding='utf-8')
        else:
            text = path_or_text
    except Exception:
        text = path_or_text
    return loader.load(text)

