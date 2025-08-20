"""
Quotex client implementation for managing API sessions and operations.
"""

from typing import Optional, Dict, Any, List
from src.service.api.quotex_api import QuotexAPIService

class QuotexClient:
    _instance = None
    
    def __new__(cls):
        """Implement singleton pattern for QuotexClient."""
        if cls._instance is None:
            cls._instance = super(QuotexClient, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the Quotex client if not already initialized."""
        if not self._initialized:
            self._api_service = QuotexAPIService()
            self._initialized = True
    
    def get_signal(self, market: str, timeframe: int = 1) -> Optional[Dict[str, Any]]:
        """
        Get trading signal for specified market.
        
        Args:
            market (str): Market symbol (e.g., 'EURUSD')
            timeframe (int): Timeframe in minutes (1-15)
            
        Returns:
            Optional[Dict[str, Any]]: Signal data if successful, None otherwise
        """
        return self._api_service.get_market_signal(market, timeframe)
    
    @staticmethod
    def get_valid_timeframes() -> List[int]:
        """
        Get list of valid timeframes.
        
        Returns:
            List[int]: List of valid timeframes in minutes
        """
        return [1, 2, 3, 4, 5, 10, 15]
    
    @classmethod
    def get_instance(cls) -> 'QuotexClient':
        """
        Get singleton instance of QuotexClient.
        
        Returns:
            QuotexClient: Singleton instance
        """
        if cls._instance is None:
            cls._instance = QuotexClient()
        return cls._instance