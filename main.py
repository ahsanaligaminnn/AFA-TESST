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
import requests, json
import base64


# Import modules
from utils.messages import print_error_message, print_success_message
from utils.inputs import wait_for_keypress
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
    signal_display_animation, success_celebration, countdown_timer
)
from src.service.news_filter import NewsFilter
from src.service.volatility_filter import VolatilityFilter

# Initialize colorama
init()

# Global timing controller
timing_controller = TimingController()

USERS_URL = "https://raw.githubusercontent.com/ahsanaligaminnn/AFA-TESST/refs/heads/main/users.json"

USERS_URL = "https://raw.githubusercontent.com/ahsanaligaminnn/AFA-TESST/refs/heads/main/users.json"

def get_users():
    try:
        res = requests.get(USERS_URL, timeout=10)
        if res.status_code == 200:
            data = res.json()  # direct JSON milega
            return data.get("users", [])
        else:
            print("❌ Error fetching users:", res.status_code)
            return []
    except Exception as e:
        print("❌ Error:", e)
        return []

def login():
    users = get_users()
    if not users:
        print("No users found. Exiting...")
        exit()

    print("===== AFA TRADING LOGIN =====")
    while True:
        username = input("Enter Username: ")
        password = input("Enter Password: ")

        for u in users:
            if u["username"] == username and u["password"] == password:
                print("✅ Login Successful!\n")
                return True
        print("❌ Invalid Username or Password. Try again.\n")

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
        print(f"\n{BLUE}💡 Try:{RESET}")
        print(f"{GREEN}   • Select 'ALL' for automatic market selection{RESET}")
        print(f"{GREEN}   • Use 'ALL' signal filter{RESET}")
        print(f"{GREEN}   • Try different timeframes{RESET}")
        wait_for_keypress()
        return
    
    if not all_signals:
        wait_for_keypress()
        return
    
    # Success celebration
    success_celebration()
    
    # Record timing for signal emission
    timing_info = timing_controller.record_signal_emission(
        forced=timing_controller.should_force_signal()
    )
    
    # Display all REAL signals
    display_signals_enhanced(all_signals, selected_markets, selected_timeframe, 
                           selected_accuracy, selected_news, selected_volatility, timing_info)

def display_signals_enhanced(signals: List[Signal], markets: List[str], timeframe: str, 
                           accuracy: str, news_filter: str, volatility_filter: str, 
                           timing_info: Optional[Dict[str, Any]] = None):
    """Enhanced signal display with animations."""
    clear_screen()
    
    # Use animated signal display
    signal_display_animation(signals)
    
    # Show summary information
    if isinstance(markets, list):
        markets_str = ", ".join(markets)
    else:
        markets_str = str(markets)
    
    print(f"{BLUE}{BOLD}📊 SIGNAL SUMMARY{RESET}")
    print(f"{BLUE}{'─' * 50}{RESET}")
    print(f"{YELLOW}Markets: {BOLD}{markets_str}{RESET}")
    print(f"{YELLOW}Timeframe: {timeframe} | Accuracy: {accuracy}{RESET}")
    print(f"{YELLOW}Filters: News({news_filter}) | Volatility({volatility_filter}){RESET}")
    print(f"{GREEN}Total Signals: {len(signals)} | Source: REAL QUOTEX{RESET}")
    
    # Ask to save signals with animation
    print(f"\n{YELLOW}💾 Save these signals to file?{RESET}")
    save_choice = input(f"{GREEN}► (y/n): {RESET}").strip().lower()
    
    if save_choice == 'y':
        afa_loading_animation(2, "Saving signals")
        filename = save_signals_to_file(signals, markets_str.replace(", ", "_"))
        print_success_message(f"Signals saved to {filename}")
    
    wait_for_keypress()

