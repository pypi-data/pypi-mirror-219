"""
Crateman logging facility.

- Change the value of file variable to any `TextTOWrapper` as a log output.
- Use `colors_enable()` or `colors_disable()` to do what you think they'll do.
- Use functions accepting a string to log them in a specific format.
"""

from sys import stdout

file = stdout


class Color:
    DEFAULT = 9
    BLACK   = 0
    RED     = 1
    GREEN   = 2
    YELLOW  = 3
    BLUE    = 4
    MAGENTA = 5
    CYAN    = 6
    WHITE   = 7
    LIGHT   = 60


class Style:
	BOLD      = 1
	REGULAR   = 10


def _set_color_no(fg: None | int = Color.DEFAULT,
                  bg: None | int = Color.DEFAULT,
                  style: None | int = Style.REGULAR) -> str:
    return ""


def _set_color_yes(fg: None | int = Color.DEFAULT,
                   bg: None | int = Color.DEFAULT,
                   style: None | int = Style.REGULAR) -> str:
    return f"\033[0;{40 + bg};{30 + fg};{style}m"


# Returns escape sequence for terminal to make it colorful
# Or returns "" when you disabled colors
set_color = _set_color_no


def _generate_mark(signature: str, fg: int) -> str:
    opening_bracket = f"{set_color(style=Style.BOLD)}["
    closing_bracket = f"{set_color(style=Style.BOLD)}]"
    signature = f"{set_color(style=Style.BOLD, fg=fg)}{signature}"
    regular = set_color()
    return opening_bracket + signature + closing_bracket + regular


class Mark:
    OK   = ""
    WARN = ""
    ERR  = ""
    DBG  = ""
    INFO = ""


def _generate_marks():
    Mark.OK   = _generate_mark('*', Color.GREEN)
    Mark.WARN = _generate_mark('!', Color.YELLOW)
    Mark.ERR  = _generate_mark('x', Color.RED)
    Mark.DBG  = _generate_mark('#', Color.CYAN)
    Mark.INFO = _generate_mark('i', Color.BLUE)

_generate_marks()


def colors_enable():
    global set_color
    set_color = _set_color_yes
    _generate_marks()


def colors_disable():
    global set_color
    set_color = _set_color_no
    _generate_marks()


def err(s: str):  file.write(f"{Mark.ERR} {s}\n")
def warn(s: str): file.write(f"{Mark.WARN} {s}\n")
def ok(s: str):   file.write(f"{Mark.OK} {s}\n")
def info(s: str): file.write(f"{Mark.INFO} {s}\n")
def dbg(s: str):  file.write(f"{Mark.DBG} {s}\n")
