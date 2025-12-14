# Complete Integration Test
# Tests IntegrationManager with mock data

from src.IntegrationEngine import IntegrationManager
from datetime import datetime
from pathlib import Path

print("=" * 60)
print("Enhanced Budget Pro - Integration Test")
print("=" * 60)

# Check if config exists
config_path = Path('integrations.json')
if not config_path.exists():
    print("\nNo integrations.json found.")
    print("This is normal for first run.")
    print("\nTo enable integrations:")
    print("  1. cp integrations.json.sample integrations.json")
    print("  2. Edit integrations.json with your webhook URLs")
    print("  3. Run this test again")
    print("\nExample Slack setup:")
    print("  - Visit: https://api.slack.com/apps")
    print("  - Create app with Incoming Webhooks")
    print("  - Copy webhook URL")
    print("  - Add to integrations.json")
    exit(0)

# Initialize manager
print("\nInitializing IntegrationManager...")
manager = IntegrationManager(str(config_path))

# Check enabled integrations
enabled = manager.get_enabled_integrations()
print(f"Enabled integrations: {', '.join(enabled) if enabled else 'None'}")

if not enabled:
    print("\nNo integrations enabled in integrations.json")
    print("Set 'enabled': true for desired integrations")
    exit(0)

# Test connections
print("\nTesting connections...")
results = manager.test_all_connections()

# Show results
print("\nConnection Results:")
for name, success in results.items():
    status = "PASS" if success else "FAIL"
    symbol = "[OK]" if success else "[X]"
    print(f"  {symbol} {name}: {status}")

# Test data export with sample analysis
if any(results.values()):
    print("\nTesting data export with sample analysis...")
    sample_data = {
        'script_name': 'test_script.fdx',
        'format': '.fdx',
        'scene_count': 12,
        'character_count': 8,
        'budget': 111215.00,
        'output_path': './output',
        'timestamp': datetime.now().isoformat(),
        'risk_summary': {'high': 2, 'medium': 4, 'low': 6}
    }
    
    export_results = manager.export_analysis(sample_data)
    
    print("\nExport Results:")
    for name, success in export_results.items():
        status = "SUCCESS" if success else "FAILED"
        symbol = "[OK]" if success else "[X]"
        print(f"  {symbol} {name}: {status}")

print("\n" + "=" * 60)
print("Integration test complete!")
print("=" * 60)