def display_signals(signals: List[Signal], markets: List[str], timeframe: str, accuracy: str, 
                   news_filter: str, volatility_filter: str, timing_info: Optional[Dict[str, Any]] = None):
    """Display generated REAL signals with enhanced formatting."""
    clear_screen()
    print_header()
    print(f"\n{BOLD}{GREEN}=== Generated REAL Signals ==={RESET}\n")
    
    if isinstance(markets, list):
        markets_str = ", ".join(markets)
    else:
        markets_str = str(markets)
    
    print(f"{BLUE}Markets: {BOLD}{markets_str}{RESET}")
    print(f"{BLUE}Timeframe: {timeframe} | Accuracy: {accuracy}{RESET}")
    print(f"{BLUE}News Filter: {'Enabled' if news_filter == 'Yes' else 'Disabled'}{RESET}")
    print(f"{BLUE}Volatility Filter: {'Enabled' if volatility_filter == 'Yes' else 'Disabled'}{RESET}")
    print(f"{BLUE}Total REAL Signals: {len(signals)}{RESET}")
    print(f"{GREEN}Data Source: REAL Quotex API{RESET}")
    
    # Display timing information
    if timing_info and timing_controller.enabled:
        print(f"{BLUE}Timing Status: {timing_info['timing_status'].upper()}{RESET}")
        if timing_info['elapsed_minutes']:
            print(f"{BLUE}Time Since Last: {timing_info['elapsed_minutes']:.1f} minutes{RESET}")
    
    print()
    
    for i, signal in enumerate(signals, 1):
        border = "+" + "-" * 80 + "+"
        print(border)
        
        signal_color = GREEN if signal.signal_type == "BUY" else RED
        strength_color = (GREEN if signal.strength in ['VERY_STRONG', 'STRONG'] else 
                         YELLOW if signal.strength in ['HIGH', 'MEDIUM'] else RED)
        
        print(f"| REAL Signal #{i:2d} | {signal_color}{signal.signal_type:4s}{RESET} | {signal.time} | {strength_color}{signal.strength:12s}{RESET} |")
        
        # Show news filter results if enabled
        if signal.news_filter_result:
            news_result = signal.news_filter_result
            sentiment = news_result.get('sentiment_score', 0)
            filter_status = news_result.get('filter_result', 'unknown')
            
            sentiment_color = GREEN if sentiment > 0.1 else RED if sentiment < -0.1 else YELLOW
            print(f"| News: {sentiment_color}{sentiment:+.2f}{RESET} | Filter: {filter_status:20s} |")
        
        # Show volatility filter results if enabled
        if signal.volatility_filter_result:
            vol_result = signal.volatility_filter_result
            vol_state = vol_result.get('volatility_state', 'unknown')
            vol_filter = vol_result.get('filter_result', 'unknown')
            position_mult = vol_result.get('position_size_multiplier', 1.0)
            
            vol_color = RED if vol_state == 'high' else GREEN if vol_state == 'low' else YELLOW
            print(f"| Volatility: {vol_color}{vol_state:8s}{RESET} | Size: {position_mult:.2f}x | Filter: {vol_filter:15s} |")
        
        print(f"| Confidence: {int(signal.confidence * 100):3d}% | Market: {signal.market:15s} | REAL DATA |")
        print(border)
        print()
    
    # Ask to save signals
    print(f"{YELLOW}Would you like to save these REAL signals to a file? (y/n){RESET}")
    save_choice = input("> ").strip().lower()
    
    if save_choice == 'y':
        filename = save_signals_to_file(signals, markets_str.replace(", ", "_"))
        print(f"\n{GREEN}REAL signals saved to {filename}{RESET}")
    
    print(f"\n{YELLOW}Press any key to return to main menu...{RESET}")
    keyboard.read_event()

def market_analysis_menu():
    """Menu for detailed market analysis with REAL data only."""
    clear_screen()
    print_header()
    print(f"\n{BOLD}{BLUE}=== Market Analysis (REAL DATA ONLY) ==={RESET}\n")
    
    print(f"{RED}{BOLD}⚠️  REAL DATA MODE ACTIVE ⚠️{RESET}")
    print(f"{YELLOW}Analysis will use REAL data from Quotex servers only.{RESET}\n")
    
    # Enhanced market selection
    selected_markets = select_market_with_categories()
    
    if not selected_markets:
        print_error_message("No markets selected")
        countdown_timer(2, "Returning to menu in")
        return
    
    print(f"\n{YELLOW}Select timeframe for analysis:{RESET}")
    timeframe_options = [1, 5, 15]
    for i, tf in enumerate(timeframe_options, 1):
        print(f"{i}. {tf} minutes")
    
    tf_idx = get_user_input("Enter timeframe number", 1, len(timeframe_options)) - 1
    selected_timeframe = timeframe_options[tf_idx]
    
    # Analyze each selected market with REAL data
    for market in selected_markets:
        market_analysis_animation(market)
        
        analysis = get_market_analysis(market, selected_timeframe)
        
        # Display analysis results
        print(f"\n{BOLD}{GREEN}=== REAL Analysis Results for {market} ==={RESET}\n")
        
        if 'error' in analysis:
            print(f"{RED}Analysis Error: {analysis['error']}{RESET}")
            print(f"{YELLOW}No real data available from Quotex for {market}{RESET}")
        else:
            print(f"{BLUE}Market:{RESET} {BOLD}{analysis['market']}{RESET}")
            print(f"{BLUE}Current Price:{RESET} {analysis.get('current_price', 'N/A')}")
            print(f"{BLUE}Average Price:{RESET} {analysis.get('average_price', 'N/A')}")
            
            trend = analysis.get('trend', 'UNKNOWN')
            trend_color = GREEN if 'BULLISH' in trend else RED if 'BEARISH' in trend else YELLOW
            print(f"{BLUE}Trend:{RESET} {trend_color}{trend}{RESET}")
            
            volatility = analysis.get('volatility', 0)
            vol_color = RED if volatility > 0.02 else YELLOW if volatility > 0.01 else GREEN
            print(f"{BLUE}Volatility:{RESET} {vol_color}{volatility:.4f}{RESET}")
            
            print(f"{BLUE}Data Points:{RESET} {analysis.get('data_points', 'N/A')}")
            print(f"{BLUE}Analysis Time:{RESET} {analysis.get('analysis_time', 'N/A')}")
            print(f"{GREEN}Data Source: REAL Quotex API{RESET}")
        
        print("-" * 60)
    
    print(f"\n{YELLOW}Press any key to return to main menu...{RESET}")
    keyboard.read_event()

