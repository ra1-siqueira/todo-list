import re
import shutil
import unicodedata
import sys
import termios
import tty

#WIDTH  : int = shutil.get_terminal_size().columns # largura do terminal
GREY   : str = '\033[90m'
YELLOW : str = '\033[33m'
GREEN  : str = '\033[32m'
RESET  : str = '\033[0m'

def wait_key():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)   
    try:
        tty.setraw(fd)
        while True:
            if sys.stdin.read(1) in ('\r', '\n'):
                break
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

def visible(text: str) -> int:
    colorless = re.sub(r'\033\[[0-9;]*m', '', text)
    extras = sum(
        unicodedata.east_asian_width(c) in ('W', 'F')
        for c in colorless
    )
    return len(colorless) + extras

def centered(text: str, width: int = 0) -> str:
    width = shutil.get_terminal_size().columns
    space = max(width - visible(text), 0)
    return ' ' * (space // 2) + text

def color_text(text: str, color: str = GREY) -> str:
    return color + text + RESET
    
def clear_console() -> None:
    print('\033[3J\033[2J\033[H', end='', flush=True)
    
#def resize() -> int:
#   WIDTH = shutil.get_terminal_size().columns
