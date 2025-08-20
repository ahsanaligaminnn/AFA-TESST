"""
Technical indicators implementation for trading strategy.
"""

import numpy as np
from typing import List, Tuple

def calculate_ema(prices: List[float], period: int) -> List[float]:
    """Calculate Exponential Moving Average."""
    prices = np.array(prices)
    alpha = 2 / (period + 1)
    ema = [prices[0]]  # First value is price
    
    for price in prices[1:]:
        ema.append(price * alpha + ema[-1] * (1 - alpha))
    
    return ema

def calculate_macd(prices: List[float], fast_period: int = 9, 
                  slow_period: int = 20, signal_period: int = 3) -> Tuple[List[float], List[float]]:
    """Calculate MACD and Signal line."""
    fast_ema = calculate_ema(prices, fast_period)
    slow_ema = calculate_ema(prices, slow_period)
    
    macd_line = [f - s for f, s in zip(fast_ema, slow_ema)]
    signal_line = calculate_ema(macd_line, signal_period)
    
    return macd_line, signal_line

def calculate_rsi(prices: List[float], period: int = 7) -> List[float]:
    """Calculate Relative Strength Index."""
    deltas = np.diff(prices)
    gains = [d if d > 0 else 0 for d in deltas]
    losses = [-d if d < 0 else 0 for d in deltas]
    
    avg_gain = np.mean(gains[:period])
    avg_loss = np.mean(losses[:period])
    
    if avg_loss == 0:
        return [100.0]
    
    rs = avg_gain / avg_loss
    rsi = [100 - (100 / (1 + rs))]
    
    for i in range(period, len(prices) - 1):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        if avg_loss == 0:
            rsi.append(100.0)
        else:
            rs = avg_gain / avg_loss
            rsi.append(100 - (100 / (1 + rs)))
    
    return rsi

def calculate_bollinger_bands(prices: List[float], period: int = 20, 
                            std_dev: float = 2.0) -> Tuple[List[float], List[float], List[float]]:
    """Calculate Bollinger Bands."""
    prices = np.array(prices)
    sma = [np.mean(prices[max(0, i-period+1):i+1]) for i in range(len(prices))]
    std = [np.std(prices[max(0, i-period+1):i+1]) for i in range(len(prices))]
    
    upper_band = [sma[i] + std_dev * std[i] for i in range(len(prices))]
    lower_band = [sma[i] - std_dev * std[i] for i in range(len(prices))]
    
    return upper_band, sma, lower_band

def calculate_atr(high: List[float], low: List[float], 
                 close: List[float], period: int = 14) -> List[float]:
    """Calculate Average True Range."""
    tr = []
    for i in range(len(close)):
        if i == 0:
            tr.append(high[i] - low[i])
        else:
            tr.append(max([
                high[i] - low[i],
                abs(high[i] - close[i-1]),
                abs(low[i] - close[i-1])
            ]))
    
    atr = [tr[0]]
    for i in range(1, len(tr)):
        atr.append((atr[-1] * (period - 1) + tr[i]) / period)
    
    return atr