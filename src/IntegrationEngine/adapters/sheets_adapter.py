from typing import Dict, Any, Optional
from ..base_adapter import BaseAdapter

try:
    from google.oauth2.service_account import Credentials as ServiceAccountCredentials
    from googleapiclient.discovery import build
    GOOGLE_AVAILABLE = True
except ImportError:
    GOOGLE_AVAILABLE = False


class SheetsAdapter(BaseAdapter):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.service = None
        if not GOOGLE_AVAILABLE:
            print("Warning: google-api-python-client not installed")
    
    def validate_config(self) -> bool:
        if not GOOGLE_AVAILABLE:
            return False
        return 'spreadsheet_id' in self.config and 'service_account_file' in self.config
    
    def test_connection(self) -> bool:
        if not self.validate_config():
            return False
        try:
            self._authenticate()
            self.service.spreadsheets().get(spreadsheetId=self.config['spreadsheet_id']).execute()
            return True
        except Exception:
            return False
    
    def _authenticate(self):
        if self.service:
            return
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        creds = ServiceAccountCredentials.from_service_account_file(
            self.config['service_account_file'], scopes=scopes
        )
        self.service = build('sheets', 'v4', credentials=creds)
    
    def export_data(self, data: Dict[str, Any]) -> bool:
        if not self.is_enabled() or not self.validate_config():
            return False
        try:
            self._authenticate()
            values = [
                ['Metric', 'Value'],
                ['Script Name', data.get('script_name', '')],
                ['Total Budget', data.get('budget', 0)],
                ['Scenes', data.get('scene_count', 0)],
                ['Characters', data.get('character_count', 0)]
            ]
            self.service.spreadsheets().values().update(
                spreadsheetId=self.config['spreadsheet_id'],
                range='Summary!A1',
                valueInputOption='RAW',
                body={'values': values}
            ).execute()
            return True
        except Exception as e:
            print(f"Google Sheets export failed: {e}")
            return False
