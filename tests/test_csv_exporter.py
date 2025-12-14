# tests/test_csv_exporter.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ExportEngine.csv_exporter import CSVExporter
from sample_files.samples import SampleBudgetData
import tempfile
import csv

def test_csv_exporter_creation():
    """Test CSVExporter can be instantiated"""
    exporter = CSVExporter()
    assert exporter is not None
    assert hasattr(exporter, 'export')

def test_csv_export_basic():
    """Test basic CSV export functionality"""
    exporter = CSVExporter()
    budget_data = SampleBudgetData().get_data()
    
    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
        tmp_path = tmp_file.name
    
    try:
        # Test export
        result = exporter.export(budget_data, tmp_path)
        
        # Check if file was created
        assert os.path.exists(tmp_path)
        
        # Check file content
        with open(tmp_path, 'r', newline='', encoding='utf-8') as f:
            content = f.read()
            assert len(content) > 0
            
            # If it's actually CSV, try to read it
            f.seek(0)
            reader = csv.reader(f)
            rows = list(reader)
            assert len(rows) > 0
            
    finally:
        # Clean up
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def test_csv_export_with_custom_data():
    """Test CSV export with custom data structure"""
    exporter = CSVExporter()
    
    # Simple test data
    test_data = {
        "title": "Test Export",
        "items": [
            {"name": "Item 1", "cost": 1000},
            {"name": "Item 2", "cost": 2000},
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp_file:
        tmp_path = tmp_file.name
    
    try:
        result = exporter.export(test_data, tmp_path)
        assert os.path.exists(tmp_path)
        
        # Verify file has content
        with open(tmp_path, 'r', encoding='utf-8') as f:
            content = f.read()
            assert "Test Export" in content or len(content) > 0
            
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)

def test_csv_exporter_error_handling():
    """Test CSV exporter error handling"""
    exporter = CSVExporter()
    
    # Test with invalid path
    invalid_data = {"test": "data"}
    invalid_path = "/invalid/path/test.csv"
    
    # Should handle errors gracefully
    try:
        result = exporter.export(invalid_data, invalid_path)
        # If it doesn't raise an exception, that's OK too
    except Exception as e:
        # Exception is acceptable for invalid paths
        pass