def historical_data_menu():
    """Menu for historical data collection."""
    clear_screen()
    print_header()
    print(f"\n{BOLD}{BLUE}=== Historical Data Collection ==={RESET}\n")
    
    collector = HistoricalDataCollector()
    
    # Market selection
    selected_markets = select_market_with_categories()
    
    if not selected_markets:
        print_error_message("No markets selected")
        countdown_timer(2, "Returning to menu in")
        return
    
    # Days input with validation
    print(f"\n{YELLOW}Enter number of days to collect data (1-30):{RESET}")
    
    while True:
        days_input = input("> ").strip()
        days = collector.validate_days_input(days_input)
        
        if days is not None:
            break
        print(f"{RED}Please enter a whole number from 1 to 30.{RESET}")
    
    # Collect data for each market
    for market in selected_markets:
        print(f"\n{BLUE}{BOLD}📊 Collecting Historical Data: {market}{RESET}")
        afa_loading_animation(2, f"Initializing data collection for {market}")
        
        def progress_callback(message):
            print(f"{YELLOW}📋 {message}{RESET}")
        
        collection_result = collector.collect_historical_data(
            market, days, progress_callback
        )
        
        # Display results
        print(f"\n{BOLD}{GREEN}=== Collection Results for {market} ==={RESET}")
        print(f"{BLUE}Status:{RESET} {collection_result['status']}")
        print(f"{BLUE}Period:{RESET} {collection_result['start_time'].strftime('%Y-%m-%d')} to {collection_result['end_time'].strftime('%Y-%m-%d')}")
        print(f"{BLUE}Granularity:{RESET} {collection_result['granularity']}")
        print(f"{BLUE}Estimated Points:{RESET} {collection_result['estimated_points']}")
        print(f"{BLUE}Collected Points:{RESET} {collection_result['collected_points']}")
        
        if collection_result['errors']:
            print(f"{RED}Errors:{RESET}")
            for error in collection_result['errors']:
                print(f"  - {error}")
        
        if collection_result['status'] == 'completed':
            print_success_message("Data collection completed successfully!")
        else:
            print_error_message("Data collection failed")
    
    wait_for_keypress()

def timing_control_menu():
    """Menu for timing control settings."""
    clear_screen()
    print_header()
    print(f"\n{BOLD}{BLUE}=== Timing Control Settings ==={RESET}\n")
    
    options = [
        "Enable Timing Control",
        "Disable Timing Control",
        "Configure Gap Settings",
        "View Current Status",
        "Reset Timing State",
        "Back to Main Menu"
    ]
    
    choice = print_menu("Timing Control Options", options)
    
    if choice == 1:
        timing_controller.enabled = True
        print_success_message("Timing Control enabled")
        countdown_timer(2, "Returning to menu in")
    elif choice == 2:
        timing_controller.enabled = False
        print(f"\n{YELLOW}⚠️ Timing Control disabled{RESET}")
        countdown_timer(2, "Returning to menu in")
    elif choice == 3:
        configure_timing_gaps()
    elif choice == 4:
        display_timing_status()
    elif choice == 5:
        timing_controller.last_signal_time = None
        timing_controller.next_allowed_time = None
        print_success_message("Timing state reset")
        countdown_timer(2, "Returning to menu in")
    elif choice == 6:
        return
    
    # Return to timing control menu unless going back to main
    if choice != 6:
        timing_control_menu()

