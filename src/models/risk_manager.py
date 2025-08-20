"""
Risk management and Martingale strategy implementation.
"""

from typing import Dict, Optional
from datetime import datetime

class RiskManager:
    def __init__(self, initial_balance: float, base_stake_percent: float = 1.0,
                 max_martingale_tier: int = 4, max_daily_loss_percent: float = 10.0):
        """
        Initialize risk manager.
        
        Args:
            initial_balance (float): Initial account balance
            base_stake_percent (float): Base stake as percentage of balance
            max_martingale_tier (int): Maximum Martingale multiplication tier
            max_daily_loss_percent (float): Maximum daily loss percentage
        """
        self.initial_balance = initial_balance
        self.current_balance = initial_balance
        self.base_stake_percent = base_stake_percent
        self.max_martingale_tier = max_martingale_tier
        self.max_daily_loss = initial_balance * (max_daily_loss_percent / 100)
        
        self.current_tier = 1
        self.daily_loss = 0
        self.daily_profit = 0
        self.last_reset = datetime.now().date()
    
    def reset_daily_stats(self):
        """Reset daily statistics if it's a new day."""
        current_date = datetime.now().date()
        if current_date > self.last_reset:
            self.daily_loss = 0
            self.daily_profit = 0
            self.last_reset = current_date
    
    def calculate_stake(self) -> Optional[float]:
        """
        Calculate stake amount based on current Martingale tier.
        
        Returns:
            Optional[float]: Stake amount if trading allowed, None if blocked
        """
        self.reset_daily_stats()
        
        # Check if daily loss limit reached
        if self.daily_loss >= self.max_daily_loss:
            return None
        
        # Calculate base stake
        base_stake = self.current_balance * (self.base_stake_percent / 100)
        
        # Apply Martingale multiplier
        stake = base_stake * (2 ** (self.current_tier - 1))
        
        return round(stake, 2)
    
    def update_balance(self, profit_loss: float, win: bool):
        """
        Update balance and Martingale tier based on trade result.
        
        Args:
            profit_loss (float): Profit (positive) or loss (negative) amount
            win (bool): Whether the trade was successful
        """
        self.current_balance += profit_loss
        
        if win:
            self.current_tier = 1  # Reset Martingale tier on win
            self.daily_profit += profit_loss
        else:
            self.daily_loss -= profit_loss  # profit_loss is negative for losses
            if self.current_tier < self.max_martingale_tier:
                self.current_tier += 1
            else:
                self.current_tier = 1  # Reset after reaching max tier
    
    def can_trade(self) -> bool:
        """
        Check if trading is allowed based on risk parameters.
        
        Returns:
            bool: True if trading is allowed, False otherwise
        """
        self.reset_daily_stats()
        return self.daily_loss < self.max_daily_loss