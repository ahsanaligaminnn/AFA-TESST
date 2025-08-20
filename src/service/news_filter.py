"""
Advanced News Filter implementation with sentiment analysis.
"""

import json
import subprocess
import time
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import re

class NewsFilter:
    def __init__(self):
        """Initialize the News Filter with sentiment analysis."""
        self.enabled = False
        self.positive_threshold = 0.1
        self.negative_threshold = -0.1
        self.cache_duration = 3600  # 1 hour cache
        self.news_cache = {}
        self.major_event_keywords = [
            'earnings', 'merger', 'acquisition', 'lawsuit', 'bankruptcy',
            'fed', 'interest rate', 'inflation', 'gdp', 'unemployment',
            'election', 'war', 'crisis', 'crash', 'rally'
        ]
        
    def enable_filter(self, positive_threshold: float = 0.1, negative_threshold: float = -0.1):
        """
        Enable news filtering with custom thresholds.
        
        Args:
            positive_threshold (float): Minimum positive sentiment for strong signals
            negative_threshold (float): Maximum negative sentiment before dropping signals
        """
        self.enabled = True
        self.positive_threshold = positive_threshold
        self.negative_threshold = negative_threshold
        
    def disable_filter(self):
        """Disable news filtering."""
        self.enabled = False
        
    def fetch_news(self, symbol: str, hours_back: int = 12) -> List[Dict]:
        """
        Fetch recent news for a given symbol/asset.
        
        Args:
            symbol (str): Asset symbol (e.g., 'EURUSD', 'GBPUSD')
            hours_back (int): How many hours back to fetch news
            
        Returns:
            List[Dict]: List of news articles with metadata
        """
        # Check cache first
        cache_key = f"{symbol}_{hours_back}"
        if cache_key in self.news_cache:
            cached_time, cached_data = self.news_cache[cache_key]
            if time.time() - cached_time < self.cache_duration:
                return cached_data
        
        try:
            # Extract currency from symbol for news search
            currencies = self._extract_currencies(symbol)
            search_terms = currencies + ['forex', 'trading', 'market']
            
            # For demo purposes, return mock news data
            mock_news = [
                {
                    "title": "EUR/USD shows bullish momentum amid ECB policy",
                    "description": "European Central Bank maintains dovish stance",
                    "publishedAt": datetime.now().isoformat(),
                    "source": {"name": "Financial Times"},
                    "url": "https://example.com"
                },
                {
                    "title": "USD strengthens on positive economic data",
                    "description": "US employment figures exceed expectations",
                    "publishedAt": (datetime.now() - timedelta(hours=1)).isoformat(),
                    "source": {"name": "Reuters"},
                    "url": "https://example.com"
                }
            ]
            
            # Cache the results
            self.news_cache[cache_key] = (time.time(), mock_news)
            return mock_news
                
        except Exception as e:
            print(f"Error fetching news: {str(e)}")
            return []
    
    def _extract_currencies(self, symbol: str) -> List[str]:
        """Extract currency codes from trading symbol."""
        # Common forex pairs
        if len(symbol) >= 6:
            base = symbol[:3]
            quote = symbol[3:6]
            return [base, quote]
        return [symbol]
    
    def analyze_sentiment(self, headlines: List[str]) -> float:
        """
        Analyze sentiment of news headlines using simple keyword-based approach.
        In production, use a proper NLP model like FinBERT.
        
        Args:
            headlines (List[str]): List of news headlines
            
        Returns:
            float: Average sentiment score (-1.0 to +1.0)
        """
        if not headlines:
            return 0.0
            
        # Simple keyword-based sentiment analysis
        positive_words = [
            'bullish', 'rally', 'surge', 'gains', 'positive', 'strong', 'rise',
            'boost', 'optimistic', 'growth', 'recovery', 'upbeat', 'soar'
        ]
        
        negative_words = [
            'bearish', 'crash', 'fall', 'decline', 'negative', 'weak', 'drop',
            'plunge', 'pessimistic', 'recession', 'crisis', 'concern', 'fear'
        ]
        
        total_score = 0.0
        total_weight = 0.0
        
        for headline in headlines:
            headline_lower = headline.lower()
            score = 0.0
            
            # Count positive and negative words
            pos_count = sum(1 for word in positive_words if word in headline_lower)
            neg_count = sum(1 for word in negative_words if word in headline_lower)
            
            # Calculate sentiment score
            if pos_count > 0 or neg_count > 0:
                score = (pos_count - neg_count) / (pos_count + neg_count + 1)
            
            # Weight by headline length (longer headlines get more weight)
            weight = min(len(headline.split()) / 10.0, 1.0)
            
            total_score += score * weight
            total_weight += weight
        
        return total_score / total_weight if total_weight > 0 else 0.0
    
    def detect_major_events(self, news_articles: List[Dict]) -> bool:
        """
        Detect if there are any major market-moving events in the news.
        
        Args:
            news_articles (List[Dict]): List of news articles
            
        Returns:
            bool: True if major events detected, False otherwise
        """
        for article in news_articles:
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            
            for keyword in self.major_event_keywords:
                if keyword in title or keyword in description:
                    return True
        
        return False
    
    def apply_time_decay(self, news_articles: List[Dict]) -> List[Dict]:
        """
        Apply time decay to news articles (recent news has more weight).
        
        Args:
            news_articles (List[Dict]): List of news articles
            
        Returns:
            List[Dict]: Articles with decay weights applied
        """
        current_time = datetime.now()
        weighted_articles = []
        
        for article in news_articles:
            try:
                pub_time_str = article['publishedAt']
                if pub_time_str.endswith('Z'):
                    pub_time_str = pub_time_str[:-1] + '+00:00'
                
                pub_time = datetime.fromisoformat(pub_time_str)
                if pub_time.tzinfo is not None:
                    pub_time = pub_time.replace(tzinfo=None)
                
                hours_diff = (current_time - pub_time).total_seconds() / 3600
                
                # Exponential decay: weight = exp(-λ * hours)
                decay_factor = 0.1  # λ parameter
                weight = max(0.1, 2.71828 ** (-decay_factor * hours_diff))
                
                article['weight'] = weight
                weighted_articles.append(article)
                
            except Exception:
                # If time parsing fails, give minimum weight
                article['weight'] = 0.1
                weighted_articles.append(article)
        
        return weighted_articles
    
    def filter_signal(self, signal: Dict, symbol: str) -> Dict:
        """
        Apply news filter to a trading signal.
        
        Args:
            signal (Dict): Original trading signal
            symbol (str): Trading symbol
            
        Returns:
            Dict: Filtered signal with news analysis
        """
        if not self.enabled:
            signal['news_filter'] = {
                'status': 'disabled',
                'sentiment_score': 0.0,
                'filter_result': 'passed'
            }
            return signal
        
        # Fetch recent news
        news_articles = self.fetch_news(symbol, hours_back=12)
        
        if not news_articles:
            signal['news_filter'] = {
                'status': 'no_news',
                'sentiment_score': 0.0,
                'filter_result': 'passed'
            }
            return signal
        
        # Apply time decay
        weighted_articles = self.apply_time_decay(news_articles)
        
        # Extract headlines for sentiment analysis
        headlines = [article.get('title', '') for article in weighted_articles]
        
        # Calculate weighted sentiment
        sentiment_score = self.analyze_sentiment(headlines)
        
        # Detect major events
        has_major_events = self.detect_major_events(weighted_articles)
        
        # Apply filtering logic
        filter_result = 'passed'
        
        if has_major_events:
            filter_result = 'major_event_detected'
        elif sentiment_score < self.negative_threshold:
            filter_result = 'negative_sentiment'
        elif sentiment_score >= self.positive_threshold:
            filter_result = 'strong_positive'
        else:
            filter_result = 'neutral'
        
        # Add news filter information to signal
        signal['news_filter'] = {
            'status': 'active',
            'sentiment_score': sentiment_score,
            'filter_result': filter_result,
            'major_events': has_major_events,
            'news_count': len(news_articles),
            'headlines_used': headlines[:3]  # First 3 headlines for audit
        }
        
        # Modify signal strength based on news
        if filter_result == 'negative_sentiment' or filter_result == 'major_event_detected':
            signal['strength'] = 'blocked'
        elif filter_result == 'strong_positive':
            signal['strength'] = 'strong'
        else:
            signal['strength'] = 'normal'
        
        return signal
    
    def get_filter_stats(self) -> Dict:
        """
        Get statistics about the news filter performance.
        
        Returns:
            Dict: Filter statistics
        """
        return {
            'enabled': self.enabled,
            'positive_threshold': self.positive_threshold,
            'negative_threshold': self.negative_threshold,
            'cache_size': len(self.news_cache),
            'major_event_keywords': len(self.major_event_keywords)
        }