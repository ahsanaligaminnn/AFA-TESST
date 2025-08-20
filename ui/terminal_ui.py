import os
import sys
import time
from colorama import Fore, Back, Style

from ui.colors import RED, GREEN, YELLOW, BLUE, RESET, BOLD, DIM
from utils.animations import (
    afa_startup_animation, typing_effect, menu_transition_animation,
    afa_loading_animation
)

def clear_screen():
    """Clear the terminal screen with AFA-TRADING style."""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Add a subtle header after clearing
    print(f"{BLUE}{DIM}{'─' * 80}{RESET}")
    print(f"{BLUE}{DIM}                           AFA-TRADING SYSTEM                           {RESET}")
    print(f"{BLUE}{DIM}{'─' * 80}{RESET}\n")

def print_header():
    """Print the enhanced AFA-TRADING header with animations."""
    # Use the startup animation for first load
    afa_startup_animation()

def print_menu(title, options):
    """
    Print an enhanced menu with AFA-TRADING styling and animations.
    
    Args:
        title (str): The title of the menu
        options (list): A list of menu option strings
        
    Returns:
        int: The user's choice (1-based index)
    """
    # Menu transition animation
    menu_transition_animation()
    
    # Enhanced menu header
    print(f"\n{BLUE}{BOLD}╔{'═' * (len(title) + 4)}╗{RESET}")
    print(f"{BLUE}{BOLD}║  {title}  ║{RESET}")
    print(f"{BLUE}{BOLD}╚{'═' * (len(title) + 4)}╝{RESET}\n")
    
    # Animated menu options
    for i, option in enumerate(options, 1):
        # Add icons based on option type
        icon = get_menu_icon(option)
        
        # Typing effect for each option
        sys.stdout.write(f"{YELLOW}{BOLD}{i}.{RESET} {icon} ")
        typing_effect(option, 0.02, BLUE)
        time.sleep(0.1)
    
    return get_user_input(f"\n{GREEN}🎯 Enter your choice", 1, len(options))

def get_menu_icon(option):
    """Get appropriate icon for menu option."""
    if "Generate" in option or "Signal" in option:
        return "🎯"
    elif "Market" in option or "View" in option:
        return "📊"
    elif "Analysis" in option:
        return "📈"
    elif "Historical" in option:
        return "📋"
    elif "News" in option:
        return "📰"
    elif "Volatility" in option:
        return "⚡"
    elif "Timing" in option:
        return "⏰"
    elif "Settings" in option:
        return "⚙️"
    elif "Exit" in option:
        return "🚪"
    else:
        return "▶️"

def get_user_input(prompt, min_value, max_value):
    """
    Get validated integer input with enhanced AFA-TRADING styling.
    
    Args:
        prompt (str): The prompt message to display
        min_value (int): The minimum acceptable value
        max_value (int): The maximum acceptable value
        
    Returns:
        int: The validated user input
    """
    while True:
        try:
            print(f"{prompt} ({YELLOW}{min_value}-{max_value}{RESET}): ", end="")
            
            # Enhanced input with cursor
            sys.stdout.write(f"{GREEN}► {RESET}")
            sys.stdout.flush()
            
            value = int(input())
            
            if min_value <= value <= max_value:
                # Success animation
                print(f"{GREEN}✅ Valid input: {value}{RESET}")
                return value
            else:
                # Error animation
                print(f"{RED}❌ Error: Please enter a number between {min_value} and {max_value}.{RESET}")
                afa_loading_animation(1, "Retrying")
        except ValueError:
            print(f"{RED}❌ Error: Please enter a valid number.{RESET}")
            afa_loading_animation(1, "Retrying")
        except KeyboardInterrupt:
            print(f"\n{YELLOW}⚠️ Operation cancelled by user.{RESET}")
            return min_value

def print_progress_bar(iteration, total, prefix='AFA Progress', suffix='Complete', length=50):
    """
    Print an enhanced AFA-TRADING progress bar.
    
    Args:
        iteration (int): Current iteration
        total (int): Total iterations
        prefix (str): Prefix string
        suffix (str): Suffix string
        length (int): Character length of bar
    """
    percent = (iteration / total) * 100
    filled_length = int(length * iteration // total)
    
    # AFA-TRADING style progress bar
    bar = f"{'█' * filled_length}{'░' * (length - filled_length)}"
    
    # Dynamic color based on progress
    if percent < 30:
        color = RED
    elif percent < 70:
        color = YELLOW
    else:
        color = GREEN
    
    # Enhanced progress display
    sys.stdout.write(f'\r{BLUE}{BOLD}🎯 {prefix}:{RESET} {color}[{bar}]{RESET} {percent:6.1f}% {suffix}')
    sys.stdout.flush()
    
    if iteration == total:
        print(f" {GREEN}{BOLD}✅ COMPLETE!{RESET}")

def print_status_message(message, status_type="info"):
    """
    Print an enhanced status message with AFA-TRADING styling.
    
    Args:
        message (str): The message to display
        status_type (str): Type of status ('info', 'success', 'warning', 'error')
    """
    icons = {
        'info': '📋',
        'success': '✅',
        'warning': '⚠️',
        'error': '❌'
    }
    
    colors = {
        'info': BLUE,
        'success': GREEN,
        'warning': YELLOW,
        'error': RED
    }
    
    icon = icons.get(status_type, '📋')
    color = colors.get(status_type, BLUE)
    
    # Enhanced status message with border
    print(f"{color}┌{'─' * (len(message) + 10)}┐{RESET}")
    print(f"{color}│ {icon} {message:<{len(message) + 5}} │{RESET}")
    print(f"{color}└{'─' * (len(message) + 10)}┘{RESET}")

def print_table_header(headers):
    """
    Print an enhanced AFA-TRADING table header.
    
    Args:
        headers (list): List of header strings
    """
    # Calculate column widths
    col_width = 15
    total_width = len(headers) * col_width + len(headers) + 1
    
    # Top border
    print(f"{BLUE}┌{'─' * (total_width - 2)}┐{RESET}")
    
    # Header row
    header_line = "│"
    for header in headers:
        header_line += f"{BOLD}{BLUE}{header:^{col_width}}{RESET}│"
    print(header_line)
    
    # Separator
    print(f"{BLUE}├{'─' * (total_width - 2)}┤{RESET}")

def print_table_row(values, colors=None):
    """
    Print an enhanced AFA-TRADING table row.
    
    Args:
        values (list): List of values to display
        colors (list, optional): List of colors for each value
    """
    if colors is None:
        colors = [RESET] * len(values)
    
    col_width = 15
    row_line = "│"
    
    for value, color in zip(values, colors):
        row_line += f"{color}{str(value):^{col_width}}{RESET}│"
    
    print(row_line)

def print_table_footer(num_cols):
    """Print table footer."""
    col_width = 15
    total_width = num_cols * col_width + num_cols + 1
    print(f"{BLUE}└{'─' * (total_width - 2)}┘{RESET}")

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