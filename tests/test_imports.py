# tests/test_imports.py
import sys
import os
import traceback

# Add src directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

def test_import_shared_utils():
    """Test that shared_utils imports correctly"""
    print("\n=== Testing shared_utils import ===")
    try:
        from IngestEngine import shared_utils
        print("✅ IngestEngine.shared_utils imported successfully!")
        
        # Check if compute_counts exists
        if hasattr(shared_utils, 'compute_counts'):
            print("✅ compute_counts function exists")
            
            # Test the function
            test_content = """INT. HOUSE - DAY
            
            JOHN sits at a table.
            
            JOHN
            Hello world.
            
            MARY
            Hi John.
            """
            
            counts = shared_utils.compute_counts(test_content)
            print(f"✅ compute_counts works! Results:")
            print(f"   Characters: {counts.get('characters', [])}")
            print(f"   Character count: {counts.get('character_count', 0)}")
            print(f"   Scene count: {counts.get('scene_count', 0)}")
            return True
        else:
            print("❌ compute_counts function NOT found in shared_utils")
            print(f"   Available functions: {[x for x in dir(shared_utils) if not x.startswith('_')]}")
            return False
            
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return False

def test_import_fdx_loader():
    """Test that fdx_loader imports correctly"""
    print("\n=== Testing fdx_loader import ===")
    try:
        from IngestEngine.fdx_loader import load_fdx
        print("✅ fdx_loader.load_fdx imported successfully!")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return False

def test_import_script_ingest():
    """Test that ScriptIngest imports correctly"""
    print("\n=== Testing ScriptIngest import ===")
    try:
        # First check what imports might be failing
        import ScriptIngest
        print("✅ ScriptIngest imported successfully!")
        print(f"   Available attributes: {[x for x in dir(ScriptIngest) if not x.startswith('_')]}")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("\nDebugging ScriptIngest import...")
        
        # Try to see what's in the file
        try:
            script_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'ScriptIngest.py')
            if os.path.exists(script_path):
                with open(script_path, 'r') as f:
                    lines = f.readlines()
                    print(f"   ScriptIngest.py exists ({len(lines)} lines)")
                    # Show first few imports
                    import_lines = [l.strip() for l in lines if l.strip().startswith('from') or l.strip().startswith('import')]
                    print(f"   Import statements: {import_lines[:5]}")
        except:
            pass
            
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return False

def test_import_csv_exporter():
    """Test that CSV exporter imports correctly"""
    print("\n=== Testing CSVExporter import ===")
    try:
        # Try direct import first
        from ExportEngine.csv_exporter import CSVExporter
        print("✅ CSVExporter imported successfully!")
        
        # Test instantiation
        exporter = CSVExporter()
        print("✅ CSVExporter can be instantiated")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        
        # Check if the module file exists
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'src', 'ExportEngine', 'csv_exporter.py')
        if os.path.exists(csv_path):
            print(f"   File exists: {csv_path}")
            # Check for circular imports
            with open(csv_path, 'r') as f:
                content = f.read()
                if 'from ExportEngine' in content or 'from .' in content and 'csv_exporter' in content:
                    print("   ⚠️  Possible circular import detected")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        traceback.print_exc()
        return False

def test_all_imports():
    """Run all import tests"""
    print("=" * 60)
    print("RUNNING IMPORT TESTS")
    print("=" * 60)
    
    results = []
    results.append(test_import_shared_utils())
    results.append(test_import_fdx_loader())
    results.append(test_import_script_ingest())
    results.append(test_import_csv_exporter())
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    success_count = sum(results)
    total_tests = len(results)
    
    print(f"Passed: {success_count}/{total_tests}")
    
    if success_count == total_tests:
        print("✅ ALL IMPORTS WORKING CORRECTLY!")
    else:
        print("❌ SOME IMPORTS FAILED")
        
        # Provide specific fixes based on which tests failed
        if not results[2]:  # ScriptIngest failed
            print("\n📝 To fix ScriptIngest import:")
            print("   Check that ScriptIngest.py doesn't use 'src.' in imports")
            print("   Change 'from src.IngestEngine' to 'from IngestEngine'")
        
        if not results[3]:  # CSVExporter failed  
            print("\n📝 To fix CSVExporter import:")
            print("   Check for circular imports in csv_exporter.py")
            print("   Remove any imports that might create a loop")
    
    return success_count == total_tests

if __name__ == "__main__":
    success = test_all_imports()
    sys.exit(0 if success else 1)
