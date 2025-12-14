from pdfminer.high_level import extract_text
from .shared_utils import clean_text, extract_characters, compute_counts


def load_pdf(path):
    text = extract_text(path)
    lines = [clean_text(l) for l in text.split("\n") if l.strip()]

    scenes = []
    scene = None

    for line in lines:
        if line.startswith(("INT.", "EXT.", "INT/EXT.", "EST.")):
            if scene:
                scenes.append(scene)
            scene = {"heading": line, "lines": []}
        elif scene:
            scene["lines"].append(line)

    if scene:
        scenes.append(scene)

    for s in scenes:
        s['characters'] = extract_characters(s['lines'])
        d,a = compute_counts(s.get('lines', []))
        s['dialogue_lines'] = d
        s['action_lines'] = a

    return {
        "scenes": scenes,
        "characters": sorted({c for s in scenes for c in s["characters"]})
    }

