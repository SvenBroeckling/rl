import curses


class StatusLine:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.default_status = "q: Quit | i: Inventory | f: Target/Attack | hjkl: Move"
        self.status = self.default_status

    def set_status(self, status):
        self.status = status

    def reset_status(self):
        self.status = self.default_status

    def draw(self):
        self.stdscr.addstr(
            curses.LINES - 1,
            0,
            self.status,
            curses.color_pair(7) | curses.A_BOLD,
        )