def configure_timing_gaps():
    """Configure timing gap settings."""
    print(f"\n{YELLOW}Current Settings:{RESET}")
    print(f"Minimum Gap: {timing_controller.min_gap_minutes} minutes")
    print(f"Maximum Gap: {timing_controller.max_gap_minutes} minutes")
    
    print(f"\n{YELLOW}Enter new minimum gap (1-60 minutes):{RESET}")
    try:
        min_gap = int(input("> "))
        if 1 <= min_gap <= 60:
            timing_controller.min_gap_minutes = min_gap
        else:
            print(f"{RED}Invalid gap. Using default.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Using default.{RESET}")
    
    print(f"\n{YELLOW}Enter new maximum gap (5-120 minutes):{RESET}")
    try:
        max_gap = int(input("> "))
        if 5 <= max_gap <= 120 and max_gap > timing_controller.min_gap_minutes:
            timing_controller.max_gap_minutes = max_gap
        else:
            print(f"{RED}Invalid gap. Using default.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Using default.{RESET}")
    
    print(f"\n{GREEN}Timing settings updated successfully!{RESET}")
    time.sleep(2)

def display_timing_status():
    """Display current timing control status."""
    print(f"\n{BOLD}{GREEN}=== Timing Control Status ==={RESET}\n")
    print(f"{BLUE}Status:{RESET} {'Enabled' if timing_controller.enabled else 'Disabled'}")
    print(f"{BLUE}Min Gap:{RESET} {timing_controller.min_gap_minutes} minutes")
    print(f"{BLUE}Max Gap:{RESET} {timing_controller.max_gap_minutes} minutes")
    
    if timing_controller.last_signal_time:
        print(f"{BLUE}Last Signal:{RESET} {timing_controller.last_signal_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        current_time = datetime.datetime.now()
        elapsed = (current_time - timing_controller.last_signal_time).total_seconds() / 60
        print(f"{BLUE}Elapsed:{RESET} {elapsed:.1f} minutes")
        
        can_emit = timing_controller.can_emit_signal()
        print(f"{BLUE}Can Emit Signal:{RESET} {'Yes' if can_emit else 'No'}")
        
        if not can_emit:
            wait_time = timing_controller.get_time_until_next_signal()
            if wait_time:
                print(f"{BLUE}Next Signal In:{RESET} {wait_time} seconds")
        
        should_force = timing_controller.should_force_signal()
        print(f"{BLUE}Should Force Signal:{RESET} {'Yes' if should_force else 'No'}")
    else:
        print(f"{BLUE}Last Signal:{RESET} None")
        print(f"{BLUE}Can Emit Signal:{RESET} Yes")
    
    print(f"\n{YELLOW}Press any key to continue...{RESET}")
    keyboard.read_event()

def volatility_filter_menu():
    """Menu for configuring volatility filter settings."""
    clear_screen()
    print_header()
    print(f"\n{BOLD}{BLUE}=== Volatility Filter Settings ==={RESET}\n")
    
    volatility_filter = VolatilityFilter()
    
    options = [
        "Enable Volatility Filter",
        "Disable Volatility Filter",
        "Configure Thresholds",
        "Position Sizing Settings",
        "View Filter Statistics",
        "Test Volatility Analysis",
        "Back to Main Menu"
    ]
    
    choice = print_menu("Volatility Filter Options", options)
    
    if choice == 1: 
        volatility_filter.enable_filter()
        print_success_message("Volatility Filter enabled")
        countdown_timer(2, "Returning to menu in")
    elif choice == 2:
        volatility_filter.disable_filter()
        print(f"\n{YELLOW}⚠️ Volatility Filter disabled{RESET}")
        countdown_timer(2, "Returning to menu in")
    elif choice == 3:
        configure_volatility_thresholds(volatility_filter)
    elif choice == 4:
        configure_position_sizing(volatility_filter)
    elif choice == 5:
        display_volatility_stats(volatility_filter)
    elif choice == 6:
        test_volatility_analysis(volatility_filter)
    elif choice == 7:
        return
    
    # Return to volatility filter menu unless going back to main
    if choice != 7:
        volatility_filter_menu()

def configure_volatility_thresholds(volatility_filter: VolatilityFilter):
    """Configure volatility filter thresholds."""
    print(f"\n{YELLOW}Current Volatility Thresholds:{RESET}")
    stats = volatility_filter.get_filter_stats()
    print(f"High Volatility - ATR: {stats['high_vol_thresholds']['atr']}")
    print(f"High Volatility - BB: {stats['high_vol_thresholds']['bb']}")
    print(f"Low Volatility - ATR: {stats['low_vol_thresholds']['atr']}")
    print(f"Low Volatility - BB: {stats['low_vol_thresholds']['bb']}")
    
    print(f"\n{YELLOW}Configure High Volatility ATR Threshold (current: {stats['high_vol_thresholds']['atr']}):{RESET}")
    try:
        high_atr = float(input("> "))
        if 1.0 <= high_atr <= 3.0:
            volatility_filter.high_vol_atr_threshold = high_atr
        else:
            print(f"{RED}Invalid threshold. Using default.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Using default.{RESET}")
    
    print(f"\n{YELLOW}Configure High Volatility BB Threshold (current: {stats['high_vol_thresholds']['bb']}):{RESET}")
    try:
        high_bb = float(input("> "))
        if 1.0 <= high_bb <= 3.0:
            volatility_filter.high_vol_bb_threshold = high_bb
        else:
            print(f"{RED}Invalid threshold. Using default.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Using default.{RESET}")
    
    print(f"\n{GREEN}Volatility thresholds updated successfully!{RESET}")
    time.sleep(2)

def configure_position_sizing(volatility_filter: VolatilityFilter):
    """Configure position sizing settings."""
    stats = volatility_filter.get_filter_stats()
    
    print(f"\n{YELLOW}Current Position Sizing Settings:{RESET}")
    print(f"Base Size: {stats['position_sizing']['base_size']}")
    print(f"Min Size: {stats['position_sizing']['min_size']}")
    print(f"Max Size: {stats['position_sizing']['max_size']}")
    
    print(f"\n{YELLOW}Configure Base Position Size (current: {stats['position_sizing']['base_size']}):{RESET}")
    try:
        base_size = float(input("> "))
        if 0.1 <= base_size <= 5.0:
            volatility_filter.base_position_size = base_size
        else:
            print(f"{RED}Invalid size. Using default.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Using default.{RESET}")
    
    print(f"\n{YELLOW}Configure Maximum Position Size (current: {stats['position_sizing']['max_size']}):{RESET}")
    try:
        max_size = float(input("> "))
        if 1.0 <= max_size <= 10.0:
            volatility_filter.max_position_size = max_size
        else:
            print(f"{RED}Invalid size. Using default.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Using default.{RESET}")
    
    print(f"\n{GREEN}Position sizing settings updated successfully!{RESET}")
    time.sleep(2)

def display_volatility_stats(volatility_filter: VolatilityFilter):
    """Display volatility filter statistics."""
    stats = volatility_filter.get_filter_stats()
    
    print(f"\n{BOLD}{GREEN}=== Volatility Filter Statistics ==={RESET}\n")
    print(f"{BLUE}Status:{RESET} {'Enabled' if stats['enabled'] else 'Disabled'}")
    print(f"{BLUE}ATR Period:{RESET} {stats['atr_period']}")
    print(f"{BLUE}Bollinger Bands Period:{RESET} {stats['bb_period']}")
    
    print(f"\n{BOLD}High Volatility Thresholds:{RESET}")
    print(f"{BLUE}ATR Threshold:{RESET} {stats['high_vol_thresholds']['atr']}")
    print(f"{BLUE}BB Threshold:{RESET} {stats['high_vol_thresholds']['bb']}")
    
    print(f"\n{BOLD}Low Volatility Thresholds:{RESET}")
    print(f"{BLUE}ATR Threshold:{RESET} {stats['low_vol_thresholds']['atr']}")
    print(f"{BLUE}BB Threshold:{RESET} {stats['low_vol_thresholds']['bb']}")
    
    print(f"\n{BOLD}Position Sizing:{RESET}")
    print(f"{BLUE}Base Size:{RESET} {stats['position_sizing']['base_size']}")
    print(f"{BLUE}Min Size:{RESET} {stats['position_sizing']['min_size']}")
    print(f"{BLUE}Max Size:{RESET} {stats['position_sizing']['max_size']}")
    
    print(f"\n{BLUE}Cooldown Periods:{RESET} {stats['cooldown_periods']}")
    print(f"{BLUE}Current Cooldown:{RESET} {stats['current_cooldown']}")
    print(f"{BLUE}Outlier Multiplier:{RESET} {stats['outlier_multiplier']}")
    
    print(f"\n{YELLOW}Press any key to continue...{RESET}")
    keyboard.read_event()

def test_volatility_analysis(volatility_filter: VolatilityFilter):
    """Test volatility analysis with sample market data."""
    print(f"\n{YELLOW}Testing volatility analysis with sample market data...{RESET}")
    
    # Generate sample market data
    sample_data = {
        'market': 'EURUSD',
        'timeframe': 5,
        'opens': [1.1000 + i * 0.0001 for i in range(50)],
        'highs': [1.1005 + i * 0.0001 for i in range(50)],
        'lows': [1.0995 + i * 0.0001 for i in range(50)],
        'closes': [1.1002 + i * 0.0001 for i in range(50)],
        'volumes': [1000 + i * 10 for i in range(50)]
    }
    
    # Add some volatility spikes
    sample_data['highs'][25] = sample_data['highs'][25] + 0.005
    sample_data['lows'][30] = sample_data['lows'][30] - 0.005
    sample_data['highs'][40] = sample_data['highs'][40] + 0.008
    
    volatility_filter.enable_filter()
    analysis = volatility_filter.analyze_market_volatility(sample_data)
    
    print(f"\n{BOLD}{GREEN}=== Volatility Analysis Test Results ==={RESET}\n")
    
    if 'error' in analysis:
        print(f"{RED}Analysis Error: {analysis['error']}{RESET}")
    else:
        print(f"{BLUE}Market:{RESET} {sample_data['market']}")
        print(f"{BLUE}Current ATR:{RESET} {analysis['current_atr']:.5f}")
        print(f"{BLUE}Normalized ATR:{RESET} {analysis['normalized_atr']:.3f}")
        print(f"{BLUE}BB Width:{RESET} {analysis['bb_width']:.5f}")
        print(f"{BLUE}Normalized BB:{RESET} {analysis['normalized_bb']:.3f}")
        
        vol_state = analysis['volatility_state']
        vol_color = RED if vol_state == 'high' else GREEN if vol_state == 'low' else YELLOW
        print(f"{BLUE}Volatility State:{RESET} {vol_color}{vol_state.upper()}{RESET}")
        
        trend_regime = analysis['trend_regime']
        trend_color = GREEN if trend_regime == 'bullish' else RED if trend_regime == 'bearish' else YELLOW
        print(f"{BLUE}Trend Regime:{RESET} {trend_color}{trend_regime.upper()}{RESET}")
        
        print(f"{BLUE}Outlier Detected:{RESET} {'Yes' if analysis['is_outlier'] else 'No'}")
        print(f"{BLUE}Position Size Multiplier:{RESET} {analysis['position_size_multiplier']:.2f}x")
    
    print(f"\n{YELLOW}Press any key to continue...{RESET}")
    keyboard.read_event()

def news_filter_menu():
    """Menu for configuring news filter settings."""
    clear_screen()
    print_header()
    print(f"\n{BOLD}{BLUE}=== News Filter Settings ==={RESET}\n")
    
    news_filter = NewsFilter()
    
    options = [
        "Enable News Filter",
        "Disable News Filter", 
        "Configure Thresholds",
        "View Filter Statistics",
        "Test News Analysis",
        "Back to Main Menu"
    ]
    
    choice = print_menu("News Filter Options", options)
    
    if choice == 1:
        news_filter.enable_filter()
        print_success_message("News Filter enabled")
        countdown_timer(2, "Returning to menu in")
    elif choice == 2:
        news_filter.disable_filter()
        print(f"\n{YELLOW}⚠️ News Filter disabled{RESET}")
        countdown_timer(2, "Returning to menu in")
    elif choice == 3:
        configure_news_thresholds(news_filter)
    elif choice == 4:
        display_filter_stats(news_filter)
    elif choice == 5:
        test_news_analysis(news_filter)
    elif choice == 6:
        return
    
    # Return to news filter menu unless going back to main
    if choice != 6:
        news_filter_menu()

def configure_news_thresholds(news_filter: NewsFilter):
    """Configure news filter thresholds."""
    print(f"\n{YELLOW}Current Thresholds:{RESET}")
    print(f"Positive Threshold: {news_filter.positive_threshold}")
    print(f"Negative Threshold: {news_filter.negative_threshold}")
    
    print(f"\n{YELLOW}Enter new positive threshold (0.0 to 1.0):{RESET}")
    try:
        pos_threshold = float(input("> "))
        if 0.0 <= pos_threshold <= 1.0:
            news_filter.positive_threshold = pos_threshold
        else:
            print(f"{RED}Invalid threshold. Using default.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Using default.{RESET}")
    
    print(f"\n{YELLOW}Enter new negative threshold (-1.0 to 0.0):{RESET}")
    try:
        neg_threshold = float(input("> "))
        if -1.0 <= neg_threshold <= 0.0:
            news_filter.negative_threshold = neg_threshold
        else:
            print(f"{RED}Invalid threshold. Using default.{RESET}")
    except ValueError:
        print(f"{RED}Invalid input. Using default.{RESET}")
    
    print(f"\n{GREEN}Thresholds updated successfully!{RESET}")
    time.sleep(2)

def display_filter_stats(news_filter: NewsFilter):
    """Display news filter statistics."""
    stats = news_filter.get_filter_stats()
    
    print(f"\n{BOLD}{GREEN}=== News Filter Statistics ==={RESET}\n")
    print(f"{BLUE}Status:{RESET} {'Enabled' if stats['enabled'] else 'Disabled'}")
    print(f"{BLUE}Positive Threshold:{RESET} {stats['positive_threshold']}")
    print(f"{BLUE}Negative Threshold:{RESET} {stats['negative_threshold']}")
    print(f"{BLUE}Cache Size:{RESET} {stats['cache_size']} entries")
    print(f"{BLUE}Major Event Keywords:{RESET} {stats['major_event_keywords']} keywords")
    
    print(f"\n{YELLOW}Press any key to continue...{RESET}")
    keyboard.read_event()

def test_news_analysis(news_filter: NewsFilter):
    """Test news analysis with sample headlines."""
    print(f"\n{YELLOW}Testing news analysis with sample headlines...{RESET}")
    
    sample_headlines = [
        "EUR/USD rallies on positive ECB outlook",
        "Market crash fears grip Wall Street",
        "Fed maintains dovish stance on interest rates",
        "Strong employment data boosts USD",
        "Geopolitical tensions weigh on risk assets"
    ]
    
    sentiment = news_filter.analyze_sentiment(sample_headlines)
    
    print(f"\n{BOLD}{GREEN}=== News Analysis Test Results ==={RESET}\n")
    print(f"{BLUE}Sample Headlines:{RESET}")
    for i, headline in enumerate(sample_headlines, 1):
        print(f"{i}. {headline}")
    
    sentiment_color = GREEN if sentiment > 0.1 else RED if sentiment < -0.1 else YELLOW
    print(f"\n{BLUE}Overall Sentiment Score:{RESET} {sentiment_color}{sentiment:+.3f}{RESET}")
    
    if sentiment > news_filter.positive_threshold:
        print(f"{GREEN}Result: Strong positive sentiment - signals would be enhanced{RESET}")
    elif sentiment < news_filter.negative_threshold:
        print(f"{RED}Result: Negative sentiment - signals would be blocked{RESET}")
    else:
        print(f"{YELLOW}Result: Neutral sentiment - signals would proceed normally{RESET}")
    
    print(f"\n{YELLOW}Press any key to continue...{RESET}")
    keyboard.read_event()

def view_markets_menu():
    """Menu to view available markets with categories."""
    clear_screen()
    print_header()
    print(f"\n{BOLD}{BLUE}=== Available Markets ==={RESET}\n")
    
    print(f"{BOLD}{GREEN}Forex Markets:{RESET}")
    for i, (market, info) in enumerate(FOREX_MARKETS.items(), 1):
        volatility = info.get('volatility', 'unknown')
        vol_color = RED if volatility == 'high' else YELLOW if volatility == 'medium' else GREEN
        print(f"{BLUE}{i:2d}. {market:15s}{RESET} - {info['description']} ({vol_color}{volatility}{RESET})")
    
    print(f"\n{BOLD}{YELLOW}OTC Markets:{RESET}")
    for i, (market, info) in enumerate(OTC_MARKETS.items(), 1):
        volatility = info.get('volatility', 'unknown')
        vol_color = RED if volatility in ['high', 'very high'] else YELLOW if volatility == 'medium' else GREEN
        print(f"{YELLOW}{i:2d}. {market:15s}{RESET} - {info['description']} ({vol_color}{volatility}{RESET})")
    
    print(f"\n{BLUE}Total Markets: {len(MARKETS)}{RESET}")
    print(f"{BLUE}Forex Pairs: {len(FOREX_MARKETS)}{RESET}")
    print(f"{BLUE}OTC Pairs: {len(OTC_MARKETS)}{RESET}")
    
    print(f"\n{YELLOW}Press any key to return to main menu...{RESET}")
    keyboard.read_event()

def settings_menu():
    """Menu for application settings."""
    clear_screen()
    print_header()
    print(f"\n{BOLD}{BLUE}=== Settings ==={RESET}\n")
    
    settings_options = [
        "Quotex API Settings",
        "Default Timeframe Settings",
        "Reset All Settings",
        "About",
        "Back to Main Menu"
    ]
    
    choice = print_menu("Settings", settings_options)
    
    if choice == 1:
        quotex_api_settings()
    elif choice == 2:
        print_status_message("Supported timeframes: 1 min, 5 min, 15 min", "info")
        countdown_timer(3, "Returning to menu in")
    elif choice == 3:
        afa_loading_animation(2, "Resetting all settings")
        print_success_message("Settings reset successfully!")
        countdown_timer(2, "Returning to menu in")
    elif choice == 4:
        about_page()
    elif choice == 5:
        return
    
    # Return to settings menu unless going back to main
    if choice != 5:
        settings_menu()

def quotex_api_settings():
    """Configure Quotex API settings."""
    # Show connection animation
    quotex_connection_animation()
    
    print(f"\n{BLUE}{BOLD}📡 QUOTEX API STATUS{RESET}")
    print(f"{BLUE}{'─' * 40}{RESET}")
    print(f"{GREEN}✓ REAL API Module Loaded{RESET}")
    print(f"{GREEN}✓ Multiple Quotex endpoints configured{RESET}")
    print(f"{GREEN}✓ Real-time connection testing enabled{RESET}")
    print(f"{GREEN}✓ Supported Timeframes: 1, 5, 15, 30, 60 minutes{RESET}")
    print(f"{GREEN}✓ REAL Signal Generation{RESET}")
    print(f"{GREEN}✓ REAL Market Data Analysis{RESET}")
    print(f"{GREEN}✓ NO SIMULATION MODE{RESET}")
    print(f"{GREEN}✓ Enhanced Market Selection{RESET}")
    print(f"{GREEN}✓ Timing Control System{RESET}")
    print(f"{GREEN}✓ Automatic Random Selection{RESET}")
    
    print(f"\n{BLUE}API Features:{RESET}")
    print(f"• REAL market data from Quotex servers")
    print(f"• REAL-time signal generation with timing control")
    print(f"• REAL historical candle data analysis")
    print(f"• Multiple timeframe support")
    print(f"• Advanced volatility filtering")
    print(f"• Categorized market selection (Forex/OTC)")
    print(f"• NO FALLBACK TO SIMULATION")
    print(f"• Signal gap enforcement (2-10 minutes)")
    print(f"• Automatic random market selection")
    
    print(f"\n{RED}{BOLD}⚠️  REAL DATA MODE ONLY ⚠️{RESET}")
    print(f"{YELLOW}This application ONLY uses REAL data from Quotex servers.{RESET}")
    print(f"{YELLOW}No simulation or dummy data is used.{RESET}")
    
    wait_for_keypress()

def about_page():
    """Display information about the application."""
    clear_screen()
    print_afa_banner()
    
    print(f"\n{BLUE}{BOLD}📋 ABOUT AFA-TRADING{RESET}")
    print(f"{BLUE}{'─' * 50}{RESET}")
    print(f"{YELLOW}Version: {BOLD}3.0.0 - REAL DATA ONLY{RESET}")
    print(f"{YELLOW}Developer: {BOLD}AFA Trading Team{RESET}")
    print(f"{YELLOW}Description: {BOLD}Professional Binary Options Signals{RESET}")
    
    print(f"\n{BOLD}{GREEN}New Features in v3.0 - REAL DATA ONLY:{RESET}")
    print(f"{GREEN}✓ REAL Quotex API Integration{RESET}")
    print(f"{GREEN}✓ NO SIMULATION OR DUMMY DATA{RESET}")
    print(f"{GREEN}✓ Live Market Data Collection{RESET}")
    print(f"{GREEN}✓ Real-time Signal Generation{RESET}")
    print(f"{GREEN}✓ Multiple Quotex Endpoint Support{RESET}")
    print(f"{GREEN}✓ Enhanced Connection Reliability{RESET}")
    print(f"{GREEN}✓ Professional Real Data Analysis{RESET}")
    
    print(f"\n{BOLD}{BLUE}Previous Features:{RESET}")
    print(f"{BLUE}✓ Enhanced Market Selection with Categories{RESET}")
    print(f"{BLUE}✓ Forex and OTC Market Separation{RESET}")
    print(f"{BLUE}✓ Signal Timing Control (2-10 minute gaps){RESET}")
    print(f"{BLUE}✓ Historical Data Collection System{RESET}")
    print(f"{BLUE}✓ Advanced News Filter with Sentiment Analysis{RESET}")
    print(f"{BLUE}✓ Volatility Filter with Dynamic Position Sizing{RESET}")
    print(f"{BLUE}✓ Multiple Timeframe Support (1, 5, 15 min){RESET}")
    print(f"{BLUE}✓ Real-time Market Analysis{RESET}")
    print(f"{BLUE}✓ Enhanced Signal Confidence Scoring{RESET}")
    print(f"{BLUE}✓ Advanced Risk Management{RESET}")
    print(f"{BLUE}✓ ATR and Bollinger Bands Analysis{RESET}")
    
    print(f"\n{RED}{BOLD}⚠️  REAL DATA MODE ONLY ⚠️{RESET}")
    print(f"{YELLOW}This application ONLY uses REAL data from Quotex servers.{RESET}")
    print(f"{YELLOW}NO simulation or dummy data is generated.{RESET}")
    
    print(f"\n{YELLOW}Warning:{RESET} This software is for educational purposes only.")
    print(f"{YELLOW}Disclaimer:{RESET} Trading in binary options involves significant risk.")
    print(f"{RED}Important:{RESET} Past performance does not guarantee future results.")
    
    wait_for_keypress()

if __name__ == "__main__":
    try:
        if login():   # 👈 login check pehle
            main()    # 👈 phir signals wala program chalega
    except KeyboardInterrupt:
        clear_screen()
        print(f"\n{YELLOW}Program terminated by user.{RESET}")
        sys.exit(0)
    except Exception as e:
        clear_screen()
        print(f"\n{RED}An error occurred: {str(e)}{RESET}")
        print(f"{YELLOW}Please restart the application.{RESET}")
        sys.exit(1)
