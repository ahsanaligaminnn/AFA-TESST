"""
Trading strategy implementation combining multiple analysis modules.
"""

from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from .indicators import (
    calculate_ema, calculate_macd, calculate_rsi,
    calculate_bollinger_bands, calculate_atr
)

class TradingStrategy:
    def __init__(self, timeframe: int = 1):
        """
        Initialize trading strategy.
        
        Args:
            timeframe (int): Trading timeframe in minutes (1, 5, or 15)
        """
        self.timeframe = timeframe
        self.last_signal_time = None
        
    def analyze_trend(self, prices: List[float], volumes: List[float]) -> str:
        """
        Analyze trend using EMA crossover and MACD.
        
        Returns:
            str: 'BUY', 'SELL', or 'NONE'
        """
        # Calculate indicators
        ema_fast = calculate_ema(prices, 5)
        ema_slow = calculate_ema(prices, 21)
        macd_line, signal_line = calculate_macd(prices)
        rsi = calculate_rsi(prices, 7)
        
        # Check last two values for crossover
        if (ema_fast[-2] <= ema_slow[-2] and ema_fast[-1] > ema_slow[-1] and
            macd_line[-1] > signal_line[-1] and rsi[-1] > 50):
            return 'BUY'
        elif (ema_fast[-2] >= ema_slow[-2] and ema_fast[-1] < ema_slow[-1] and
              macd_line[-1] < signal_line[-1] and rsi[-1] < 50):
            return 'SELL'
        
        return 'NONE'
    
    def analyze_reversal(self, prices: List[float], highs: List[float], 
                        lows: List[float]) -> str:
        """
        Analyze potential reversals using RSI and price action.
        
        Returns:
            str: 'BUY', 'SELL', or 'NONE'
        """
        rsi = calculate_rsi(prices, 5)
        
        # Check for oversold/overbought conditions
        if rsi[-1] < 30 and prices[-1] > prices[-2]:  # Bullish reversal
            return 'BUY'
        elif rsi[-1] > 70 and prices[-1] < prices[-2]:  # Bearish reversal
            return 'SELL'
        
        return 'NONE'
    
    def analyze_volatility(self, prices: List[float], highs: List[float], 
                         lows: List[float]) -> str:
        """
        Analyze volatility breakouts using Bollinger Bands and ATR.
        
        Returns:
            str: 'BUY', 'SELL', or 'NONE'
        """
        upper_band, sma, lower_band = calculate_bollinger_bands(prices)
        atr = calculate_atr(highs, lows, prices)
        
        # Calculate ATR ratio
        atr_ratio = atr[-1] / atr[-5] if len(atr) >= 5 else 1.0
        
        # Check for breakouts with increased volatility
        if atr_ratio >= 1.2:  # Volatility spike
            if prices[-1] > upper_band[-1]:
                return 'BUY'
            elif prices[-1] < lower_band[-1]:
                return 'SELL'
        
        return 'NONE'
    
    def check_news_filter(self, market: str) -> bool:
        """
        Check if trading should be allowed based on news events.
        
        Returns:
            bool: True if trading is allowed, False if blocked
        """
        # TODO: Implement news filter logic
        return True
    
    def generate_signal(self, market_data: Dict) -> Optional[Dict]:
        """
        Generate trading signal based on all analysis modules.
        
        Args:
            market_data: Dictionary containing OHLCV data
            
        Returns:
            Optional[Dict]: Signal details if generated, None otherwise
        """
        if not self.check_news_filter(market_data['market']):
            return None
            
        prices = market_data['closes']
        highs = market_data['highs']
        lows = market_data['lows']
        volumes = market_data['volumes']
        
        # Get signals from each module
        trend_signal = self.analyze_trend(prices, volumes)
        reversal_signal = self.analyze_reversal(prices, highs, lows)
        volatility_signal = self.analyze_volatility(prices, highs, lows)
        
        # Count signals
        buy_signals = sum(1 for s in [trend_signal, reversal_signal, volatility_signal] 
                         if s == 'BUY')
        sell_signals = sum(1 for s in [trend_signal, reversal_signal, volatility_signal] 
                          if s == 'SELL')
        
        # Generate final signal if at least two modules agree
        if buy_signals >= 2:
            return {
                'market': market_data['market'],
                'signal_type': 'BUY',
                'timeframe': self.timeframe,
                'time': datetime.now()
            }
        elif sell_signals >= 2:
            return {
                'market': market_data['market'],
                'signal_type': 'SELL',
                'timeframe': self.timeframe,
                'time': datetime.now()
            }
        
        return None