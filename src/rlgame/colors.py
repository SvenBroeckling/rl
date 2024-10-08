import curses
from . import curses_colors


class ColorBase:
    pair_number = 0
    foreground = curses_colors.COLOR_WHITE
    background = curses_colors.COLOR_BLACK

    def curses_init_pair(self):
        curses.init_pair(self.pair_number, self.foreground, self.background)


class PlayerColor(ColorBase):
    pair_number = 1
    foreground = curses_colors.COLOR_CYAN
    background = curses_colors.COLOR_BLACK


class EnemyColor(ColorBase):
    pair_number = 2
    foreground = curses_colors.COLOR_RED
    background = curses_colors.COLOR_BLACK


class ItemColor(ColorBase):
    pair_number = 3
    foreground = curses_colors.COLOR_YELLOW
    background = curses_colors.COLOR_BLACK


class WallColor(ColorBase):
    pair_number = 4
    foreground = curses_colors.COLOR_WHITE
    background = curses_colors.COLOR_BLACK


class DoorColor(ColorBase):
    pair_number = 5
    foreground = curses_colors.COLOR_CYAN
    background = curses_colors.COLOR_BLACK


class FloorColor(ColorBase):
    pair_number = 6
    foreground = curses_colors.COLOR_GRAY_88
    background = curses_colors.COLOR_BLACK


class OutsideSightColor(ColorBase):
    pair_number = 7
    foreground = curses_colors.COLOR_GRAY_68
    background = curses_colors.COLOR_BLACK


class UIColor(ColorBase):
    pair_number = 8
    foreground = curses_colors.COLOR_WHITE
    background = curses_colors.COLOR_BLACK
