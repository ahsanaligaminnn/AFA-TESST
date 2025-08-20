# utils/messages.py
"""
Central message helpers.
Put this file in a package folder named `utils` (create utils/__init__.py if needed).
"""

def _try_colorama():
    try:
        from colorama import Fore, Style
        return Fore, Style
    except Exception:
        return None, None

Fore, Style = _try_colorama()

def print_success_message(message):
    """Print a green success message if colorama exists, otherwise plain."""
    try:
        if Fore and Style:
            print(Fore.GREEN + "[SUCCESS] " + str(message) + Style.RESET_ALL)
        else:
            print("[SUCCESS] " + str(message))
    except Exception:
        print("[SUCCESS] " + str(message))

def print_error_message(message):
    """Print a red error message if colorama exists, otherwise plain."""
    try:
        if Fore and Style:
            print(Fore.RED + "[ERROR] " + str(message) + Style.RESET_ALL)
        else:
            print("[ERROR] " + str(message))
    except Exception:
        print("[ERROR] " + str(message))
