"""
Script Generator for Scale Testing
Phase 13.3: Generate realistic FDX scripts with varying sizes

Creates test scripts with:
- Multiple characters with different roles
- Mix of dialogue and action scenes
- Realistic scene headings and content
- Emotional variety in dialogue
"""

import random
import os


class ScriptGenerator:
    """Generates realistic screenplay content."""
    
    def __init__(self):
        self.locations = [
            "INT. APARTMENT", "EXT. CITY STREET", "INT. COFFEE SHOP",
            "EXT. PARK", "INT. OFFICE", "INT. RESTAURANT", "EXT. ROOFTOP",
            "INT. POLICE STATION", "EXT. PARKING LOT", "INT. HOSPITAL",
            "EXT. BEACH", "INT. WAREHOUSE", "INT. BAR", "EXT. ALLEY",
            "INT. COURTHOUSE", "EXT. HIGHWAY", "INT. SUBWAY", "INT. GALLERY"
        ]
        
        self.times = ["DAY", "NIGHT", "DAWN", "DUSK", "MORNING", "EVENING"]
        
        self.characters = [
            "SARAH", "MARCUS", "DETECTIVE CHEN", "ELIJAH", "DR. RODRIGUEZ",
            "JAMES", "MARIA", "CAPTAIN WILLIAMS", "ALEX", "RACHEL",
            "THOMAS", "LISA", "OFFICER MARTINEZ", "EMMA", "DAVID"
        ]
        
        self.dialogue_templates = [
            "We need to talk about what happened.",
            "I can't believe you did this.",
            "There's something I need to tell you.",
            "This isn't what it looks like.",
            "You don't understand the situation.",
            "We're running out of time.",
            "I've been thinking about us.",
            "What are you going to do now?",
            "This changes everything.",
            "I never wanted it to end this way.",
            "You have to trust me on this.",
            "There's no turning back now.",
            "I'm not sure I can help you.",
            "We've come too far to stop.",
            "This is bigger than both of us."
        ]
        
        self.action_templates = [
            "{char} enters the room, looking around nervously.",
            "{char} sits down and pulls out a folder.",
            "{char} glances at the door, then back.",
            "{char} picks up the phone and hesitates.",
            "{char} walks to the window, deep in thought.",
            "{char} slams the table in frustration.",
            "{char} checks their watch anxiously.",
            "{char} paces back and forth.",
            "{char} reaches for something in their pocket.",
            "{char} stares at the photograph on the wall."
        ]
    
    def generate_scene_heading(self):
        """Generate random scene heading."""
        location = random.choice(self.locations)
        time = random.choice(self.times)
        return f"{location} - {time}"
    
    def generate_action(self, character=None):
        """Generate action line."""
        if character and random.random() > 0.3:
            template = random.choice(self.action_templates)
            return template.format(char=character)
        
        generic_actions = [
            "The room is dimly lit. Papers scattered everywhere.",
            "A phone rings in the distance.",
            "Footsteps echo down the hallway.",
            "Rain begins to fall outside.",
            "Sirens wail in the distance.",
            "The door slowly creaks open.",
            "A car speeds by outside.",
            "The lights flicker momentarily."
        ]
        return random.choice(generic_actions)
    
    def generate_dialogue(self):
        """Generate dialogue line."""
        return random.choice(self.dialogue_templates)
    
    def generate_scene(self, scene_num, characters_in_scene):
        """Generate a complete scene."""
        heading = self.generate_scene_heading()
        
        lines = []
        
        # Opening action
        lines.append(f'    <Paragraph Type="Action">{self.generate_action()}</Paragraph>')
        
        # Dialogue exchanges (2-5 exchanges)
        num_exchanges = random.randint(2, 5)
        for _ in range(num_exchanges):
            char = random.choice(characters_in_scene)
            
            # Character action
            if random.random() > 0.5:
                lines.append(f'    <Paragraph Type="Action">{self.generate_action(char)}</Paragraph>')
            
            # Character name and dialogue
            lines.append(f'    <Paragraph Type="Character">{char}</Paragraph>')
            
            # Parenthetical occasionally
            if random.random() > 0.7:
                parentheticals = ["quietly", "whispered", "shouting", "to themselves", "angry"]
                lines.append(f'    <Paragraph Type="Parenthetical">({random.choice(parentheticals)})</Paragraph>')
            
            lines.append(f'    <Paragraph Type="Dialogue">{self.generate_dialogue()}</Paragraph>')
        
        # Closing action
        if random.random() > 0.3:
            lines.append(f'    <Paragraph Type="Action">{self.generate_action()}</Paragraph>')
        
        scene_xml = f'    <Paragraph Type="Scene Heading">{heading}</Paragraph>\n'
        scene_xml += '\n'.join(lines)
        
        return scene_xml
    
    def generate_script(self, num_scenes, output_path):
        """Generate complete FDX script with specified number of scenes."""
        print(f"\n🎬 Generating {num_scenes}-scene script...")
        
        # Select main characters (60% of all characters appear frequently)
        num_main_chars = max(3, len(self.characters) * 60 // 100)
        main_characters = random.sample(self.characters, num_main_chars)
        
        scenes = []
        for i in range(num_scenes):
            # 2-4 characters per scene
            num_chars = random.randint(2, min(4, len(main_characters)))
            scene_chars = random.sample(main_characters, num_chars)
            
            scene_xml = self.generate_scene(i+1, scene_chars)
            scenes.append(scene_xml)
            
            if (i + 1) % 10 == 0:
                print(f"  Generated {i+1}/{num_scenes} scenes...")
        
        # Build complete FDX file
        fdx_content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<FinalDraft DocumentType="Script" Template="No" Version="1">
  <Content>
'''
        fdx_content += '\n\n'.join(scenes)
        fdx_content += '''
  </Content>
</FinalDraft>
'''
        
        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(fdx_content)
        
        print(f"✅ Generated: {output_path}")
        print(f"   Scenes: {num_scenes}")
        print(f"   Main Characters: {len(main_characters)}")
        
        return output_path


if __name__ == "__main__":
    generator = ScriptGenerator()
    
    # Create samples directory if it doesn't exist
    os.makedirs("samples/scale_tests", exist_ok=True)
    
    # Generate test scripts of various sizes
    test_sizes = [10, 25, 50, 75, 100]
    
    print("="*60)
    print("SCRIPT GENERATOR - Scale Testing")
    print("="*60)
    
    generated_files = []
    
    for size in test_sizes:
        output_file = f"samples/scale_tests/test_script_{size}scenes.fdx"
        generator.generate_script(size, output_file)
        generated_files.append((size, output_file))
    
    print(f"\n{'='*60}")
    print("GENERATION COMPLETE")
    print(f"{'='*60}")
    print(f"Generated {len(generated_files)} test scripts:")
    for size, path in generated_files:
        file_size = os.path.getsize(path) / 1024
        print(f"  {size:3d} scenes: {path} ({file_size:.1f} KB)")
    print(f"{'='*60}\n")
