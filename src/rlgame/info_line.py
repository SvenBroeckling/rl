import curses


class InfoLine:
    def __init__(self, game):
        self.game = game
        self.info = ""

    def set_info(self, info):
        self.info = info

    def draw(self):
        self.game.stdscr.addstr(
            self.game.screen_height - 7,
            0,
            self.info,
            curses.color_pair(7),
        )
