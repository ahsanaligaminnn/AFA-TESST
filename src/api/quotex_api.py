"""
Quotex API wrapper - REAL DATA ONLY
This wrapper ONLY uses real Quotex API - NO SIMULATION.
"""

import asyncio
import time
from typing import Dict, Optional, Any, List
from .quotex_real_api import QuotexRealAPI

class QuotexAPI:
    """
    Quotex API wrapper - REAL DATA ONLY
    NO SIMULATION OR DUMMY DATA ALLOWED.
    """
    
    def __init__(self, use_real_api: bool = True):
        """
        Initialize Quotex API wrapper - REAL ONLY.
        
        Args:
            use_real_api (bool): Must be True - no simulation allowed
        """
        if not use_real_api:
            raise ValueError("❌ SIMULATION NOT ALLOWED - REAL DATA ONLY")
        
        self.real_api = None
        self.connected = False
        self.valid_timeframes = [1, 5, 15, 30, 60]
        
        try:
            self.real_api = QuotexRealAPI()
            print("🔗 Real Quotex API wrapper initialized - LIVE DATA ONLY")
        except Exception as e:
            print(f"❌ Real API initialization failed: {str(e)}")
            raise Exception("❌ Cannot initialize without real API connection")
    
    async def connect(self, email: str = None, password: str = None) -> bool:
        """
        Connect to real Quotex platform - NO SIMULATION.
        
        Args:
            email (str, optional): User email for authentication
            password (str, optional): User password for authentication
            
        Returns:
            bool: True if real connection successful
        """
        if not self.real_api:
            print("❌ No real API available")
            return False
        
        try:
            print("🔗 Connecting to REAL Quotex API...")
            success = await self.real_api.connect(email, password)
            
            if success:
                self.connected = True
                print("✅ Connected to REAL Quotex API successfully")
                return True
            else:
                print("❌ Real API connection failed")
                return False
                
        except Exception as e:
            print(f"❌ Real API connection error: {str(e)}")
            return False
    
    def get_candles(self, asset: str, timeframe: int, count: int = 100) -> Optional[List[Dict]]:
        """
        Get real candle data from Quotex - NO SIMULATION.
        
        Args:
            asset (str): Asset symbol (e.g., 'EURUSD')
            timeframe (int): Timeframe in minutes
            count (int): Number of candles to retrieve
            
        Returns:
            Optional[List[Dict]]: Real candle data from Quotex or None
        """
        if timeframe not in self.valid_timeframes:
            print(f"❌ Invalid timeframe: {timeframe}. Valid: {self.valid_timeframes}")
            return None
        
        if not self.real_api or not self.connected:
            print("❌ Not connected to real Quotex")
            return None
        
        try:
            candles = self.real_api.get_candles(asset, timeframe, count)
            if candles:
                print(f"✅ Retrieved {len(candles)} REAL candles for {asset}")
                return candles
            else:
                print(f"❌ No real candles available for {asset}")
                return None
                
        except Exception as e:
            print(f"❌ Real candles error: {str(e)}")
            return None
    
    def get_signal(self, asset: str, timeframe: int = 1) -> Optional[Dict[str, Any]]:
        """
        Get real trading signal from Quotex - NO SIMULATION.
        
        Args:
            asset (str): Asset symbol (e.g., 'EURUSD')
            timeframe (int): Timeframe in minutes
            
        Returns:
            Optional[Dict[str, Any]]: Real signal data from Quotex or None
        """
        if timeframe not in self.valid_timeframes:
            print(f"❌ Invalid timeframe: {timeframe}. Valid: {self.valid_timeframes}")
            return None
        
        if not self.real_api or not self.connected:
            print("❌ Not connected to real Quotex")
            return None
        
        try:
            signal = self.real_api.get_signal(asset, timeframe)
            if signal:
                print(f"✅ Retrieved REAL signal for {asset}: {signal['direction'].upper()}")
                return signal
            else:
                print(f"❌ No real signal available for {asset}")
                return None
                
        except Exception as e:
            print(f"❌ Real signal error: {str(e)}")
            return None
    
    def get_balance(self) -> Optional[float]:
        """Get real account balance from Quotex."""
        if not self.real_api or not self.connected:
            return None
        
        try:
            balance = self.real_api.get_balance()
            return balance
        except Exception as e:
            print(f"❌ Real balance error: {str(e)}")
            return None
    
    def place_trade(self, asset: str, direction: str, amount: float, timeframe: int) -> Optional[Dict]:
        """Place real trade on Quotex platform."""
        if not self.real_api or not self.connected:
            print("❌ Not connected to real Quotex")
            return None
        
        try:
            result = self.real_api.place_trade(asset, direction, amount, timeframe)
            return result
        except Exception as e:
            print(f"❌ Real trade error: {str(e)}")
            return None
    
    def disconnect(self) -> bool:
        """Disconnect from real Quotex platform."""
        if self.real_api:
            try:
                return self.real_api.disconnect()
            except Exception as e:
                print(f"❌ Real disconnect error: {str(e)}")
        
        self.connected = False
        return True
    
    def get_environment_info(self) -> Dict[str, Any]:
        """Get real environment information."""
        if self.real_api:
            try:
                return self.real_api.get_environment_info()
            except Exception:
                pass
        
        return {
            'api_mode': 'REAL QUOTEX API ONLY',
            'connected': self.connected,
            'simulation_mode': False,
            'valid_timeframes': self.valid_timeframes,
            'source': 'REAL QUOTEX SERVERS ONLY'
        }