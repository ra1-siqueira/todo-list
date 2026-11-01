import re
import shutil
import unicodedata

WIDTH  : int = shutil.get_terminal_size().columns # largura do terminal
GREY   : str = '\033[90m'
YELLOW : str = '\033[33m'
GREEN  : str = '\033[32m'
RESET  : str = '\033[0m'

def visible(text: str) -> int:
    colorless = re.sub(r'\033\[[0-9;]*m', '', text)
    extras = sum(
        unicodedata.east_asian_width(c) in ('W', 'F')
        for c in colorless
    )
    return len(colorless) + extras

def centered(text: str, width: int = WIDTH) -> str:
    space = max(width - visible(text), 0)
    return ' ' * (space // 2) + text

def color_text(text: str, color: str = GREY) -> str:
    return color + text + RESET
