"""
Utilities for file operations.
"""

import os
import datetime

def save_signals_to_file(signals, market_name):
    """
    Save a list of signals to a text file.
    
    Args:
        signals (list): List of Signal objects to save
        market_name (str): Name of the market for filename
        
    Returns:
        str: The filename where signals were saved
    """
    # Create directory if it doesn't exist
    os.makedirs("signals", exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"signals/{market_name}_{timestamp}.txt"
    
    # Write signals to file
    with open(filename, "w") as f:
        f.write(f"Trading Signals for {market_name}\n")
        f.write(f"Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 50 + "\n\n")
        
        for signal in signals:
            f.write(f"{str(signal)}\n")
    
    return filename

def read_signals_from_file(filename):
    """
    Read signals from a file.
    
    Args:
        filename (str): Path to the signals file
        
    Returns:
        list: List of signal strings read from the file
    """
    if not os.path.exists(filename):
        return []
    
    signals = []
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("-") and ":" in line:
                signals.append(line)
    
    return signals