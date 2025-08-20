"""
Enhanced Market data models with categorized selection and improved data handling.
"""

import random
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta

# Categorized markets dictionary
FOREX_MARKETS = {
    "EURUSD": {"description": "Euro vs US Dollar", "volatility": "medium", "category": "forex"},
    "GBPUSD": {"description": "British Pound vs US Dollar", "volatility": "medium", "category": "forex"},
    "AUDUSD": {"description": "Australian Dollar vs US Dollar", "volatility": "medium", "category": "forex"},
    "EURGBP": {"description": "Euro vs British Pound", "volatility": "low", "category": "forex"},
    "EURJPY": {"description": "Euro vs Japanese Yen", "volatility": "high", "category": "forex"},
    "AUDJPY": {"description": "Australian Dollar vs Japanese Yen", "volatility": "high", "category": "forex"},
    "USDJPY": {"description": "US Dollar vs Japanese Yen", "volatility": "medium", "category": "forex"},
    "USDCAD": {"description": "US Dollar vs Canadian Dollar", "volatility": "medium", "category": "forex"},
    "GBPCAD": {"description": "British Pound vs Canadian Dollar", "volatility": "medium", "category": "forex"},
    "GBPJPY": {"description": "British Pound vs Japanese Yen", "volatility": "high", "category": "forex"},
    "AUDCAD": {"description": "Australian Dollar vs Canadian Dollar", "volatility": "medium", "category": "forex"},
}

OTC_MARKETS = {
    "USDPKR-OTC": {"description": "US Dollar vs Pakistani Rupee OTC", "volatility": "high", "category": "otc"},
    "USDINR-OTC": {"description": "US Dollar vs Indian Rupee OTC", "volatility": "high", "category": "otc"},
    "USDBRL-OTC": {"description": "US Dollar vs Brazilian Real OTC", "volatility": "high", "category": "otc"},
    "USDZAR-OTC": {"description": "US Dollar vs South African Rand OTC", "volatility": "high", "category": "otc"},
    "EURUSD-OTC": {"description": "Euro vs US Dollar OTC", "volatility": "medium", "category": "otc"},
    "USDBDT-OTC": {"description": "US Dollar vs Bangladeshi Taka OTC", "volatility": "high", "category": "otc"},
    "EURJPY-OTC": {"description": "Euro vs Japanese Yen OTC", "volatility": "high", "category": "otc"},
    "GBPUSD-OTC": {"description": "British Pound vs US Dollar OTC", "volatility": "medium", "category": "otc"},
    "EURGBP-OTC": {"description": "Euro vs British Pound OTC", "volatility": "low", "category": "otc"},
    "USDTRY-OTC": {"description": "US Dollar vs Turkish Lira OTC", "volatility": "very high", "category": "otc"},
    "NZDCAD-OTC": {"description": "New Zealand Dollar vs Canadian Dollar OTC", "volatility": "medium", "category": "otc"},
    "USDMXN-OTC": {"description": "US Dollar vs Mexican Peso OTC", "volatility": "high", "category": "otc"},
    "USDNGN-OTC": {"description": "US Dollar vs Nigerian Naira OTC", "volatility": "high", "category": "otc"},
    "USDCOP-OTC": {"description": "US Dollar vs Colombian Peso OTC", "volatility": "high", "category": "otc"},
}

# Combined markets for backward compatibility
MARKETS = {**FOREX_MARKETS, **OTC_MARKETS}

class MarketSelector:
    """Enhanced market selection with categorization and random selection."""
    
    def __init__(self, default_random_count: int = 3):
        """
        Initialize market selector.
        
        Args:
            default_random_count (int): Default number of markets to select in "All" mode
        """
        self.default_random_count = default_random_count
        self.min_random_count = 1
        self.max_random_count = 5
        
    def get_market_categories(self) -> Dict[str, str]:
        """Get available market categories."""
        return {
            "1": "Forex",
            "2": "OTC"
        }
    
    def get_forex_markets(self) -> Dict[str, Dict]:
        """Get all Forex markets."""
        return FOREX_MARKETS
    
    def get_otc_markets(self) -> Dict[str, Dict]:
        """Get all OTC markets."""
        return OTC_MARKETS
    
    def select_random_markets(self, market_dict: Dict[str, Dict], count: Optional[int] = None) -> List[str]:
        """
        Randomly select markets from given dictionary.
        
        Args:
            market_dict (Dict[str, Dict]): Dictionary of markets to select from
            count (Optional[int]): Number of markets to select, defaults to default_random_count
            
        Returns:
            List[str]: List of selected market symbols
        """
        if count is None:
            count = self.default_random_count
        
        # Ensure count is within bounds
        count = max(self.min_random_count, min(count, len(market_dict), self.max_random_count))
        
        # Randomly select markets
        market_symbols = list(market_dict.keys())
        selected = random.sample(market_symbols, count)
        
        return selected
    
    def validate_choice(self, choice: str, max_options: int) -> Optional[int]:
        """
        Validate user choice input.
        
        Args:
            choice (str): User input
            max_options (int): Maximum valid option number
            
        Returns:
            Optional[int]: Validated choice number or None if invalid
        """
        try:
            choice_num = int(choice.strip())
            if 1 <= choice_num <= max_options:
                return choice_num
            return None
        except ValueError:
            return None

