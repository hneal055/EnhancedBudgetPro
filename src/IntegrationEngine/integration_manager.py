import json
from typing import Dict, Any, List, Optional
from pathlib import Path

from .adapters.slack_adapter import SlackAdapter
from .adapters.webhook_adapter import WebhookAdapter
from .adapters.sheets_adapter import SheetsAdapter


class IntegrationManager:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or 'integrations.json'
        self.adapters = {}
        self._load_config()
        self._initialize_adapters()
    
    def _load_config(self):
        if Path(self.config_path).exists():
            with open(self.config_path, 'r') as f:
                self.config = json.load(f)
        else:
            self.config = {
                'slack': {'enabled': False},
                'webhook': {'enabled': False},
                'sheets': {'enabled': False}
            }
    
    def _initialize_adapters(self):
        adapter_classes = {
            'slack': SlackAdapter,
            'webhook': WebhookAdapter,
            'sheets': SheetsAdapter
        }
        for name, adapter_class in adapter_classes.items():
            if name in self.config:
                self.adapters[name] = adapter_class(self.config[name])
    
    def export_analysis(self, data: Dict[str, Any]) -> Dict[str, bool]:
        results = {}
        for name, adapter in self.adapters.items():
            if adapter.is_enabled():
                try:
                    success = adapter.export_data(data)
                    results[name] = success
                    status = 'OK' if success else 'FAILED'
                    print(f"{name.capitalize()} export: {status}")
                except Exception as e:
                    print(f"{name.capitalize()} export error: {e}")
                    results[name] = False
        return results
    
    def test_all_connections(self) -> Dict[str, bool]:
        results = {}
        for name, adapter in self.adapters.items():
            if adapter.is_enabled():
                try:
                    connected = adapter.test_connection()
                    results[name] = connected
                    status = 'OK' if connected else 'FAILED'
                    print(f"{name.capitalize()} connection: {status}")
                except Exception as e:
                    print(f"{name.capitalize()} connection error: {e}")
                    results[name] = False
        return results
    
    def get_enabled_integrations(self) -> List[str]:
        return [name for name, adapter in self.adapters.items() if adapter.is_enabled()]
