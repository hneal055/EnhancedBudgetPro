import requests
from typing import Dict, Any
from ..base_adapter import BaseAdapter


class WebhookAdapter(BaseAdapter):
    def validate_config(self) -> bool:
        return 'url' in self.config and self.config['url'].startswith('http')
    
    def test_connection(self) -> bool:
        if not self.validate_config():
            return False
        try:
            response = requests.post(
                self.config['url'],
                json={'event': 'test', 'message': 'Enhanced Budget Pro connection test'},
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
            return response.status_code in [200, 201, 202]
        except Exception:
            return False
    
    def export_data(self, data: Dict[str, Any]) -> bool:
        if not self.is_enabled() or not self.validate_config():
            return False
        
        payload = {
            'event': 'analysis_complete',
            'timestamp': data.get('timestamp'),
            'script_info': {
                'name': data.get('script_name'),
                'format': data.get('format'),
                'scenes': data.get('scene_count'),
                'characters': data.get('character_count')
            },
            'budget': {
                'total': data.get('budget'),
                'currency': 'USD'
            },
            'output_path': data.get('output_path')
        }
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'EnhancedBudgetPro/1.0'
        }
        
        if 'auth_token' in self.config:
            headers['Authorization'] = f"Bearer {self.config['auth_token']}"
        
        try:
            response = requests.post(self.config['url'], json=payload, headers=headers, timeout=30)
            return response.status_code in [200, 201, 202]
        except Exception as e:
            print(f"Webhook delivery failed: {e}")
            return False
