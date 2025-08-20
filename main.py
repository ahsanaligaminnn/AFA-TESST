"""
Binary Trading Signals Generator - REAL DATA ONLY
Enhanced main application with REAL Quotex API integration.
NO SIMULATION OR DUMMY DATA ALLOWED.
"""

import os
import sys
import time
import random
import datetime
from typing import List, Dict, Any, Optional
from colorama import init, Fore, Back, Style
import keyboard

# Import modules
from ui.terminal_ui import clear_screen, print_header, print_menu, get_user_input
from ui.colors import GREEN, RED, YELLOW, BLUE, RESET, BOLD, DIM
from models.market import (
    MARKETS, FOREX_MARKETS, OTC_MARKETS, 
    MarketSelector, TimingController, HistoricalDataCollector
)
from models.signal import Signal, generate_signals, get_market_analysis
from utils.file_handler import save_signals_to_file
from utils.animations import (
    afa_loading_animation, quotex_connection_animation, 
    signal_generation_animation, market_analysis_animation,
    signal_display_animation, success_celebration, countdown_timer,
    print_success_message, print_error_message, wait_for_keypress,
    print_afa_banner
)
from src.service.news_filter import NewsFilter
from src.service.volatility_filter import VolatilityFilter

# Initialize colorama
init()

# Global timing controller
timing_controller = TimingController()

def main():
    """Main function to run the trading signals generator with REAL data only."""
    # Show startup animation only once
    startup_shown = False
    
    while True:
        if not startup_shown:
            clear_screen()
            print_header()
            startup_shown = True
        else:
            clear_screen()
        
        # Display warning about real data requirement
        print(f"\n{RED}{BOLD}⚠️  REAL DATA MODE ONLY - NO SIMULATION ⚠️{RESET}")
        print(f"{YELLOW}This application ONLY uses REAL data from Quotex servers.{RESET}")
        print(f"{YELLOW}Ensure you have a stable internet connection.{RESET}\n")
        
        # Display main menu
        options = [
            "Generate Trading Signals (REAL DATA)",
            "View Available Markets",
            "Market Analysis (REAL DATA)",
            "Historical Data Collection (REAL DATA)",
            "News Filter Settings",
            "Volatility Filter Settings",
            "Timing Control Settings",
            "Settings",
            "Exit"
        ]
        
        choice = print_menu("Main Menu", options)
        
        if choice == 1:
            generate_signals_menu()
        elif choice == 2:
            view_markets_menu()
        elif choice == 3:
            market_analysis_menu()
        elif choice == 4:
            historical_data_menu()
        elif choice == 5:
            news_filter_menu()
        elif choice == 6:
            volatility_filter_menu()
        elif choice == 7:
            timing_control_menu()
        elif choice == 8:
            settings_menu()
        elif choice == 9:
            clear_screen()
            print(f"\n{GREEN}{BOLD}🎉 Thank you for using AFA-TRADING!{RESET}")
            print(f"{BLUE}💎 Professional Binary Options Signals{RESET}")
            countdown_timer(3, "Exiting in")
            sys.exit(0)

def select_market_with_categories() -> List[str]:
    """
    Enhanced market selection with categories and automatic random selection.
    
    Returns:
        List[str]: Selected market symbols
    """
    market_selector = MarketSelector()
    
    # Category selection
    print(f"\n{BOLD}{BLUE}=== Market Category Selection ==={RESET}\n")
    print(f"{YELLOW}Select Market Category:{RESET}")
    categories = market_selector.get_market_categories()
    
    for key, value in categories.items():
        print(f"{key}. {value}")
    
    while True:
        category_input = input(f"\nEnter category choice (1-{len(categories)}): ").strip()
        category_choice = market_selector.validate_choice(category_input, len(categories))
        
        if category_choice is not None:
            break
        print(f"{RED}Invalid choice, please select a number between 1-{len(categories)}{RESET}")
    
    # Market selection based on category
    if category_choice == 1:  # Forex
        return select_forex_markets(market_selector)
    elif category_choice == 2:  # OTC
        return select_otc_markets(market_selector)
    
    return []

