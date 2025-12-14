from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseAdapter(ABC):
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.enabled = self.config.get('enabled', False)
    
    @abstractmethod
    def validate_config(self) -> bool:
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        pass
    
    @abstractmethod
    def export_data(self, data: Dict[str, Any]) -> bool:
        pass
    
    def is_enabled(self) -> bool:
        return self.enabled
