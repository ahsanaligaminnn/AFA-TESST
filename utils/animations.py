"""
Enhanced Animation utilities for AFA-TRADING terminal UI.
Professional animations with AFA-TRADING branding.
"""

import time
import sys
import random
from ui.colors import BLUE, GREEN, RED, YELLOW, RESET, BOLD, DIM

def afa_loading_animation(duration=3, message="Processing"):
    """
    AFA-TRADING branded loading animation.
    
    Args:
        duration (int): Duration in seconds
        message (str): Loading message
    """
    # AFA-TRADING animation frames
    frames = [
        "🔄 AFA",
        "⚡ AFA",
        "💎 AFA", 
        "🎯 AFA",
        "🚀 AFA",
        "⭐ AFA"
    ]
    
    end_time = time.time() + duration
    i = 0
    
    while time.time() < end_time:
        frame = frames[i % len(frames)]
        sys.stdout.write(f"\r{BLUE}{BOLD}{frame} TRADING{RESET} {YELLOW}► {message}...{RESET}")
        sys.stdout.flush()
        time.sleep(0.3)
        i += 1
    
    sys.stdout.write(f"\r{GREEN}{BOLD}✅ AFA TRADING{RESET} {GREEN}► {message} Complete!{' ' * 20}{RESET}\n")
    sys.stdout.flush()

def print_success_message(message):
    """Print success message with celebration."""
    print(f"\n{GREEN}{BOLD}{'='*60}{RESET}")
    print(f"{GREEN}{BOLD}🎉           SUCCESS!           🎉{RESET}")
    print(f"{GREEN}{BOLD}{'='*60}{RESET}")
    print(f"{GREEN}✅ {message}{RESET}")
    print(f"{GREEN}{BOLD}{'='*60}{RESET}\n")

def print_error_message(message):
    """Print error message with warning styling."""
    print(f"\n{RED}{BOLD}{'='*60}{RESET}")
    print(f"{RED}{BOLD}⚠️            ERROR            ⚠️{RESET}")
    print(f"{RED}{BOLD}{'='*60}{RESET}")
    print(f"{RED}❌ {message}{RESET}")
    print(f"{RED}{BOLD}{'='*60}{RESET}\n")

def wait_for_keypress(message="Press any key to continue..."):
    """
    Enhanced wait for keypress with AFA-TRADING styling.
    
    Args:
        message (str): Message to display
    """
    print(f"\n{YELLOW}{BOLD}⏳ {message}{RESET}")
    
    # Animated waiting indicator
    chars = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    
    try:
        import keyboard
        
        # Animate while waiting for keypress
        i = 0
        while True:
            sys.stdout.write(f"\r{BLUE}{chars[i % len(chars)]} Waiting for input...{RESET}")
            sys.stdout.flush()
            
            if keyboard.is_pressed('space') or keyboard.is_pressed('enter'):
                break
                
            time.sleep(0.1)
            i += 1
            
            # Timeout after 30 seconds
            if i > 300:
                break
        
        print(f"\r{GREEN}✅ Input received!{' ' * 20}{RESET}")
        
    except ImportError:
        # Fallback to input() if keyboard module not available
        input(f"{GREEN}► Press Enter to continue...{RESET}")

def print_afa_banner():
    """Print AFA-TRADING banner for special occasions."""
    banner = f"""
{BLUE}{BOLD}
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║      █▀▀█ █▀▀ █▀▀█   ▀▀█▀▀ █▀▀█ █▀▀█ █▀▀▄ ─▀─ █▀▀▄    ║
    ║      █▄▄█ █▀▀ █▄▄█   ──█── █▄▄▀ █▄▄█ █──█ ▀█▀ █──█    ║
    ║      ▀──▀ ▀── ▀──▀   ──▀── ▀─▀▀ ▀──▀ ▀──▀ ▀▀▀ ▀──▀    ║
    ║                                                          ║
    ║           🎯 PROFESSIONAL TRADING SIGNALS 🎯            ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
{RESET}
    """
    print(banner)