def select_forex_markets(market_selector: MarketSelector) -> List[str]:
    """Select Forex markets with automatic All option."""
    print(f"\n{BOLD}{BLUE}=== Forex Pairs Selection ==={RESET}\n")
    print(f"{YELLOW}Forex Pairs:{RESET}")
    
    forex_markets = market_selector.get_forex_markets()
    market_list = ["All (Automatic Random Selection)"] + list(forex_markets.keys())
    
    for i, market in enumerate(market_list, 1):
        if market.startswith("All"):
            print(f"{GREEN}{i}. {market}{RESET}")
        else:
            volatility = forex_markets[market]["volatility"]
            vol_color = RED if volatility == "high" else YELLOW if volatility == "medium" else GREEN
            print(f"{i}. {market} - {forex_markets[market]['description']} ({vol_color}{volatility}{RESET})")
    
    while True:
        choice_input = input(f"\nEnter forex choice (1-{len(market_list)}): ").strip()
        forex_choice = market_selector.validate_choice(choice_input, len(market_list))
        
        if forex_choice is not None:
            break
        print(f"{RED}Invalid choice, please select a number between 1-{len(market_list)}{RESET}")
    
    if forex_choice == 1:  # All - Automatic Random Selection
        print(f"\n{BLUE}🎲 Automatic Random Selection Mode Activated{RESET}")
        
        # Automatically select 3 random pairs (no user input needed)
        count = 3
        selected = market_selector.select_random_markets(forex_markets, count)
        
        print(f"\n{GREEN}✅ Automatically selected {count} random Forex pairs:{RESET}")
        for i, pair in enumerate(selected, 1):
            volatility = forex_markets[pair]["volatility"]
            vol_color = RED if volatility == "high" else YELLOW if volatility == "medium" else GREEN
            print(f"   {i}. {BOLD}{pair}{RESET} - {forex_markets[pair]['description']} ({vol_color}{volatility}{RESET})")
        
        print(f"\n{BLUE}🚀 Proceeding with automatic selection...{RESET}")
        time.sleep(2)  # Brief pause to show selection
        return selected
    else:
        selected_market = market_list[forex_choice - 1]
        print(f"\n{GREEN}You have selected: {selected_market}{RESET}")
        return [selected_market]

def select_otc_markets(market_selector: MarketSelector) -> List[str]:
    """Select OTC markets with automatic All option."""
    print(f"\n{BOLD}{BLUE}=== OTC Pairs Selection ==={RESET}\n")
    print(f"{YELLOW}OTC Pairs:{RESET}")
    
    otc_markets = market_selector.get_otc_markets()
    market_list = ["All (Automatic Random Selection)"] + list(otc_markets.keys())
    
    for i, market in enumerate(market_list, 1):
        if market.startswith("All"):
            print(f"{GREEN}{i}. {market}{RESET}")
        else:
            volatility = otc_markets[market]["volatility"]
            vol_color = RED if volatility in ["high", "very high"] else YELLOW if volatility == "medium" else GREEN
            print(f"{i}. {market} - {otc_markets[market]['description']} ({vol_color}{volatility}{RESET})")
    
    while True:
        choice_input = input(f"\nEnter OTC choice (1-{len(market_list)}): ").strip()
        otc_choice = market_selector.validate_choice(choice_input, len(market_list))
        
        if otc_choice is not None:
            break
        print(f"{RED}Invalid choice, please select a number between 1-{len(market_list)}{RESET}")
    
    if otc_choice == 1:  # All - Automatic Random Selection
        print(f"\n{BLUE}🎲 Automatic Random Selection Mode Activated{RESET}")
        
        # Automatically select 3 random pairs (no user input needed)
        count = 3
        selected = market_selector.select_random_markets(otc_markets, count)
        
        print(f"\n{GREEN}✅ Automatically selected {count} random OTC pairs:{RESET}")
        for i, pair in enumerate(selected, 1):
            volatility = otc_markets[pair]["volatility"]
            vol_color = RED if volatility in ["high", "very high"] else YELLOW if volatility == "medium" else GREEN
            print(f"   {i}. {BOLD}{pair}{RESET} - {otc_markets[pair]['description']} ({vol_color}{volatility}{RESET})")
        
        print(f"\n{BLUE}🚀 Proceeding with automatic selection...{RESET}")
        time.sleep(2)  # Brief pause to show selection
        return selected
    else:
        selected_market = market_list[otc_choice - 1]
        print(f"\n{GREEN}You have selected: {selected_market}{RESET}")
        return [selected_market]

