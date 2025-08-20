"""
Advanced Volatility Filter implementation with dynamic position sizing.
"""

import numpy as np
import time
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta

class VolatilityFilter:
    def __init__(self):
        """Initialize the Volatility Filter with default settings."""
        self.enabled = False
        self.atr_period = 14
        self.bb_period = 20
        self.bb_std_dev = 2.0
        self.historical_vol_period = 20
        self.trend_filter_period = 50
        
        # Thresholds
        self.high_vol_atr_threshold = 1.2
        self.high_vol_bb_threshold = 1.1
        self.low_vol_atr_threshold = 0.8
        self.low_vol_bb_threshold = 0.9
        
        # Risk management
        self.base_position_size = 1.0
        self.min_position_size = 0.5
        self.max_position_size = 2.0
        self.cooldown_periods = 3
        self.outlier_multiplier = 3.0
        
        # State tracking
        self.volatility_history = []
        self.cooldown_counter = 0
        self.last_analysis_time = None
        
    def enable_filter(self, **kwargs):
        """
        Enable volatility filtering with optional parameter overrides.
        
        Args:
            **kwargs: Optional parameter overrides
        """
        self.enabled = True
        
        # Update parameters if provided
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
    
    def disable_filter(self):
        """Disable volatility filtering."""
        self.enabled = False
    
    def calculate_atr(self, highs: List[float], lows: List[float], 
                     closes: List[float]) -> float:
        """
        Calculate Average True Range.
        
        Args:
            highs (List[float]): High prices
            lows (List[float]): Low prices
            closes (List[float]): Close prices
            
        Returns:
            float: ATR value
        """
        if len(highs) < 2:
            return 0.0
        
        true_ranges = []
        for i in range(1, len(highs)):
            tr = max([
                highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1])
            ])
            true_ranges.append(tr)
        
        # Calculate ATR using exponential moving average
        if len(true_ranges) < self.atr_period:
            return np.mean(true_ranges)
        
        atr = true_ranges[0]
        alpha = 2.0 / (self.atr_period + 1)
        
        for tr in true_ranges[1:]:
            atr = alpha * tr + (1 - alpha) * atr
        
        return atr
    
    def calculate_bollinger_bands(self, prices: List[float]) -> Tuple[float, float, float]:
        """
        Calculate Bollinger Bands.
        
        Args:
            prices (List[float]): Price data
            
        Returns:
            Tuple[float, float, float]: (upper_band, middle_band, lower_band)
        """
        if len(prices) < self.bb_period:
            return 0.0, 0.0, 0.0
        
        recent_prices = prices[-self.bb_period:]
        sma = np.mean(recent_prices)
        std = np.std(recent_prices)
        
        upper_band = sma + (self.bb_std_dev * std)
        lower_band = sma - (self.bb_std_dev * std)
        
        return upper_band, sma, lower_band
    
    def calculate_historical_volatility(self, prices: List[float]) -> float:
        """
        Calculate historical volatility using log returns.
        
        Args:
            prices (List[float]): Price data
            
        Returns:
            float: Historical volatility
        """
        if len(prices) < self.historical_vol_period + 1:
            return 0.0
        
        recent_prices = prices[-self.historical_vol_period-1:]
        log_returns = []
        
        for i in range(1, len(recent_prices)):
            if recent_prices[i-1] > 0:
                log_return = np.log(recent_prices[i] / recent_prices[i-1])
                log_returns.append(log_return)
        
        return np.std(log_returns) if log_returns else 0.0
    
    def calculate_sma(self, prices: List[float], period: int) -> float:
        """Calculate Simple Moving Average."""
        if len(prices) < period:
            return np.mean(prices) if prices else 0.0
        
        return np.mean(prices[-period:])
    
    def normalize_metrics(self, current_atr: float, current_bb_width: float,
                         atr_history: List[float], bb_history: List[float]) -> Tuple[float, float]:
        """
        Normalize volatility metrics against their rolling means.
        
        Args:
            current_atr (float): Current ATR value
            current_bb_width (float): Current BB width
            atr_history (List[float]): Historical ATR values
            bb_history (List[float]): Historical BB width values
            
        Returns:
            Tuple[float, float]: (normalized_atr, normalized_bb)
        """
        # Calculate rolling means
        atr_mean = np.mean(atr_history) if atr_history else current_atr
        bb_mean = np.mean(bb_history) if bb_history else current_bb_width
        
        # Avoid division by zero
        norm_atr = current_atr / atr_mean if atr_mean > 0 else 1.0
        norm_bb = current_bb_width / bb_mean if bb_mean > 0 else 1.0
        
        return norm_atr, norm_bb
    
    def detect_trend_regime(self, prices: List[float], current_price: float) -> str:
        """
        Detect current trend regime using SMA.
        
        Args:
            prices (List[float]): Historical prices
            current_price (float): Current price
            
        Returns:
            str: 'bullish', 'bearish', or 'neutral'
        """
        if len(prices) < self.trend_filter_period:
            return 'neutral'
        
        sma = self.calculate_sma(prices, self.trend_filter_period)
        
        if current_price > sma * 1.001:  # 0.1% buffer
            return 'bullish'
        elif current_price < sma * 0.999:
            return 'bearish'
        else:
            return 'neutral'
    
    def detect_outlier_volatility(self, current_atr: float, atr_history: List[float]) -> bool:
        """
        Detect outlier volatility spikes.
        
        Args:
            current_atr (float): Current ATR value
            atr_history (List[float]): Historical ATR values
            
        Returns:
            bool: True if outlier detected
        """
        if len(atr_history) < 5:
            return False
        
        avg_atr = np.mean(atr_history[-5:])
        return current_atr > (avg_atr * self.outlier_multiplier)
    
    def calculate_dynamic_position_size(self, volatility_metric: float) -> float:
        """
        Calculate dynamic position size based on volatility.
        
        Args:
            volatility_metric (float): Normalized volatility metric
            
        Returns:
            float: Position size multiplier
        """
        # Inverse relationship: higher volatility = smaller position
        if volatility_metric <= 0:
            return self.base_position_size
        
        size = self.base_position_size * (1.0 / volatility_metric)
        
        # Apply caps
        return max(self.min_position_size, min(self.max_position_size, size))
    
    def analyze_market_volatility(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive volatility analysis of market data.
        
        Args:
            market_data (Dict[str, Any]): Market data with OHLC
            
        Returns:
            Dict[str, Any]: Volatility analysis results
        """
        try:
            highs = market_data.get('highs', [])
            lows = market_data.get('lows', [])
            closes = market_data.get('closes', [])
            
            if len(closes) < 10:
                return {'error': 'Insufficient data for volatility analysis'}
            
            current_price = closes[-1]
            
            # Calculate volatility metrics
            current_atr = self.calculate_atr(highs, lows, closes)
            upper_band, middle_band, lower_band = self.calculate_bollinger_bands(closes)
            current_bb_width = upper_band - lower_band
            historical_vol = self.calculate_historical_volatility(closes)
            
            # Build history for normalization
            atr_history = []
            for i in range(max(10, len(closes)-20), len(closes)):
                start_idx = max(0, i-self.atr_period)
                end_idx = i+1
                if end_idx > start_idx:
                    atr_val = self.calculate_atr(highs[start_idx:end_idx], 
                                               lows[start_idx:end_idx],
                                               closes[start_idx:end_idx])
                    atr_history.append(atr_val)
            
            bb_history = []
            for i in range(max(10, len(closes)-20), len(closes)):
                start_idx = max(0, i-self.bb_period)
                end_idx = i+1
                if end_idx > start_idx:
                    ub, mb, lb = self.calculate_bollinger_bands(closes[start_idx:end_idx])
                    bb_history.append(ub - lb)
            
            # Normalize metrics
            norm_atr, norm_bb = self.normalize_metrics(current_atr, current_bb_width,
                                                     atr_history, bb_history)
            
            # Detect trend regime
            trend_regime = self.detect_trend_regime(closes, current_price)
            
            # Detect outliers
            is_outlier = self.detect_outlier_volatility(current_atr, atr_history)
            
            # Determine volatility state
            volatility_state = 'neutral'
            if (norm_atr >= self.high_vol_atr_threshold or 
                norm_bb >= self.high_vol_bb_threshold):
                volatility_state = 'high'
            elif (norm_atr <= self.low_vol_atr_threshold and 
                  norm_bb <= self.low_vol_bb_threshold):
                volatility_state = 'low'
            
            # Calculate position size
            avg_volatility = (norm_atr + norm_bb) / 2
            position_size_multiplier = self.calculate_dynamic_position_size(avg_volatility)
            
            return {
                'current_atr': current_atr,
                'normalized_atr': norm_atr,
                'bb_width': current_bb_width,
                'normalized_bb': norm_bb,
                'historical_volatility': historical_vol,
                'volatility_state': volatility_state,
                'trend_regime': trend_regime,
                'is_outlier': is_outlier,
                'position_size_multiplier': position_size_multiplier,
                'analysis_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {'error': f'Volatility analysis failed: {str(e)}'}
    
    def filter_signal(self, signal: Dict[str, Any], market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply volatility filter to a trading signal.
        
        Args:
            signal (Dict[str, Any]): Original trading signal
            market_data (Dict[str, Any]): Market data for analysis
            
        Returns:
            Dict[str, Any]: Filtered signal with volatility analysis
        """
        if not self.enabled:
            signal['volatility_filter'] = {
                'status': 'disabled',
                'volatility_state': 'unknown',
                'filter_result': 'passed'
            }
            return signal
        
        # Check cooldown
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1
            signal['volatility_filter'] = {
                'status': 'cooldown',
                'cooldown_remaining': self.cooldown_counter,
                'filter_result': 'blocked'
            }
            signal['strength'] = 'blocked'
            return signal
        
        # Analyze volatility
        vol_analysis = self.analyze_market_volatility(market_data)
        
        if 'error' in vol_analysis:
            signal['volatility_filter'] = {
                'status': 'error',
                'error': vol_analysis['error'],
                'filter_result': 'passed'
            }
            return signal
        
        # Apply filtering logic
        filter_result = 'passed'
        volatility_state = vol_analysis['volatility_state']
        is_outlier = vol_analysis['is_outlier']
        trend_regime = vol_analysis['trend_regime']
        
        # Handle outlier volatility
        if is_outlier:
            self.cooldown_counter = self.cooldown_periods
            filter_result = 'outlier_detected'
            signal['strength'] = 'blocked'
        
        # High volatility filtering
        elif volatility_state == 'high':
            signal_type = signal.get('signal_type', '').upper()
            
            # Drop high-risk signals in high volatility
            if signal_type in ['BUY', 'SELL'] and signal.get('strength') in ['HIGH', 'STRONG']:
                filter_result = 'high_volatility_risk'
                signal['strength'] = 'weak'
            else:
                filter_result = 'high_volatility_adjusted'
        
        # Low volatility enhancement
        elif volatility_state == 'low':
            # Enhance mean-reversion strategies in low volatility
            if signal.get('strategy_type') == 'reversal':
                filter_result = 'low_volatility_enhanced'
                if signal.get('strength') == 'MEDIUM':
                    signal['strength'] = 'HIGH'
        
        # Apply dynamic position sizing
        position_multiplier = vol_analysis['position_size_multiplier']
        signal['position_size_multiplier'] = position_multiplier
        
        # Add volatility filter information
        signal['volatility_filter'] = {
            'status': 'active',
            'volatility_state': volatility_state,
            'trend_regime': trend_regime,
            'filter_result': filter_result,
            'is_outlier': is_outlier,
            'atr_normalized': vol_analysis['normalized_atr'],
            'bb_normalized': vol_analysis['normalized_bb'],
            'position_size_multiplier': position_multiplier
        }
        
        return signal
    
    def get_filter_stats(self) -> Dict[str, Any]:
        """
        Get volatility filter statistics and settings.
        
        Returns:
            Dict[str, Any]: Filter statistics
        """
        return {
            'enabled': self.enabled,
            'atr_period': self.atr_period,
            'bb_period': self.bb_period,
            'high_vol_thresholds': {
                'atr': self.high_vol_atr_threshold,
                'bb': self.high_vol_bb_threshold
            },
            'low_vol_thresholds': {
                'atr': self.low_vol_atr_threshold,
                'bb': self.low_vol_bb_threshold
            },
            'position_sizing': {
                'base_size': self.base_position_size,
                'min_size': self.min_position_size,
                'max_size': self.max_position_size
            },
            'cooldown_periods': self.cooldown_periods,
            'current_cooldown': self.cooldown_counter,
            'outlier_multiplier': self.outlier_multiplier
        }
    
    def update_settings(self, settings: Dict[str, Any]):
        """
        Update filter settings.
        
        Args:
            settings (Dict[str, Any]): New settings to apply
        """
        for key, value in settings.items():
            if hasattr(self, key) and isinstance(value, (int, float, bool)):
                setattr(self, key, value)