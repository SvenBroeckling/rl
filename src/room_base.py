import random


class RoomBase:
    def __init__(self, game):
        self.height = random.randint(10, game.map_height)
        self.width = random.randint(10, game.map_width)
        self.game = game
        self.tiles = self.generate()

    def generate(self):
        raise NotImplementedError("generate method must be implemented in subclass")

    @property
    def name(self):
        raise NotImplementedError("generate method must be implemented in subclass")

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
