def normalize_scene(scene: dict) -> dict:
    return {
        "heading": str(scene.get("heading", "")).strip(),
        "lines": [str(l).strip() for l in scene.get("lines", []) if str(l).strip()],
        "characters": sorted(set(
            c.strip().upper()
            for c in scene.get("characters", [])
            if is_valid_character(c)
        )),
        "dialogue_lines": int(scene.get("dialogue_lines", 0)),
        "action_lines": int(scene.get("action_lines", 0))
    }
