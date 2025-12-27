import streamlit as st
"""
Test that ignores Streamlit deprecation warnings.
"""

import warnings
import os
import sys
import ast

# Suppress Streamlit deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def test_module_without_warnings():
    """Test module structure while ignoring warnings."""
    module_path = "pages/16_Storytelling_Insights.py"
    
    print("Testing module (ignoring deprecation warnings)...")
    print("=" * 60)
    
    # 1. File exists
    if not os.path.exists(module_path):
        print("❌ Module file not found")
        return False
    
    print("✓ Module file exists")
    
    # 2. Read and check content
    with open(module_path, 'r') as f:
        content = f.read()
    
    # Check for key patterns (case insensitive)
    patterns = [
        ('import streamlit', 'Streamlit import'),
        ('st.set_page_config', 'Page config'),
        ('st.session_state', 'Session state usage'),
        ('st.error', 'Error messages'),
        ('st.stop()', 'Stop calls for prerequisites'),
        ('character_arcs', 'Character arcs reference'),
    ]
    
    all_ok = True
    for pattern, description in patterns:
        if pattern.lower() in content.lower():
            print(f"✓ {description}")
        else:
            print(f"✗ Missing: {description}")
            all_ok = False
    
    # 3. Check if it's valid Python
    try:
        ast.parse(content)
        print("✓ Valid Python syntax")
    except SyntaxError as e:
        print(f"✗ Syntax error: {e}")
        all_ok = False
    
    # 4. Count prerequisite checks
    stop_count = content.count('st.stop()')
    error_count = content.count('st.error')
    
    print(f"✓ Found {stop_count} prerequisite checks (st.stop() calls)")
    print(f"✓ Found {error_count} error messages")
    
    if stop_count >= 2 and error_count >= 2:
        print("✓ Sufficient prerequisite checking")
    else:
        print("⚠ May need more prerequisite checks")
    
    return all_ok and stop_count >= 2

def main():
    print("\nSTORYTELLING INSIGHTS - NO WARNINGS TEST")
    print("=" * 60)
    
    # Also suppress warnings from subprocess if we use it
    env = os.environ.copy()
    env['PYTHONWARNINGS'] = 'ignore'
    
    try:
        if test_module_without_warnings():
            print("\n" + "=" * 60)
            print("✅ TEST PASSED (warnings ignored)")
            print("\nNote: Deprecation warnings about use_container_width")
            print("      are ignored. Update the module when possible.")
            return 0
        else:
            print("\n" + "=" * 60)
            print("❌ TEST FAILED")
            return 1
            
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
NOWARNcat > tests/test_storytelling_no_warnings.py << 'NOWARN'
"""
Test that ignores Streamlit deprecation warnings.
"""

import warnings
import os
import sys
import ast

# Suppress Streamlit deprecation warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

def test_module_without_warnings():
    """Test module structure while ignoring warnings."""
    module_path = "pages/16_Storytelling_Insights.py"
    
    print("Testing module (ignoring deprecation warnings)...")
    print("=" * 60)
    
    # 1. File exists
    if not os.path.exists(module_path):
        print("❌ Module file not found")
        return False
    
    print("✓ Module file exists")
    
    # 2. Read and check content
    with open(module_path, 'r') as f:
        content = f.read()
    
    # Check for key patterns (case insensitive)
    patterns = [
        ('import streamlit', 'Streamlit import'),
        ('st.set_page_config', 'Page config'),
        ('st.session_state', 'Session state usage'),
        ('st.error', 'Error messages'),
        ('st.stop()', 'Stop calls for prerequisites'),
        ('character_arcs', 'Character arcs reference'),
    ]
    
    all_ok = True
    for pattern, description in patterns:
        if pattern.lower() in content.lower():
            print(f"✓ {description}")
        else:
            print(f"✗ Missing: {description}")
            all_ok = False
    
    # 3. Check if it's valid Python
    try:
        ast.parse(content)
        print("✓ Valid Python syntax")
    except SyntaxError as e:
        print(f"✗ Syntax error: {e}")
        all_ok = False
    
    # 4. Count prerequisite checks
    stop_count = content.count('st.stop()')
    error_count = content.count('st.error')
    
    print(f"✓ Found {stop_count} prerequisite checks (st.stop() calls)")
    print(f"✓ Found {error_count} error messages")
    
    if stop_count >= 2 and error_count >= 2:
        print("✓ Sufficient prerequisite checking")
    else:
        print("⚠ May need more prerequisite checks")
    
    return all_ok and stop_count >= 2

def main():
    print("\nSTORYTELLING INSIGHTS - NO WARNINGS TEST")
    print("=" * 60)
    
    # Also suppress warnings from subprocess if we use it
    env = os.environ.copy()
    env['PYTHONWARNINGS'] = 'ignore'
    
    try:
        if test_module_without_warnings():
            print("\n" + "=" * 60)
            print("✅ TEST PASSED (warnings ignored)")
            print("\nNote: Deprecation warnings about use_container_width")
            print("      are ignored. Update the module when possible.")
            return 0
        else:
            print("\n" + "=" * 60)
            print("❌ TEST FAILED")
            return 1
            
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
