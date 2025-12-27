# tests/sample_files/samples.py
import os

class SampleScript:
    """Sample screenplay data for testing"""
    
    def __init__(self):
        self.content = """FADE IN:

INT. COFFEE SHOP - DAY

A small, indie coffee shop. JESSICA (30s, creative type) types on her laptop.

JEFF (40s, business casual) enters, looking around.

JEFF
Jessica?

JESSICA
(looking up)
Jeff! Over here.

Jeff approaches her table.

JEFF (O.S.)
Nice place. Good for writing?

JESSICA
It's perfect. Quiet, good coffee.

FADE TO BLACK:

FADE IN:

EXT. CITY STREET - NIGHT

Rain falls lightly. Jessica and Jeff walk together under an umbrella.

JESSICA
So, what did you think of the script?

JEFF
It's good. Strong characters. The father-son dynamic really works.

JESSICA
Thanks. I was worried about the neighborhood father subplot.

JEFF
No, it adds depth. Speaking of which...

MONTAGE - VARIOUS LOCATIONS

1. INT. APARTMENT - DAY - Jessica writes feverishly.
2. EXT. PARK - DAY - Jeff reads pages on a bench.
3. INT. COFFEE SHOP - NIGHT - They discuss revisions.

END MONTAGE

INT. PRODUCTION OFFICE - DAY

Jessica and Jeff sit with SARAH (50s, producer).

SARAH
The budget's tight. We need to consolidate locations.

JEFF
The coffee shop scenes can all be shot at one location.

JESSICA
And the park is public, no fees.

FADE OUT.

THE END
"""
    
    def get_content(self):
        """Return the screenplay content"""
        return self.content
    
    def get_file_path(self, format="fountain"):
        """Return a sample file path"""
        if format == "fountain":
            return "sample_script.fountain"
        elif format == "pdf":
            return "sample_script.pdf"
        elif format == "fdx":
            return "sample_script.fdx"
        return "sample_script.txt"
    
    def get_parsed_structure(self):
        """Return a parsed structure for testing"""
        return {
            "title": "Sample Screenplay",
            "scenes": [
                {
                    "number": 1,
                    "location": "INT. COFFEE SHOP - DAY",
                    "description": "A small, indie coffee shop. JESSICA (30s, creative type) types on her laptop.",
                    "characters": ["JESSICA", "JEFF"],
                    "dialogue_lines": 4
                },
                {
                    "number": 2,
                    "location": "EXT. CITY STREET - NIGHT",
                    "description": "Rain falls lightly. Jessica and Jeff walk together under an umbrella.",
                    "characters": ["JESSICA", "JEFF"],
                    "dialogue_lines": 3
                },
                {
                    "number": 3,
                    "location": "MONTAGE - VARIOUS LOCATIONS",
                    "description": "1. INT. APARTMENT - DAY - Jessica writes feverishly.\n2. EXT. PARK - DAY - Jeff reads pages on a bench.\n3. INT. COFFEE SHOP - NIGHT - They discuss revisions.",
                    "characters": [],
                    "dialogue_lines": 0
                },
                {
                    "number": 4,
                    "location": "INT. PRODUCTION OFFICE - DAY",
                    "description": "Jessica and Jeff sit with SARAH (50s, producer).",
                    "characters": ["JESSICA", "JEFF", "SARAH"],
                    "dialogue_lines": 3
                }
            ],
            "characters": ["JESSICA", "JEFF", "SARAH"],
            "character_cost": 3,
            "page_count": 5.2,
            "locations": ["COFFEE SHOP", "CITY STREET", "APARTMENT", "PARK", "PRODUCTION OFFICE"],
            "transitions": ["FADE IN:", "FADE TO BLACK:", "FADE IN:", "FADE OUT."]
        }