def quotex_connection_animation():
    """Professional Quotex connection animation."""
    steps = [
        ("🔍", "Scanning Quotex endpoints"),
        ("🔗", "Establishing connection"),
        ("🔐", "Authenticating session"),
        ("📡", "Syncing market data"),
        ("✅", "Connection established")
    ]
    
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}           AFA-TRADING QUOTEX CONNECTION{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}\n")
    
    for icon, step in steps:
        sys.stdout.write(f"{YELLOW}{icon} {step}...")
        sys.stdout.flush()
        
        # Animated dots
        for _ in range(3):
            time.sleep(0.5)
            sys.stdout.write(".")
            sys.stdout.flush()
        
        print(f" {GREEN}✓{RESET}")
        time.sleep(0.3)
    
    print(f"\n{GREEN}{BOLD}🎉 QUOTEX CONNECTION SUCCESSFUL!{RESET}")
    print(f"{BLUE}Ready for live trading signals...{RESET}\n")

def signal_generation_animation(market, num_signals):
    """
    Professional signal generation animation.
    
    Args:
        market (str): Market name
        num_signals (int): Number of signals to generate
    """
    print(f"\n{BLUE}{BOLD}{'='*60}{RESET}")
    print(f"{BLUE}{BOLD}        AFA-TRADING SIGNAL GENERATOR{RESET}")
    print(f"{BLUE}{BOLD}{'='*60}{RESET}")
    
    print(f"\n{YELLOW}📊 Market: {BOLD}{market}{RESET}")
    print(f"{YELLOW}🎯 Signals: {BOLD}{num_signals}{RESET}")
    print(f"{YELLOW}⚡ Mode: {BOLD}REAL QUOTEX DATA{RESET}\n")
    
    # Signal generation steps
    steps = [
        ("📈", "Fetching live market data"),
        ("🧠", "Analyzing price patterns"),
        ("📊", "Calculating indicators"),
        ("🎯", "Generating signals"),
        ("✨", "Applying filters")
    ]
    
    for icon, step in steps:
        sys.stdout.write(f"{BLUE}{icon} {step}")
        sys.stdout.flush()
        
        # Progress dots with random timing
        dots = random.randint(3, 6)
        for _ in range(dots):
            time.sleep(random.uniform(0.2, 0.5))
            sys.stdout.write(f"{YELLOW}.{RESET}")
            sys.stdout.flush()
        
        print(f" {GREEN}✓{RESET}")
    
    print(f"\n{GREEN}{BOLD}🚀 SIGNAL GENERATION COMPLETE!{RESET}\n")

def market_analysis_animation(market):
    """
    Market analysis animation with technical indicators.
    
    Args:
        market (str): Market being analyzed
    """
    print(f"\n{BLUE}{BOLD}{'='*50}{RESET}")
    print(f"{BLUE}{BOLD}    AFA-TRADING MARKET ANALYSIS{RESET}")
    print(f"{BLUE}{BOLD}{'='*50}{RESET}")
    
    print(f"\n{YELLOW}🔍 Analyzing: {BOLD}{market}{RESET}\n")
    
    indicators = [
        ("📊", "RSI Analysis", "Relative Strength Index"),
        ("📈", "MACD Calculation", "Moving Average Convergence"),
        ("🎯", "Bollinger Bands", "Volatility Analysis"),
        ("⚡", "ATR Measurement", "Average True Range"),
        ("🧠", "Trend Detection", "Market Direction"),
        ("💎", "Support/Resistance", "Key Levels")
    ]
    
    for icon, name, description in indicators:
        sys.stdout.write(f"{BLUE}{icon} {name:<20}")
        sys.stdout.flush()
        
        # Animated progress bar
        bar_length = 20
        for i in range(bar_length + 1):
            progress = i / bar_length
            filled = int(progress * bar_length)
            bar = f"[{'█' * filled}{'░' * (bar_length - filled)}]"
            
            sys.stdout.write(f"\r{BLUE}{icon} {name:<20} {GREEN}{bar}{RESET} {int(progress * 100):3d}%")
            sys.stdout.flush()
            time.sleep(0.1)
        
        print(f" {GREEN}✓ {description}{RESET}")
    
    print(f"\n{GREEN}{BOLD}📊 ANALYSIS COMPLETE!{RESET}\n")