class TimingController:
    """Real-time signal timing control with gap enforcement."""
    
    def __init__(self, min_gap_minutes: int = 3, max_gap_minutes: int = 15):
        """
        Initialize timing controller.
        
        Args:
            min_gap_minutes (int): Minimum gap between signals
            max_gap_minutes (int): Maximum gap before forced signal
        """
        self.enabled = True
        self.min_gap_minutes = min_gap_minutes
        self.max_gap_minutes = max_gap_minutes
        self.last_signal_time = None
        self.next_allowed_time = None
        self.forced_signal_timer = None
        
    def can_emit_signal(self) -> bool:
        """
        Check if a signal can be emitted now.
        
        Returns:
            bool: True if signal can be emitted
        """
        if not self.enabled:
            return True
            
        current_time = datetime.now()
        
        if self.last_signal_time is None:
            return True
            
        elapsed = (current_time - self.last_signal_time).total_seconds() / 60
        return elapsed >= self.min_gap_minutes
    
    def get_next_allowed_time(self) -> Optional[datetime]:
        """
        Get the next time a signal can be emitted.
        
        Returns:
            Optional[datetime]: Next allowed emission time
        """
        if not self.enabled or self.last_signal_time is None:
            return None
            
        return self.last_signal_time + timedelta(minutes=self.min_gap_minutes)
    
    def get_time_until_next_signal(self) -> Optional[int]:
        """
        Get seconds until next signal can be emitted.
        
        Returns:
            Optional[int]: Seconds until next signal, None if can emit now
        """
        next_time = self.get_next_allowed_time()
        if next_time is None:
            return None
            
        current_time = datetime.now()
        if current_time >= next_time:
            return None
            
        return int((next_time - current_time).total_seconds())
    
    def should_force_signal(self) -> bool:
        """
        Check if a signal should be forced due to max gap.
        
        Returns:
            bool: True if signal should be forced
        """
        if not self.enabled or self.last_signal_time is None:
            return False
            
        current_time = datetime.now()
        elapsed = (current_time - self.last_signal_time).total_seconds() / 60
        return elapsed >= self.max_gap_minutes
    
    def record_signal_emission(self, forced: bool = False) -> Dict[str, Any]:
        """
        Record that a signal was emitted.
        
        Args:
            forced (bool): Whether this was a forced signal
            
        Returns:
            Dict[str, Any]: Timing information
        """
        current_time = datetime.now()
        elapsed = None
        
        if self.last_signal_time:
            elapsed = (current_time - self.last_signal_time).total_seconds() / 60
        
        self.last_signal_time = current_time
        self.next_allowed_time = current_time + timedelta(minutes=self.min_gap_minutes)
        
        return {
            'emission_time': current_time,
            'elapsed_minutes': elapsed,
            'timing_status': 'forced' if forced else 'normal',
            'next_allowed': self.next_allowed_time
        }

