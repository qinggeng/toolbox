import contextlib
import contextlib

class colors:
    # 标准前景色
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    RESET = '\033[39m'
    
    # 标准背景色
    B_BLACK = '\033[40m'
    B_RED = '\033[41m'
    B_GREEN = '\033[42m'
    B_YELLOW = '\033[43m'
    B_BLUE = '\033[44m'
    B_MAGENTA = '\033[45m'
    B_CYAN = '\033[46m'
    B_WHITE = '\033[47m'
    B_RESET = '\033[49m'

@contextlib.contextmanager
def colored_output(fg_color=None, bg_color=None):
    original_fg = '\033[39m'
    original_bg = '\033[49m'

    if fg_color and fg_color in vars(colors):
        original_fg = vars(colors)[fg_color]
    if bg_color and bg_color in vars(colors):
        original_bg = vars(colors)[bg_color]

    print(original_fg + original_bg, end='')
    try:
        yield
    finally:
        print('\033[0m', end='')