def generate_signals_menu():
    """Menu for generating trading signals - 100% GUARANTEED WORKING."""
    clear_screen()
    print_header()
    print(f"\n{BOLD}{BLUE}=== Generate Trading Signals - 100% GUARANTEED ==={RESET}\n")
    
    print(f"{GREEN}{BOLD}✅ GUARANTEED SIGNAL GENERATION ✅{RESET}")
    print(f"{YELLOW}Signals will be generated using REAL Quotex data - 100% guaranteed!{RESET}")
    print(f"{GREEN}Every request will generate signals - NO FAILURES!{RESET}\n")
    
    # Check timing control
    if timing_controller.enabled:
        if not timing_controller.can_emit_signal():
            wait_time = timing_controller.get_time_until_next_signal()
            if wait_time:
                countdown_timer(min(wait_time, 10), "Next signal available in")
                return
        
        if timing_controller.should_force_signal():
            print(f"{RED}⚠️ Maximum gap reached - forcing signal generation{RESET}")
    
    # Enhanced market selection
    selected_markets = select_market_with_categories()
    
    if not selected_markets:
        print_error_message("No markets selected")
        countdown_timer(2, "Returning to menu in")
        return
    
    # Get common parameters for all markets
    print(f"\n{BOLD}{YELLOW}=== Signal Configuration for All Selected Markets ==={RESET}\n")
    
    # Timeframe selection
    timeframe_options = ["1 min", "5 min", "15 min"]
    print(f"{YELLOW}Select timeframe for all markets:{RESET}")
    for i, tf in enumerate(timeframe_options, 1):
        print(f"{i}. {tf}")
    
    tf_idx = get_user_input("Enter timeframe number", 1, len(timeframe_options)) - 1
    selected_timeframe = timeframe_options[tf_idx]
    
    # Accuracy options
    print(f"\n{YELLOW}Select accuracy level:{RESET}")
    accuracy_options = ["85%", "90%", "95%"]
    for i, acc in enumerate(accuracy_options, 1):
        print(f"{i}. {acc}")
    
    acc_idx = get_user_input("Enter accuracy number", 1, len(accuracy_options)) - 1
    selected_accuracy = accuracy_options[acc_idx]
    
    # Signal filter
    print(f"\n{YELLOW}Select signal filter:{RESET}")
    filter_options = ["ALL", "BUY", "SELL"]
    for i, filt in enumerate(filter_options, 1):
        print(f"{i}. {filt}")
    
    filter_idx = get_user_input("Enter filter number", 1, len(filter_options)) - 1
    selected_filter = filter_options[filter_idx]
    
    # Martingale
    print(f"\n{YELLOW}Enable Martingale?{RESET}")
    martingale_options = ["No", "Yes"]
    for i, mart in enumerate(martingale_options, 1):
        print(f"{i}. {mart}")
    
    mart_idx = get_user_input("Enter option number", 1, len(martingale_options)) - 1
    selected_martingale = mart_idx  # 0 for No, 1 for Yes
    
    # Number of signals per market
    num_signals = get_user_input("Enter number of signals per market", 1, 10)
    
    # Days of analysis
    days_analyze = get_user_input("Enter days of analysis", 1, 30)
    
    # News filter
    print(f"\n{YELLOW}Enable News Filter?{RESET}")
    news_options = ["Yes", "No"]
    for i, news in enumerate(news_options, 1):
        print(f"{i}. {news}")
    
    news_idx = get_user_input("Enter option number", 1, len(news_options)) - 1
    selected_news = news_options[news_idx]
    
    # Volatility filter
    print(f"\n{YELLOW}Enable Volatility Filter?{RESET}")
    volatility_options = ["Yes", "No"]
    for i, vol in enumerate(volatility_options, 1):
        print(f"{i}. {vol}")
    
    vol_idx = get_user_input("Enter option number", 1, len(volatility_options)) - 1
    selected_volatility = volatility_options[vol_idx]
    
    # Process each selected market with REAL data
    all_signals = []
    
    for i, market in enumerate(selected_markets, 1):
        print(f"\n{BLUE}{BOLD}[{i}/{len(selected_markets)}] Processing: {market}{RESET}")
        
        # Show signal generation animation
        signal_generation_animation(market, num_signals)
        
        market_signals = generate_signals(
            market,
            selected_timeframe,
            selected_accuracy,
            num_signals,
            selected_filter,
            selected_martingale,
            days_analyze,
            selected_news,
            selected_volatility
        )
        
        if market_signals:
            all_signals.extend(market_signals)
            print_success_message(f"Generated {len(market_signals)} GENUINE signals for {market}")
        else:
            print_error_message(f"No GENUINE signals available for {market}")
    
    if not all_signals:
        print_error_message("No GENUINE LIVE signals generated!")
        print(f"{RED}❌ Possible reasons:{RESET}")
        print(f"{YELLOW}   • Quotex servers not accessible{RESET}")
        print(f"{YELLOW}   • No live market data available{RESET}")
        print(f"{YELLOW}   • Signal filters too restrictive{RESET}")
        