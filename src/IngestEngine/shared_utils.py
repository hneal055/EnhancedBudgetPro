# src/IngestEngine/shared_utils.py (minimal version)
import re
from typing import Dict, List, Any

def compute_counts(content: str) -> Dict[str, Any]:
    """
    Basic character and scene counting.
    """
    lines = content.split('\n') if isinstance(content, str) else content
    
    # Simple character detection (uppercase lines not in scene headings)
    characters = set()
    for line in lines:
        stripped = line.strip()
        # Skip scene headings and empty lines
        if stripped and not stripped.startswith(('INT.', 'EXT.', 'I/E.', 'INT/EXT.')):
            # Check if all caps (simple character detection)
            if stripped.isupper() and len(stripped) > 1 and ' ' not in stripped:
                characters.add(stripped)
    
    # Count scenes
    scene_count = 0
    for line in lines:
        if line.strip().startswith(('INT.', 'EXT.', 'I/E.', 'INT/EXT.')):
            scene_count += 1
    
    return {
        "character_count": len(characters),
        "characters": list(characters),
        "scene_count": scene_count,
        "page_count": round(len(lines) / 55.0, 1),
        "line_count": len(lines)
    }

# Add other functions as needed

def clean_text(text: str) -> str:
    """Clean and normalize text."""
    if not text:
        return ""
    
    # Remove extra whitespace
    text = ' '.join(text.split())
    
    # Remove non-printable characters but keep line breaks
    import string
    printable = set(string.printable)
    text = ''.join(filter(lambda x: x in printable, text))
    
    return text.strip()

def extract_characters(content: str) -> list:
    """Extract character names from script content."""
    import re
    
    lines = content.split('\n') if isinstance(content, str) else content
    characters = set()
    
    # Character pattern: uppercase words at line start (not in scene headings)
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip if empty or scene heading
        if not stripped:
            continue
        if stripped.startswith(('INT.', 'EXT.', 'I/E.', 'INT/EXT.')):
            continue
        
        # Check if this looks like a character name
        # Usually all caps, not too long, standalone
        if (stripped.isupper() and 
            1 < len(stripped) < 30 and
            ' ' not in stripped and
            not any(x in stripped for x in ['CONTINUED', 'OMITTED', 'MORE'])):
            
            # Additional check: character names are often followed by dialogue
            is_likely_character = False
            if i + 1 < len(lines):
                next_line = lines[i + 1].strip()
                if next_line.startswith('(') or not next_line:  # Parenthetical or empty line
                    is_likely_character = True
                elif i > 0:
                    prev_line = lines[i - 1].strip()
                    if not prev_line:  # Empty line before character name
                        is_likely_character = True
            
            if is_likely_character:
                characters.add(stripped)
    
    return list(characters)

# Update __all__ to include new functions
# Find the existing __all__ line and update it

__all__ = [
    'compute_counts',
    'normalize_scene_heading', 
    'extract_scene_location',
    'clean_text',
    'extract_characters',
    'validate_parsed_data'
]
