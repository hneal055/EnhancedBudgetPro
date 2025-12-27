import requests
from typing import Dict, Any
from ..base_adapter import BaseAdapter


class SlackAdapter(BaseAdapter):
    def validate_config(self) -> bool:
        return 'webhook_url' in self.config and self.config['webhook_url'].startswith('https://hooks.slack.com/')
    
    def test_connection(self) -> bool:
        if not self.validate_config():
            return False
        try:
            response = requests.post(
                self.config['webhook_url'],
                json={'text': 'Enhanced Budget Pro connection test'},
                timeout=5
            )
            return response.status_code == 200
        except Exception:
            return False
    
    def export_data(self, data: Dict[str, Any]) -> bool:
        if not self.is_enabled() or not self.validate_config():
            return False
        
        script_name = data.get('script_name', 'Unknown Script')
        budget = data.get('budget', 0)
        scenes = data.get('scene_count', 0)
        characters = data.get('character_count', 0)
        
        payload = {
            'text': f'Budget Analysis Complete: *{script_name}*',
            'attachments': [{
                'color': 'good',
                'fields': [
                    {'title': 'Total Budget', 'value': f'${"$"}budget:,.2f', 'short': True},
                    {'title': 'Scenes', 'value': str(scenes), 'short': True},
                    {'title': 'Characters', 'value': str(characters), 'short': True},
                    {'title': 'Status', 'value': 'Ready for review', 'short': True}
                ]
            }]
        }
        
        try:
            response = requests.post(self.config['webhook_url'], json=payload, timeout=10)
            return response.status_code == 200
        except Exception as e:
            print(f"Slack notification failed: {e}")
            return False
