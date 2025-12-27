import json
from .shared_utils import clean_text, extract_characters


def load_celtx(path):
    """
    Celtx screenplay JSON loader
    Accepts:
      - .celtx
      - .json
      - .celtx.json
    Output returns unified structure:
      scenes = [ { heading, lines[], characters[] } ]
      characters = [unique character names]
    """

    # Load Celtx structured JSON
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    scenes = []

    for scene in data.get("scenes", []):
        heading = clean_text(scene.get("title", "UNTITLED SCENE"))
        lines = [clean_text(l) for l in scene.get("lines", [])]

        scenes.append({
            "heading":    heading,
            "lines":      lines,
            "characters": extract_characters("\n".join(lines)),
            "dialogue_lines": 0,
            "action_lines": 0
        })

    # compute counts & Flatten character list across all scenes
    for sc in scenes:
        # Simple heuristic: lines with ? or ! are dialogue, rest are action
        lines = sc.get('lines', [])
        dialogue_count = sum(1 for line in lines if line.endswith(('?', '!')))
        sc['dialogue_lines'] = dialogue_count
        sc['action_lines'] = len(lines) - dialogue_count
    characters = sorted({c for s in scenes for c in s['characters']})

    return {
        "scenes": scenes,
        "characters": characters
    }

