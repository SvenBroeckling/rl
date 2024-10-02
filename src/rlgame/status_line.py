import curses


class StatusLine:
    def __init__(self, game):
        self.default_status = "q: Quit | i: Inventory | f: Target/Attack | hjkl: Move | r: Reload | Arrow keys: Scroll log"
        self.status = self.default_status
        self.game = game

    def set_status(self, status):
        self.status = status

    def reset_status(self):
        self.status = self.default_status

    def draw(self):
        filled_status = self.status.ljust(curses.COLS - 1)
        self.game.stdscr.addstr(
            curses.LINES - 1,
            0,
            filled_status,
            curses.color_pair(7) | curses.A_REVERSE,
        )
