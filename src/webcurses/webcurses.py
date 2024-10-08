from .constants import HTML_COLOR_CLASSES


def html_color_class_name_to_hex(color_class_name):
    """Convert an HTML color class name to a hex color code."""
    if color_class_name.startswith("rgb-"):
        _, r, g, b = color_class_name.split("-")
        r = int(r)
        g = int(g)
        b = int(b)
        r = (r * 51) // 255
        g = (g * 51) // 255
        b = (b * 51) // 255
        return f"#{r:02x}{g:02x}{b:02x}"
    elif color_class_name.startswith("gray-"):
        gray = int(color_class_name.split("-")[1])
        gray = (gray * 255) // 100
        return f"#{gray:02x}{gray:02x}{gray:02x}"
    elif color_class_name.startswith("bright-"):
        return html_color_class_name_to_hex(color_class_name[7:])
    else:
        return color_class_name


def curses_color_pair_to_html_color_pair(curses_color_pair):
    """Convert a curses color pair to an HTML color pair."""
    fg, bg = curses_color_pair
    fg = html_color_class_name_to_hex(HTML_COLOR_CLASSES[fg])
    bg = html_color_class_name_to_hex(HTML_COLOR_CLASSES[bg])
    return fg, bg


class Window:
    pass


class Screen:
    def __init__(self, thread, web_curses):
        self.thread = thread
        self.web_curses = web_curses

    def getmaxyx(self):
        return self.web_curses.getmaxyx()

    @property
    def height(self):
        return self.web_curses.getmaxyx()[0]

    @property
    def width(self):
        return self.web_curses.getmaxyx()[1]

    def refresh(self):
        if self.web_curses.screen_update_callback:
            self.web_curses.screen_update_callback(
                self.web_curses.get_screen_as_string()
            )

    def addstr(self, y, x, string, color=None):
        """Add a string to the screen at a given position with optional color."""
        if color is None:
            color = self.web_curses.current_color_pair
        for i, char in enumerate(string):
            if 0 <= x + i < self.width and 0 <= y < self.height:
                self.web_curses.screen[y][x + i] = (char, color)

    def addch(self, y, x, ch, color=None):
        """Add a single character to the screen at a given position."""
        if color is None:
            color = self.web_curses.current_color_pair
        if 0 <= x < self.width and 0 <= y < self.height:
            if color is None:
                color = self.web_curses.current_color_pair
            self.web_curses.screen[y][x] = (ch, color)

    def clear(self):
        for y in range(self.web_curses.getmaxyx()[0]):
            for x in range(self.web_curses.getmaxyx()[1]):
                self.addch(y, x, " ")

    def getch(self):
        self.thread.key_event.wait()
        self.thread.key_event.clear()
        key = self.thread.key_queue.get()
        try:
            return ord(key)
        except TypeError:
            return key


class WebCurses:
    COLOR_BLACK = 0
    COLOR_RED = 1
    COLOR_GREEN = 2
    COLOR_YELLOW = 3
    COLOR_BLUE = 4
    COLOR_MAGENTA = 5
    COLOR_CYAN = 6
    COLOR_WHITE = 7
    A_REVERSE = 1
    A_BOLD = 2
    KEY_UP = 65
    KEY_DOWN = 66

    def __init__(self, thread, rows, columns, screen_update_callback=None):
        self.thread = thread
        self.width = columns
        self.height = rows
        self.screen_update_callback = screen_update_callback
        self.color_pairs = {}  # Maps pair_number to (fg, bg) colors
        self.colors_initialized = False
        self.current_color_pair = 0  # Default color pair
        self.init_screen()
        self.stdscr = Screen(thread, self)

    @property
    def COLS(self):
        return self.width

    @property
    def LINES(self):
        return self.height

    def start_color(self):
        """Enable color functionality."""
        self.colors_initialized = True

    def init_pair(self, pair_number, fg, bg):
        """Initialize a color pair with a foreground and background."""
        if self.colors_initialized:
            self.color_pairs[pair_number] = (fg, bg)

    def curs_set(self, visibility):
        pass

    def init_screen(self):
        self.screen = [
            [(" ", self.current_color_pair) for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def resize(self, width, height):
        """Resize the screen."""
        self.width = width
        self.height = height
        self.init_screen()

    def color_pair(self, pair_number):
        """Return the color pair attribute."""
        return pair_number if pair_number in self.color_pairs else 0

    def getmaxyx(self):
        """Return the current screen dimensions (height, width)."""
        return self.height, self.width

    def get_screen_as_string(self):
        """Return the screen as a single string with HTML span elements for colors."""
        result = []
        for row in self.screen:
            line = []
            for char, color_pair in row:
                fg, bg = curses_color_pair_to_html_color_pair(
                    self.color_pairs.get(color_pair, (7, 0))
                )
                span = (
                    f'<span style="color: {fg}; background-color: {bg};">{char}</span>'
                )
                line.append(span)
            result.append("".join(line))
        result = "<br>".join(result)
        if self.screen_update_callback:
            self.screen_update_callback(result)
        return result
