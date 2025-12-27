# tests/test_validation.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

# Now import correctly
from validation import validate_parsed_script

# If you need any other imports from your project, add them here
# Example:
# from ScriptIngest import parse_script
# from errors import ValidationError

import pytest

# Your existing test code below...
def test_validation_basic():
    """Test basic validation functionality"""
    # Example test - replace with your actual test code
    sample_data = {
        "title": "Test Script",
        "scenes": [],
        "characters": []
    }
    
    result = validate_parsed_script(sample_data)
    
    # Assert something about the result
    # assert result is True or has expected properties
    # This depends on what validate_parsed_script returns

# Add more test functions as needed
def test_validation_with_invalid_data():
    """Test validation with invalid input"""
    # Your test code here
    pass

def test_validation_with_missing_fields():
    """Test validation when required fields are missing"""
    # Your test code here
    pass

# Add any other tests you have in your original file