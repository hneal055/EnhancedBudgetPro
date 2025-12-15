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
    all_characters = set()

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
                "lines": [],
                "characters": []
            }

        elif p_type == "Character" and current_scene and text:
            # Extract character name (remove parentheticals like "(V.O.)")
            char_name = text.split("(")[0].strip().upper()
            if char_name:
                current_scene["characters"].append(char_name)
                all_characters.add(char_name)
                # Store last speaking character for next dialogue line
                current_scene["_last_speaker"] = char_name

        elif p_type == "Dialogue" and current_scene and text:
            # Dialogue line - attach to last speaking character
            speaker = current_scene.get("_last_speaker", "UNKNOWN")
            current_scene["lines"].append({
                "type": "dialogue",
                "character": speaker,
                "text": text
            })

        elif current_scene and text:
            # Action, parenthetical, or other content
            line_type = "action" if p_type in ["Action", ""] else p_type.lower()
            current_scene["lines"].append({
                "type": line_type,
                "character": None,
                "text": text
            })

    # Don't forget last scene
    if current_scene:
        scenes.append(current_scene)

    # Compute line counts for each scene
    for scene in scenes:
        # Remove duplicates from characters list while preserving order
        scene['characters'] = list(dict.fromkeys(scene['characters']))
        # Remove temp tracking field
        scene.pop('_last_speaker', None)
        d, a = compute_line_counts(scene.get('lines', []))
        scene['dialogue_lines'] = d
        scene['action_lines'] = a

    return {
        "scenes": scenes,
        "characters": sorted(list(all_characters)),
        "scene_count": len(scenes)
    }