class HistoricalDataCollector:
    """Real-time historical data collection with proper error handling."""
    
    def __init__(self):
        """Initialize data collector."""
        self.max_days = 30
        self.min_days = 1
        self.rate_limit_delay = 1.0  # seconds between requests
        self.max_retries = 3
        self.retry_backoff = 2.0
        
    def validate_days_input(self, days_input: str) -> Optional[int]:
        """
        Validate user input for number of days.
        
        Args:
            days_input (str): User input
            
        Returns:
            Optional[int]: Validated days or None if invalid
        """
        try:
            days = int(days_input.strip())
            if self.min_days <= days <= self.max_days:
                return days
            return None
        except ValueError:
            return None
    
    def determine_granularity(self, days: int) -> str:
        """
        Determine appropriate data granularity based on time window.
        
        Args:
            days (int): Number of days
            
        Returns:
            str: Granularity ('1min', '5min', '15min', '1hour')
        """
        if days <= 5:
            return '1min'
        elif days <= 15:
            return '5min'
        elif days <= 30:
            return '15min'
        else:
            return '1hour'
    
    def calculate_time_window(self, days: int) -> tuple:
        """
        Calculate start and end times for data collection.
        
        Args:
            days (int): Number of days to collect
            
        Returns:
            tuple: (start_time, end_time)
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        return start_time, end_time
    
    def estimate_data_points(self, days: int, granularity: str) -> int:
        """
        Estimate number of data points to be collected.
        
        Args:
            days (int): Number of days
            granularity (str): Data granularity
            
        Returns:
            int: Estimated number of data points
        """
        trading_hours_per_day = 24  # Forex trades 24/5
        
        granularity_minutes = {
            '1min': 1,
            '5min': 5,
            '15min': 15,
            '1hour': 60
        }
        
        minutes_per_interval = granularity_minutes.get(granularity, 5)
        points_per_day = (trading_hours_per_day * 60) // minutes_per_interval
        
        return days * points_per_day
    
    def collect_historical_data(self, market: str, days: int, 
                              progress_callback=None) -> Dict[str, Any]:
        """
        Collect historical data for specified market and time period.
        
        Args:
            market (str): Market symbol
            days (int): Number of days to collect
            progress_callback: Optional callback for progress updates
            
        Returns:
            Dict[str, Any]: Collection results
        """
        start_time, end_time = self.calculate_time_window(days)
        granularity = self.determine_granularity(days)
        estimated_points = self.estimate_data_points(days, granularity)
        
        collection_info = {
            'market': market,
            'start_time': start_time,
            'end_time': end_time,
            'granularity': granularity,
            'estimated_points': estimated_points,
            'status': 'started',
            'collected_points': 0,
            'errors': []
        }
        
        if progress_callback:
            progress_callback(f"Starting data collection for {market}")
            progress_callback(f"Period: {start_time.strftime('%Y-%m-%d')} to {end_time.strftime('%Y-%m-%d')}")
            progress_callback(f"Granularity: {granularity}, Estimated points: {estimated_points}")
        
        try:
            # Simulate data collection (replace with actual API calls)
            collected_data = self._simulate_data_collection(
                market, start_time, end_time, granularity, progress_callback
            )
            
            collection_info.update({
                'status': 'completed',
                'collected_points': len(collected_data),
                'data': collected_data
            })
            
        except Exception as e:
            collection_info.update({
                'status': 'failed',
                'errors': [str(e)]
            })
        
        return collection_info
    
    def _simulate_data_collection(self, market: str, start_time: datetime, 
                                end_time: datetime, granularity: str, 
                                progress_callback=None) -> List[Dict]:
        """
        Simulate historical data collection.
        
        Args:
            market (str): Market symbol
            start_time (datetime): Start time
            end_time (datetime): End time
            granularity (str): Data granularity
            progress_callback: Progress callback function
            
        Returns:
            List[Dict]: Simulated historical data
        """
        data = []
        current_time = start_time
        
        granularity_delta = {
            '1min': timedelta(minutes=1),
            '5min': timedelta(minutes=5),
            '15min': timedelta(minutes=15),
            '1hour': timedelta(hours=1)
        }
        
        delta = granularity_delta.get(granularity, timedelta(minutes=5))
        base_price = 1.1000 if 'USD' in market else 100.0
        current_price = base_price
        
        point_count = 0
        total_points = int((end_time - start_time).total_seconds() / delta.total_seconds())
        
        while current_time < end_time:
            # Simulate price movement
            change = random.uniform(-0.002, 0.002)
            open_price = current_price
            close_price = current_price * (1 + change)
            high_price = max(open_price, close_price) * (1 + random.uniform(0, 0.001))
            low_price = min(open_price, close_price) * (1 - random.uniform(0, 0.001))
            volume = random.uniform(1000, 10000)
            
            data.append({
                'timestamp': current_time,
                'open': open_price,
                'high': high_price,
                'low': low_price,
                'close': close_price,
                'volume': volume
            })
            
            current_price = close_price
            current_time += delta
            point_count += 1
            
            # Progress update every 100 points
            if point_count % 100 == 0 and progress_callback:
                progress = (point_count / total_points) * 100
                progress_callback(f"Collected {point_count}/{total_points} points ({progress:.1f}%)")
            
            # Simulate rate limiting
            time.sleep(0.001)  # Small delay to simulate API calls
        
        return data

class MarketAnalyzer:
    """
    Enhanced market analyzer with proper error handling.
    """
    
    @staticmethod
    def analyze_market(market_name, days, use_news_filter=True):
        """
        Analyze a market for the given number of days with enhanced error handling.
        
        Args:
            market_name (str): The market to analyze
            days (int): Number of days to analyze
            use_news_filter (bool): Whether to apply news filters
            
        Returns:
            dict: Analysis results
        """
        try:
            if market_name not in MARKETS:
                return {"success": False, "error": "Market not found"}
            
            market_info = MARKETS[market_name]
            volatility = market_info["volatility"]
            
            # Simulate different trend strengths based on volatility
            trend_strength = {
                "low": 0.3,
                "medium": 0.5,
                "high": 0.7,
                "very high": 0.9
            }.get(volatility, 0.5)
            
            # Apply news filter effect (simulated)
            if use_news_filter and str(use_news_filter).lower() == "yes":
                trend_strength *= 1.2  # News filter improves trend detection
            
            return {
                "success": True,
                "market": market_name,
                "days_analyzed": days,
                "trend_strength": min(trend_strength, 1.0),  # Cap at 1.0
                "volatility": volatility,
                "news_filtered": use_news_filter,
                "category": market_info.get("category", "unknown")
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Analysis failed: {str(e)}",
                "market": market_name
            }