def afa_progress_bar(current, total, prefix='AFA Progress', width=40):
    """
    AFA-TRADING branded progress bar.
    
    Args:
        current (int): Current progress
        total (int): Total items
        prefix (str): Progress prefix
        width (int): Bar width
    """
    percent = (current / total) * 100
    filled = int(width * current // total)
    
    # AFA-TRADING style bar
    bar = f"{'█' * filled}{'░' * (width - filled)}"
    
    # Color based on progress
    if percent < 30:
        color = RED
    elif percent < 70:
        color = YELLOW
    else:
        color = GREEN
    
    sys.stdout.write(f"\r{BLUE}{BOLD}🎯 {prefix}:{RESET} {color}[{bar}]{RESET} {percent:6.1f}% ({current}/{total})")
    sys.stdout.flush()
    
    if current == total:
        print(f" {GREEN}{BOLD}✅ COMPLETE!{RESET}")

def typing_effect(text, delay=0.03, color=BLUE):
    """
    Typing effect animation for text.
    
    Args:
        text (str): Text to type
        delay (float): Delay between characters
        color (str): Text color
    """
    for char in text:
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()

def afa_startup_animation():
    """AFA-TRADING startup animation sequence."""
    # Clear screen
    import os
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # AFA-TRADING ASCII Art with animation
    logo_lines = [
        "    ╔══════════════════════════════════════════════════════════╗",
        "    ║                                                          ║",
        "    ║      █▀▀█ █▀▀ █▀▀█   ▀▀█▀▀ █▀▀█ █▀▀█ █▀▀▄ ─▀─ █▀▀▄    ║",
        "    ║      █▄▄█ █▀▀ █▄▄█   ──█── █▄▄▀ █▄▄█ █──█ ▀█▀ █──█    ║",
        "    ║      ▀──▀ ▀── ▀──▀   ──▀── ▀─▀▀ ▀──▀ ▀──▀ ▀▀▀ ▀──▀    ║",
        "    ║                                                          ║",
        "    ║      █▀▀ ─▀─ █▀▀▀ █▀▀▄ █▀▀█ █── █▀▀ █▀▀                ║",
        "    ║      ▀▀█ ▀█▀ █─▀█ █──█ █▄▄█ █── ▀▀█ ▀▀█                ║",
        "    ║      ▀▀▀ ▀▀▀ ▀▀▀▀ ▀──▀ ▀──▀ ▀▀▀ ▀▀▀ ▀▀▀                ║",
        "    ║                                                          ║",
        "    ╚══════════════════════════════════════════════════════════╝"
    ]
    
    # Animate logo appearance
    for line in logo_lines:
        print(f"{BLUE}{BOLD}{line}{RESET}")
        time.sleep(0.2)
    
    # Animated title
    print(f"\n{YELLOW}{BOLD}", end="")
    typing_effect("      PROFESSIONAL BINARY OPTIONS SIGNALS GENERATOR v3.0", 0.05, YELLOW + BOLD)
    
    # Loading sequence
    print(f"\n{BLUE}Initializing AFA-TRADING System...")
    
    components = [
        "🔧 Loading core modules",
        "📊 Initializing market data",
        "🎯 Setting up signal engine",
        "🔗 Connecting to Quotex API",
        "⚡ Activating real-time feeds",
        "✨ System ready!"
    ]
    
    for component in components:
        sys.stdout.write(f"{YELLOW}{component}")
        sys.stdout.flush()
        
        # Animated dots
        for _ in range(3):
            time.sleep(0.3)
            sys.stdout.write(".")
            sys.stdout.flush()
        
        print(f" {GREEN}✓{RESET}")
        time.sleep(0.2)
    
    print(f"\n{GREEN}{BOLD}🚀 AFA-TRADING SYSTEM ONLINE!{RESET}")
    print(f"{BLUE}Ready to generate professional trading signals...{RESET}\n")
    
    time.sleep(1)

def signal_display_animation(signals):
    """
    Animated signal display with professional formatting.
    
    Args:
        signals (list): List of signals to display
    """
    print(f"\n{BLUE}{BOLD}{'='*70}{RESET}")
    print(f"{BLUE}{BOLD}              AFA-TRADING LIVE SIGNALS{RESET}")
    print(f"{BLUE}{BOLD}{'='*70}{RESET}\n")
    
    for i, signal in enumerate(signals, 1):
        # Signal header with animation
        signal_color = GREEN if signal.signal_type == "BUY" else RED
        
        print(f"{BLUE}┌{'─' * 66}┐{RESET}")
        
        # Animated signal appearance
        sys.stdout.write(f"{BLUE}│{RESET}")
        time.sleep(0.1)
        
        typing_effect(f" 🎯 SIGNAL #{i:02d} │ {signal.signal_type:4s} │ {signal.time} │ {signal.market:12s} ", 0.02, signal_color + BOLD)
        
        print(f"{BLUE}├{'─' * 66}┤{RESET}")
        
        # Signal details
        confidence_color = GREEN if signal.confidence > 0.85 else YELLOW if signal.confidence > 0.75 else RED
        
        print(f"{BLUE}│{RESET} Confidence: {confidence_color}{int(signal.confidence * 100):3d}%{RESET} │ Strength: {signal.strength:12s} │ Real Data: ✅ {BLUE}│{RESET}")
        
        # Filters info if available
        if hasattr(signal, 'news_filter_result') and signal.news_filter_result:
            news_status = signal.news_filter_result.get('filter_result', 'unknown')
            print(f"{BLUE}│{RESET} News Filter: {news_status:20s} │ Volatility: Active      {BLUE}│{RESET}")
        
        print(f"{BLUE}└{'─' * 66}┘{RESET}\n")
        
        time.sleep(0.3)  # Pause between signals

def countdown_timer(seconds, message="Next signal in"):
    """
    Animated countdown timer.
    
    Args:
        seconds (int): Countdown duration
        message (str): Countdown message
    """
    for i in range(seconds, 0, -1):
        mins, secs = divmod(i, 60)
        timer = f"{mins:02d}:{secs:02d}"
        
        color = RED if i <= 10 else YELLOW if i <= 30 else GREEN
        
        sys.stdout.write(f"\r{BLUE}{message}: {color}{BOLD}{timer}{RESET}")
        sys.stdout.flush()
        time.sleep(1)
    
    print(f"\r{GREEN}{BOLD}🚀 Ready to proceed!{' ' * 30}{RESET}")

def matrix_rain_effect(duration=3):
    """
    Matrix-style rain effect for dramatic moments.
    
    Args:
        duration (int): Effect duration in seconds
    """
    import os
    width = os.get_terminal_size().columns
    height = 10
    
    chars = "AFA0123456789TRADING$€¥£"
    
    end_time = time.time() + duration
    
    while time.time() < end_time:
        # Clear previous frame
        print("\033[H\033[J", end="")
        
        for _ in range(height):
            line = ""
            for _ in range(width // 2):
                if random.random() < 0.1:
                    char = random.choice(chars)
                    color = random.choice([GREEN, BLUE, YELLOW])
                    line += f"{color}{char}{RESET}"
                else:
                    line += " "
            print(line)
        
        time.sleep(0.1)
    
    # Clear screen after effect
    print("\033[H\033[J", end="")

def success_celebration():
    """Success celebration animation."""
    celebration_frames = [
        "🎉 SUCCESS! 🎉",
        "✨ SUCCESS! ✨", 
        "🚀 SUCCESS! 🚀",
        "⭐ SUCCESS! ⭐",
        "💎 SUCCESS! 💎"
    ]
    
    for _ in range(3):  # Repeat 3 times
        for frame in celebration_frames:
            sys.stdout.write(f"\r{GREEN}{BOLD}{frame:^30}{RESET}")
            sys.stdout.flush()
            time.sleep(0.3)
    
    print(f"\n{GREEN}{BOLD}🎯 AFA-TRADING SIGNALS GENERATED SUCCESSFULLY!{RESET}")

def error_animation(error_msg):
    """
    Error display animation.
    
    Args:
        error_msg (str): Error message to display
    """
    print(f"\n{RED}{BOLD}{'='*50}{RESET}")
    print(f"{RED}{BOLD}           ⚠️  ERROR DETECTED  ⚠️{RESET}")
    print(f"{RED}{BOLD}{'='*50}{RESET}")
    
    # Blinking error message
    for _ in range(3):
        sys.stdout.write(f"\r{RED}{BOLD}❌ {error_msg}{RESET}")
        sys.stdout.flush()
        time.sleep(0.5)
        sys.stdout.write(f"\r{' ' * (len(error_msg) + 5)}")
        sys.stdout.flush()
        time.sleep(0.3)
    
    print(f"\r{RED}{BOLD}❌ {error_msg}{RESET}")
    print(f"{YELLOW}🔧 AFA-TRADING will attempt to recover...{RESET}\n")

def menu_transition_animation():
    """Smooth menu transition animation."""
    # Sliding effect
    for i in range(5):
        sys.stdout.write(f"\r{BLUE}{'█' * (i * 10)}{' ' * (50 - i * 10)}{RESET}")
        sys.stdout.flush()
        time.sleep(0.1)
    
    print(f"\r{GREEN}{'█' * 50}{RESET}")
    time.sleep(0.2)
    
    # Clear the bar
    print(f"\r{' ' * 50}")