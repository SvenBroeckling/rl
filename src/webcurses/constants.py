import _curses

HTML_COLOR_CLASSES = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
]

# Bright colors

HTML_COLOR_CLASSES += [f"bright-{color}" for color in HTML_COLOR_CLASSES]

# Extended 6x6x6 cube colors (R, G, B values)
# Algorithm to calculate the color code:
# 16 + 36 * R + 6 * G + B
# where R, G, B are in [0, 5]

HTML_COLOR_CLASSES += [
    f"rgb-{r}-{g}-{b}" for r in range(6) for g in range(6) for b in range(6)
]

# Grayscale colors
HTML_COLOR_CLASSES += [f"gray-{i}" for i in range(8, 238, 10)]

KEY_MAP = {
    # Arrow Keys
    "ArrowUp": _curses.KEY_UP,
    "ArrowDown": _curses.KEY_DOWN,
    "ArrowLeft": _curses.KEY_LEFT,
    "ArrowRight": _curses.KEY_RIGHT,
    # Function Keys
    "F1": _curses.KEY_F1,
    "F2": _curses.KEY_F2,
    "F3": _curses.KEY_F3,
    "F4": _curses.KEY_F4,
    "F5": _curses.KEY_F5,
    "F6": _curses.KEY_F6,
    "F7": _curses.KEY_F7,
    "F8": _curses.KEY_F8,
    "F9": _curses.KEY_F9,
    "F10": _curses.KEY_F10,
    "F11": _curses.KEY_F11,
    "F12": _curses.KEY_F12,
    # Control Keys
    "Backspace": _curses.KEY_BACKSPACE,
    "Enter": 10,  # ASCII value of Enter
    "Escape": 27,  # ASCII value of ESC
    "Tab": 9,  # ASCII value of Tab
    "Delete": _curses.KEY_DC,  # Delete key
    "Insert": _curses.KEY_IC,  # Insert key
    "Home": _curses.KEY_HOME,
    "End": _curses.KEY_END,
    "PageUp": _curses.KEY_PPAGE,  # Page Up
    "PageDown": _curses.KEY_NPAGE,  # Page Down
    # Miscellaneous Keys
    "Pause": _curses.KEY_BREAK,
    "PrintScreen": _curses.KEY_PRINT,
    "Space": ord(" "),  # ASCII value of space bar
    "Clear": _curses.KEY_CLEAR,
    # Numeric Keypad (mapped to ASCII codes)
    "Numpad0": ord("0"),
    "Numpad1": ord("1"),
    "Numpad2": ord("2"),
    "Numpad3": ord("3"),
    "Numpad4": ord("4"),
    "Numpad5": ord("5"),
    "Numpad6": ord("6"),
    "Numpad7": ord("7"),
    "Numpad8": ord("8"),
    "Numpad9": ord("9"),
    "NumpadEnter": 10,  # Enter key on the keypad
}
