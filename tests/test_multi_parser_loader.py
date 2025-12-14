"""
Comprehensive tests for MultiParserLoader
"""

import unittest
import tempfile
import os
from typing import Dict, Any
from src.IngestEngine.multi_parser_loader import MultiParserLoader, load_script, detect_file_format
from tests.sample_files.samples import SampleScripts

class TestMultiParserLoader(unittest.TestCase):
    """Test suite for MultiParserLoader"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.parser = MultiParserLoader()
        self.samples = SampleScripts.get_all_samples()
    
    # ==================== BASIC FUNCTIONALITY TESTS ====================
    
    def test_parser_initialization(self):
        """Test that parser initializes correctly"""
        self.assertIsInstance(self.parser, MultiParserLoader)
        self.assertIn('fdx', self.parser.supported_formats)
        self.assertIn('fountain', self.parser.supported_formats)
        self.assertIn('pdf', self.parser.supported_formats)
    
    def test_load_script_convenience_function(self):
        """Test the convenience load_script function"""
        content = self.samples['plain_text']
        result = load_script(content, 'text')
        self.assertIsInstance(result, dict)
        self.assertIn('scenes', result)
        self.assertIn('scene_count', result)
    
    # ==================== PLAIN TEXT PARSING TESTS ====================
    
    def test_parse_plain_text(self):
        """Test plain text parsing"""
        content = self.samples['plain_text']
        result = self.parser.parse(content, 'text')
        
        self.assertEqual(result['scene_count'], 2)
        self.assertGreater(len(result['scenes']), 0)
        self.assertIn('JANE', result['characters'])
        self.assertIn('JOHN', result['characters'])
        
        # Check scene headers
        scene_headers = [scene['header'] for scene in result['scenes']]
        self.assertIn('INT. COFFEE SHOP - DAY', scene_headers)
        self.assertIn('EXT. COFFEE SHOP - NIGHT', scene_headers)
    
    def test_parse_plain_text_with_scene_numbers(self):
        """Test plain text with scene numbers"""
        content = self.samples['plain_text_numbers']
        result = self.parser.parse(content, 'text')
        
        self.assertEqual(result['scene_count'], 2)
        scenes = result['scenes']
        self.assertEqual(scenes[0]['scene_number'], 1)
        self.assertEqual(scenes[1]['scene_number'], 2)
    
    def test_parse_minimal_scenes(self):
        """Test parsing script with minimal content"""
        content = self.samples['minimal_scenes']
        result = self.parser.parse(content, 'text')
        
        self.assertEqual(result['scene_count'], 3)
        self.assertEqual(len(result['characters']), 0)  # No characters
    
    def test_parse_no_scenes(self):
        """Test parsing text without scene headings"""
        content = self.samples['no_scenes']
        result = self.parser.parse(content, 'text')
        
        # Should create one scene with all content
        self.assertEqual(result['scene_count'], 1)
        self.assertEqual(result['scenes'][0]['header'], 'SCRIPT')
    
    # ==================== FOUNTAIN PARSING TESTS ====================
    
    def test_parse_fountain(self):
        """Test Fountain format parsing"""
        content = self.samples['fountain']
        result = self.parser.parse(content, 'fountain')
        
        self.assertEqual(result['scene_count'], 3)
        self.assertIn('SARAH', result['characters'])
        self.assertIn('MIKE', result['characters'])
        self.assertIn('BARISTA', result['characters'])
        
        # Check metadata extraction
        self.assertEqual(result['metadata']['title'], 'The Coffee Shop Chronicles')
        self.assertEqual(result['metadata']['author'], 'Alex Writer')
        
        # Check transitions
        transitions = []
        for scene in result['scenes']:
            for element in scene.get('elements', []):
                if element['type'] == 'transition':
                    transitions.append(element['text'])
        
        self.assertIn('CUT TO:', transitions)
        self.assertIn('DISSOLVE TO:', transitions)
    
    def test_parse_fountain_minimal(self):
        """Test minimal Fountain format"""
        content = self.samples['fountain_minimal']
        result = self.parser.parse(content, 'fountain')
        
        self.assertEqual(result['scene_count'], 2)
        self.assertIn('DAVID', result['characters'])
    
    # ==================== FDX PARSING TESTS ====================
    
    def test_parse_fdx_xml(self):
        """Test FDX XML parsing"""
        content = self.samples['fdx_xml']
        result = self.parser.parse(content, 'fdx')
        
        self.assertEqual(result['scene_count'], 2)
        self.assertIn('DETECTIVE MILLER', result['characters'])
        self.assertIn('SUSPECT', result['characters'])
        
        # Check element types
        scene = result['scenes'][0]
        element_types = [e['type'] for e in scene['elements']]
        
        self.assertIn('scene_heading', element_types)
        self.assertIn('action', element_types)
        self.assertIn('character', element_types)
        self.assertIn('dialogue', element_types)
        self.assertIn('parenthetical', element_types)
    
    # ==================== CELTX PARSING TESTS ====================
    
    def test_parse_celtx_xml(self):
        """Test Celtx XML parsing"""
        content = self.samples['celtx_xml']
        result = self.parser.parse(content, 'celtx')
        
        self.assertEqual(result['scene_count'], 2)
        self.assertIn('EMILY', result['characters'])
        self.assertIn('LIBRARIAN', result['characters'])
        
        # Check metadata
        self.assertEqual(result['metadata']['format_type'], 'Celtx')
    
    def test_parse_celtx_html(self):
        """Test Celtx HTML parsing"""
        content = self.samples['celtx_html']
        result = self.parser.parse(content, 'celtx')
        
        # Should parse or fallback gracefully
        self.assertIsInstance(result, dict)
        self.assertIn('scenes', result)
    
    # ==================== PDF PARSING TESTS ====================
    
    def test_parse_pdf_text(self):
        """Test PDF text extraction parsing"""
        content = self.samples['pdf_text']
        # Convert to bytes to simulate PDF
        content_bytes = content.encode('utf-8')
        
        # Mock PDF detection by passing as bytes
        result = self.parser.parse(content_bytes, 'pdf')
        
        self.assertGreater(result['scene_count'], 0)
        self.assertIn('ALICE', result['characters'])
        
        # Check format info
        self.assertEqual(result['format_info']['detected_format'], 'pdf')
    
    # ==================== FADE IN PARSING TESTS ====================
    
    def test_parse_fadein_xml(self):
        """Test Fade In XML parsing"""
        content = self.samples['fadein_xml']
        result = self.parser.parse(content, 'fadein')
        
        self.assertEqual(result['scene_count'], 2)
        self.assertIn('PILOT', result['characters'])
        self.assertIn('COMPUTER', result['characters'])
    
    def test_parse_fadein_text(self):
        """Test Fade In text parsing"""
        content = self.samples['fadein_text']
        result = self.parser.parse(content, 'fadein')
        
        self.assertEqual(result['scene_count'], 1)
        self.assertIn('PILOT', result['characters'])
    
    # ==================== FORMAT DETECTION TESTS ====================
    
    def test_detect_format_from_extension(self):
        """Test format detection from filename extension"""
        # Test various extensions
        self.assertEqual(
            detect_file_format('script.fdx', b'dummy content'),
            'fdx'
        )
        self.assertEqual(
            detect_file_format('screenplay.fountain', b'dummy content'),
            'fountain'
        )
        self.assertEqual(
            detect_file_format('movie_script.pdf', b'dummy content'),
            'pdf'
        )
        self.assertEqual(
            detect_file_format('play.celtx', b'dummy content'),
            'celtx'
        )
        self.assertEqual(
            detect_file_format('script.txt', b'dummy content'),
            'txt'
        )
    
    def test_detect_format_from_content(self):
        """Test format detection from content analysis"""
        # FDX detection
        fdx_content = self.samples['fdx_xml'].encode('utf-8')
        self.assertEqual(
            self.parser.detect_format_from_content(fdx_content),
            'fdx'
        )
        
        # Fountain detection
        fountain_content = self.samples['fountain'].encode('utf-8')
        self.assertEqual(
            self.parser.detect_format_from_content(fountain_content),
            'fountain'
        )
        
        # Plain text detection
        text_content = self.samples['plain_text'].encode('utf-8')
        self.assertEqual(
            self.parser.detect_format_from_content(text_content),
            'text'
        )
    
    def test_detect_format_mixed(self):
        """Test format detection with both filename and content"""
        # Content should override wrong extension
        fountain_content = self.samples['fountain'].encode('utf-8')
        detected = detect_file_format('wrong_extension.txt', fountain_content)
        self.assertEqual(detected, 'fountain')
    
    # ==================== SPECIAL CASE TESTS ====================
    
    def test_parse_unicode_content(self):
        """Test parsing content with Unicode characters"""
        content = self.samples['unicode']
        result = self.parser.parse(content, 'text')
        
        self.assertEqual(result['scene_count'], 2)
        self.assertIn('PIÉRRE', result['characters'])
        self.assertIn('MARIE', result['characters'])
    
    def test_parse_complex_character_names(self):
        """Test parsing complex character names"""
        content = self.samples['complex_chars']
        result = self.parser.parse(content, 'text')
        
        characters = result['characters']
        # Check various character name formats
        self.assertIn('KING ARTHUR VII', characters)
        self.assertIn('SIR LANCELOT-DU-LAC', characters)
        self.assertIn('DR. JOHN SMITH, PH.D.', characters)
        self.assertIn('MARY-ANN', characters)
        self.assertIn('A.I. VOICE', characters)
    
    def test_parse_mixed_format(self):
        """Test parsing mixed format content"""
        content = self.samples['mixed_format']
        result = self.parser.parse(content, 'text')
        
        # Should parse despite mixed format
        self.assertGreater(result['scene_count'], 0)
        self.assertIn('ENGINEER', result['characters'])
    
    def test_parse_feature_excerpt(self):
        """Test parsing feature-length excerpt"""
        content = self.samples['feature_excerpt']
        result = self.parser.parse(content, 'text')
        
        self.assertEqual(result['scene_count'], 5)
        characters = result['characters']
        self.assertIn('FIGURE', characters)
        self.assertIn('LEADER', characters)
        self.assertIn('CLIMBER 1', characters)
        self.assertIn('CLIMBER 2', characters)
        self.assertIn('DOCTOR', characters)
    
    # ==================== ERROR HANDLING TESTS ====================
    
    def test_parse_invalid_fdx(self):
        """Test parsing invalid FDX content"""
        invalid_xml = "Not XML at all"
        result = self.parser.parse(invalid_xml, 'fdx')
        
        # Should fallback to plain text
        self.assertEqual(result['format_info']['detected_format'], 'text')
        self.assertIn('error', result['format_info'])
    
    def test_parse_empty_content(self):
        """Test parsing empty content"""
        result = self.parser.parse('', 'text')
        
        self.assertEqual(result['scene_count'], 0)
        self.assertEqual(len(result['characters']), 0)
    
    def test_parse_whitespace_only(self):
        """Test parsing whitespace-only content"""
        result = self.parser.parse('   \n\n   \n', 'text')
        
        self.assertEqual(result['scene_count'], 0)
        self.assertEqual(len(result['characters']), 0)
    
    # ==================== METADATA TESTS ====================
    
    def test_metadata_extraction(self):
        """Test metadata extraction from various formats"""
        # Fountain with metadata
        fountain_result = self.parser.parse(
            self.samples['fountain'], 
            'fountain'
        )
        self.assertEqual(fountain_result['metadata']['title'], 'The Coffee Shop Chronicles')
        self.assertEqual(fountain_result['metadata']['author'], 'Alex Writer')
        
        # Plain text without metadata
        text_result = self.parser.parse(
            self.samples['plain_text'],
            'text'
        )
        self.assertEqual(text_result['metadata']['format_type'], 'Plain Text')
    
    # ==================== PROCESSING STATS TESTS ====================
    
    def test_processing_stats_included(self):
        """Test that processing stats are included in results"""
        content = self.samples['plain_text']
        result = self.parser.parse(content, 'text')
        
        self.assertIn('processing_stats', result)
        stats = result['processing_stats']
        
        self.assertIn('parse_time_seconds', stats)
        self.assertIn('timestamp', stats)
        self.assertIsInstance(stats['parse_time_seconds'], float)
    
    # ==================== REAL FILE TESTS ====================
    
    def test_parse_with_temp_files(self):
        """Test parsing with actual temporary files"""
        # Create temporary files for different formats
        formats_to_test = [
            ('test.fdx', self.samples['fdx_xml'], 'fdx'),
            ('test.fountain', self.samples['fountain'], 'fountain'),
            ('test.txt', self.samples['plain_text'], 'text'),
        ]
        
        for filename, content, expected_format in formats_to_test:
            with tempfile.NamedTemporaryFile(
                mode='w',
                suffix=filename.split('.')[-1],
                delete=False,
                encoding='utf-8'
            ) as tmp_file:
                tmp_file.write(content)
                tmp_path = tmp_file.name
            
            try:
                # Read file and parse
                with open(tmp_path, 'rb') as f:
                    file_content = f.read()
                
                # Detect format
                detected = detect_file_format(tmp_path, file_content)
                self.assertEqual(detected, expected_format)
                
                # Parse
                result = self.parser.parse(file_content, detected)
                self.assertIsInstance(result, dict)
                self.assertIn('scenes', result)
                
            finally:
                # Clean up
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
    
    # ==================== ALTERNATIVE FORMATS TESTS ====================
    
    def test_parse_commercial_script(self):
        """Test parsing commercial/AV script format"""
        content = self.samples['commercial']
        result = self.parser.parse(content, 'text')
        
        # Should parse as a single scene
        self.assertEqual(result['scene_count'], 1)
    
    def test_parse_two_column_script(self):
        """Test parsing two-column AV script"""
        content = self.samples['two_column']
        result = self.parser.parse(content, 'text')
        
        # Should parse despite non-standard format
        self.assertIsInstance(result, dict)
        self.assertIn('scenes', result)
    
    def test_parse_stage_play(self):
        """Test parsing stage play format"""
        content = self.samples['stage_play']
        result = self.parser.parse(content, 'text')
        
        self.assertEqual(result['scene_count'], 1)
        self.assertIn('JOHN', result['characters'])
        self.assertIn('MARY', result['characters'])
    
    # ==================== BATCH PROCESSING TEST ====================
    
    def test_batch_parsing(self):
        """Test parsing multiple formats in sequence"""
        formats = [
            ('text', self.samples['plain_text']),
            ('fountain', self.samples['fountain']),
            ('fdx', self.samples['fdx_xml']),
            ('celtx', self.samples['celtx_xml']),
        ]
        
        for format_type, content in formats:
            with self.subTest(format=format_type):
                result = self.parser.parse(content, format_type)
                
                # Basic validation
                self.assertIsInstance(result, dict)
                self.assertIn('scenes', result)
                self.assertIn('scene_count', result)
                self.assertIn('characters', result)
                self.assertIn('metadata', result)
                
                # Specific validations
                self.assertGreaterEqual(result['scene_count'], 1)
                self.assertIsInstance(result['characters'], list)
    
    # ==================== PERFORMANCE TESTS ====================
    
    def test_parsing_speed(self):
        """Test parsing speed for typical script"""
        content = self.samples['feature_excerpt']
        
        import time
        start_time = time.time()
        
        result = self.parser.parse(content, 'text')
        
        end_time = time.time()
        parse_time = end_time - start_time
        
        # Should parse in reasonable time (< 0.5 seconds for this size)
        self.assertLess(parse_time, 0.5)
        
        # Verify result
        self.assertEqual(result['scene_count'], 5)
        self.assertGreater(len(result['characters']), 0)
        
        # Check processing stats
        self.assertLess(result['processing_stats']['parse_time_seconds'], 0.5)
    
    # ==================== ELEMENT TYPE TESTS ====================
    
    def test_element_type_classification(self):
        """Test that element types are correctly classified"""
        content = self.samples['fountain']
        result = self.parser.parse(content, 'fountain')
        
        # Collect all element types
        element_types = set()
        for scene in result['scenes']:
            for element in scene.get('elements', []):
                element_types.add(element['type'])
        
        # Should have various element types
        expected_types = {'scene_heading', 'action', 'character', 'dialogue', 'transition'}
        for expected in expected_types:
            self.assertIn(expected, element_types)
    
    def test_scene_location_time_extraction(self):
        """Test extraction of location and time from scene headings"""
        content = self.samples['plain_text']
        result = self.parser.parse(content, 'text')
        
        scenes = result['scenes']
        
        # Check first scene
        self.assertEqual(scenes[0]['location'], 'INTERIOR')
        self.assertEqual(scenes[0]['time_of_day'], 'DAY')
        
        # Check second scene
        self.assertEqual(scenes[1]['location'], 'EXTERIOR')
        self.assertEqual(scenes[1]['time_of_day'], 'NIGHT')
    
    # ==================== EDGE CASE TESTS ====================
    
    def test_parse_single_line(self):
        """Test parsing single line content"""
        result = self.parser.parse('INT. ROOM - DAY', 'text')
        self.assertEqual(result['scene_count'], 1)
        self.assertEqual(result['scenes'][0]['header'], 'INT. ROOM - DAY')
    
    def test_parse_only_characters(self):
        """Test parsing content with only character names"""
        content = """JOHN
MARY
DAVID"""
        result = self.parser.parse(content, 'text')
        
        # Should create one scene
        self.assertEqual(result['scene_count'], 1)
        self.assertEqual(len(result['characters']), 3)
    
    def test_parse_with_parentheticals(self):
        """Test parsing parentheticals"""
        content = """INT. ROOM - DAY

JOHN
(smiling)
Hello there.

MARY
(not looking up)
Hi."""
        
        result = self.parser.parse(content, 'text')
        
        # Check parenthetical elements
        parentheticals = []
        for scene in result['scenes']:
            for element in scene.get('elements', []):
                if element['type'] == 'parenthetical':
                    parentheticals.append(element['text'])
        
        self.assertIn('(smiling)', parentheticals)
        self.assertIn('(not looking up)', parentheticals)


if __name__ == '__main__':
    unittest.main()