import xml.etree.ElementTree as ET

def clean_text(text: str) -> str:
    return text.strip().replace("\n", "").replace("\r", "")

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
    current_character = None  # Track current speaking character

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
                "characters": set(),  # Track characters in this scene
                "dialogue_map": {}  # Map character to their dialogue
            }
            current_character = None

        elif p_type == "Character":
            # Character name paragraph
            if current_scene and text:
                char_name = text.upper().strip()
                current_character = char_name
                current_scene["characters"].add(char_name)
                if char_name not in current_scene["dialogue_map"]:
                    current_scene["dialogue_map"][char_name] = []

        elif p_type == "Dialogue":
            # Dialogue paragraph - associate with current character
            if current_scene and text and current_character:
                current_scene["dialogue_map"][current_character].append(text)
                current_scene["lines"].append(f"{current_character}: {text}")
            elif current_scene and text:
                current_scene["lines"].append(text)

        elif p_type == "Action":
            # Action paragraph
            if current_scene and text:
                current_scene["lines"].append(text)
            current_character = None  # Reset character on action

        elif current_scene and text:
            # Other content
            current_scene["lines"].append(text)

    # Don't forget last scene
    if current_scene:
        scenes.append(current_scene)

    # Convert character sets to lists and compute counts for each scene
    all_characters = set()
    for scene in scenes:
        scene['characters'] = sorted(list(scene.get('characters', set())))
        all_characters.update(scene['characters'])
        
        # Compute line counts
        d, a = compute_line_counts(scene.get('lines', []))
        scene['dialogue_lines'] = d
        scene['action_lines'] = a
        
        # Remove dialogue_map from output (internal use only)
        scene.pop('dialogue_map', None)

    return {
        "scenes": scenes,
        "characters": sorted(list(all_characters)),
        "scene_count": len(scenes)
    }
