import curses
import random

from tiles import TILES


class Hallway:
    def __init__(self, map_width, map_height, game):
        self.width = random.randint(10, map_width)
        self.height = random.randint(10, map_height)
        self.name = "Hallway"
        self.game = game
        self.tiles = self.generate()

    def generate(self):
        return [
            [TILES["hallway"] for x in range(self.width)] for y in range(self.height)
        ]

    @property
    def offset_x(self):
        return (self.game.map_width - self.width) // 2

    @property
    def offset_y(self):
        return (self.game.map_height - self.height) // 2

    def draw(self, stdscr):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                stdscr.addch(y + self.offset_y, x + self.offset_x, tile)

        for y in range(self.height):
            stdscr.addch(y + self.offset_y, self.offset_x, "|")
            stdscr.addch(y + self.offset_y, self.width - 1 + self.offset_x, "|")
        for x in range(self.width):
            stdscr.addch(self.offset_y, x + self.offset_x, "-")
            stdscr.addch(self.height - 1 + self.offset_y, x + self.offset_x, "-")

        self.draw_room_entries()

    def draw_room_entries(self):
        for room in self.game.available_rooms:
            x, y = room.hallway_entry
            self.game.stdscr.addch(
                y + self.offset_y,
                x + self.offset_x,
                TILES["door"],
                curses.color_pair(3),
            )
