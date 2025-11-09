"""Unified context manager for all services"""

from typing import Any, Dict, Optional


class BaseContext:
    """Base context class for all service interactions"""
    
    def __init__(self, data: Optional[Dict[str, Any]] = None):
        """
        Initialize context with optional data
        
        Args:
            data: Initial data dictionary
        """
        self.state: Optional[str] = None
        self.data: Dict[str, Any] = data or {}
    
    def set(self, **kwargs) -> None:
        """
        Set multiple attributes at once
        
        Args:
            **kwargs: Key-value pairs to set
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
            if key != 'state':
                self.data[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from data dictionary"""
        return self.data.get(key, default)
    
    def update(self, data: Dict[str, Any]) -> None:
        """Update multiple data values at once"""
        self.data.update(data)
        for key, value in data.items():
            if key != 'state':
                setattr(self, key, value)
    
    def clear(self) -> None:
        """Clear all data"""
        self.data.clear()
        self.state = None


class NewsContext(BaseContext):
    """Context for news service"""
    
    def __init__(self, articles: list = None):
        super().__init__()
        self.articles = articles or []
        self.data['articles'] = self.articles


class AgriculturalContext(BaseContext):
    """Context for agriculture service"""
    pass


class SchemeContext(BaseContext):
    """Context for scheme service"""
    pass
