"""
Service layer for Quotex API operations.
"""

from typing import Dict, Optional, Any
from src.api.quotex_api import QuotexAPI

class QuotexAPIService:
    def __init__(self):
        """Initialize the Quotex API service."""
        self._api = QuotexAPI()
        
    def get_market_signal(self, market: str, timeframe: int = 1) -> Optional[Dict[str, Any]]:
        """
        Get trading signal for a specific market.
        
        Args:
            market (str): Market symbol (e.g., 'EURUSD')
            timeframe (int): Timeframe in minutes (1-15)
            
        Returns:
            Optional[Dict[str, Any]]: Signal data if successful, None otherwise
        """
        try:
            signal = self._api.get_signal(market, timeframe)
            if signal:
                return self._process_signal(signal)
            return None
        except Exception:
            return None
    
    def _process_signal(self, signal: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process and validate the raw signal data.
        
        Args:
            signal (Dict[str, Any]): Raw signal data from API
            
        Returns:
            Dict[str, Any]: Processed signal data
        """
        # Add any additional signal processing logic here
        return signal