class SampleBudgetData:
    """Sample budget data for testing"""
    
    def __init__(self):
        self.data = {
            "title": "Sample Film Budget",
            "total_budget": 1500000,
            "breakdown": {
                "above_the_line": {
                    "amount": 300000,
                    "items": [
                        {"name": "Producer", "amount": 100000},
                        {"name": "Director", "amount": 80000},
                        {"name": "Writer", "amount": 60000},
                        {"name": "Principal Cast", "amount": 60000}
                    ]
                },
                "production": {
                    "amount": 800000,
                    "items": [
                        {"name": "Crew", "amount": 300000},
                        {"name": "Equipment", "amount": 200000},
                        {"name": "Locations", "amount": 150000},
                        {"name": "Sets & Construction", "amount": 150000}
                    ]
                },
                "post_production": {
                    "amount": 300000,
                    "items": [
                        {"name": "Editing", "amount": 100000},
                        {"name": "Visual Effects", "amount": 80000},
                        {"name": "Sound Design", "amount": 70000},
                        {"name": "Music", "amount": 50000}
                    ]
                },
                "other": {
                    "amount": 100000,
                    "items": [
                        {"name": "Insurance", "amount": 40000},
                        {"name": "Contingency", "amount": 40000},
                        {"name": "Marketing", "amount": 20000}
                    ]
                }
            },
            "schedule": {
                "pre_production_weeks": 4,
                "production_weeks": 6,
                "post_production_weeks": 8,
                "total_weeks": 18
            }
        }
    
    def get_data(self):
        """Return the budget data"""
        return self.data


class SampleScheduleData:
    """Sample scheduling data for testing"""
    
    def __init__(self):
        self.data = {
            "title": "Sample Production Schedule",
            "scenes": [
                {
                    "scene_number": 1,
                    "location": "COFFEE SHOP",
                    "int_ext": "INT",
                    "day_night": "DAY",
                    "pages": 1.5,
                    "cast": ["JESSICA", "JEFF"],
                    "crew": ["Director", "DP", "Sound", "AD"],
                    "estimated_hours": 8
                },
                {
                    "scene_number": 2,
                    "location": "CITY STREET",
                    "int_ext": "EXT",
                    "day_night": "NIGHT",
                    "pages": 1.2,
                    "cast": ["JESSICA", "JEFF"],
                    "crew": ["Director", "DP", "Sound", "AD", "Gaffer"],
                    "estimated_hours": 10
                }
            ],
            "talent_availability": {
                "JESSICA": ["2024-06-01", "2024-06-15"],
                "JEFF": ["2024-06-05", "2024-06-20"],
                "SARAH": ["2024-06-10", "2024-06-25"]
            },
            "locations": {
                "COFFEE SHOP": {"days_needed": 3, "permit_required": True},
                "CITY STREET": {"days_needed": 2, "permit_required": True},
                "PARK": {"days_needed": 1, "permit_required": True}
            }
        }
    
    def get_data(self):
        """Return the schedule data"""
        return self.data




class SampleScripts:
    """Collection of sample scripts in different formats for testing"""
    
    @staticmethod
    def get_all_samples():
        """Return dictionary of sample scripts in different formats"""
        import os
        samples_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'samples')
        
        # Read actual sample files
        with open(os.path.join(samples_dir, 'test_script.fdx'), 'r') as f:
            fdx_xml = f.read()
        
        with open(os.path.join(samples_dir, 'test_script.fountain'), 'r') as f:
            fountain = f.read()
        
        with open(os.path.join(samples_dir, 'test_script.celtx.json'), 'r') as f:
            celtx_xml = f.read()
        
        plain_text = fountain  # Use fountain as plain text
        
        return {
            'plain_text': plain_text,
            'fountain': fountain,
            'fdx_xml': fdx_xml,
            'fdx_content': fdx_xml,
            'celtx_xml': celtx_xml,
            'celtx_content': celtx_xml,
            'pdf_content': plain_text  # For tests that don't need real PDF
        }
    @staticmethod
    def get_sample_paths():
        """Return dictionary of actual sample file paths"""
        import os
        base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'samples')
        return {
            'fdx': os.path.join(base_path, 'test_script.fdx'),
            'fountain': os.path.join(base_path, 'test_script.fountain'),
            'celtx': os.path.join(base_path, 'test_script.celtx.json')
        }


# Export all classes
__all__ = ['SampleScript', 'SampleBudgetData', 'SampleScheduleData', 'SampleScripts']