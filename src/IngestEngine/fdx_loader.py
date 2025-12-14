import xml.etree.ElementTree as ET

def clean_text(text: str) -> str:
    return text.strip().replace("\n", "").replace("\r", "")

def extract_characters(lines):
    """Extract character names from lines."""
    chars = set()
    for line in lines:
        if isinstance(line, str) and line.isupper() and 1 < len(line.split()) <= 4:
            chars.add(line.strip())
    return list(chars)

def compute_line_counts(lines):
    """Compute dialogue and action line counts.
    
    Heuristic: lines ending with punctuation or all-caps short lines = dialogue
    """
    dialogue = 0
    action = 0
    for line in lines or []:
        t = str(line).strip()
        if not t:
            continue
        if t.isupper() and len(t.split()) <= 6:
            dialogue += 1
        elif t.endswith(('.', '!', '?', ':')):
            dialogue += 1
        else:
            action += 1
    return dialogue, action

def load_fdx(path):
    """Load FDX (Final Draft XML) screenplay and extract scenes.
    
    Returns dict with: scenes[], characters[], scene_count
    Each scene has: heading, lines, characters, dialogue_lines, action_lines
    """
    tree = ET.parse(path)
    root = tree.getroot()

    scenes = []
    current_scene = None

    for elem in root.iter("Paragraph"):
        text = clean_text("".join(elem.itertext()))
        p_type = elem.get("Type", "")

        if p_type == "Scene Heading":
            # Save previous scene
            if current_scene:
                scenes.append(current_scene)

            # Start new scene
            current_scene = {
                "heading": text,
                "lines": []
            }

        elif current_scene and text:
            # Add all other content to current scene
            current_scene["lines"].append(text)

    # Don't forget last scene
    if current_scene:
        scenes.append(current_scene)

    # Extract characters and compute counts for each scene
    for scene in scenes:
        scene['characters'] = extract_characters(scene.get('lines', []))
        d, a = compute_line_counts(scene.get('lines', []))
        scene['dialogue_lines'] = d
        scene['action_lines'] = a

    return {
        "scenes": scenes,
        "characters": sorted(set(c for s in scenes for c in s.get("characters", []))),
        "scene_count": len(scenes)
    }
