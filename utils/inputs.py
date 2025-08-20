# utils/inputs.py
"""
Small cross-platform helper for waiting a single keypress.
Use: from utils.inputs import wait_for_keypress
"""

import sys
import os

def wait_for_keypress(prompt="Press any key to continue..."):
    """
    Wait for a single keypress. Works on Windows (msvcrt) and POSIX (tty/termios).
    Falls back to input() if anything fails.
    """
    try:
        # Windows
        if os.name == 'nt':
            try:
                import msvcrt
                print(prompt, end='', flush=True)
                msvcrt.getch()
                print()
                return
            except Exception:
                # fall through to input fallback
                pass

        # POSIX (Linux / mac / WSL)
        if hasattr(sys.stdin, "fileno"):
            try:
                import tty, termios
                fd = sys.stdin.fileno()
                old_settings = termios.tcgetattr(fd)
                try:
                    print(prompt, end='', flush=True)
                    tty.setraw(fd)
                    sys.stdin.read(1)
                    print()
                    return
                finally:
                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            except Exception:
                pass

    except Exception:
        # If something unexpected happens, we'll go to fallback below
        pass

    # Fallback: blocking input (works everywhere, just needs Enter)
    try:
        input(prompt)
    except Exception:
        # last resort: do nothing
        return
