import random
import curses


class RoomBase:
    def __init__(self, game):
        self.height = random.randint(10, game.map_height)
        self.width = random.randint(10, game.map_width)
        self.was_entered = False
        self.exit = None
        self.game = game
        self.tiles = self.generate()
        self.create_exit()

    def generate(self):
        raise NotImplementedError("generate method must be implemented in subclass")

    def create_exit(self):
        return None

    def position_player(self, player):
        if self.exit:
            player.x, player.y = self.exit
        else:
            player.x, player.y = self.width // 2, self.height // 2

    @property
    def name(self):
        raise NotImplementedError("generate method must be implemented in subclass")

    @property
    def offset_x(self):
        return (self.game.map_width - self.width) // 2

    @property
    def offset_y(self):
        return (self.game.map_height - self.height) // 2

    def is_walkable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x] in (
                self.game.TILES["rumble"],
                self.game.TILES["hallway"],
                self.game.TILES["floor"],
                self.game.TILES["door"],
            )
        return False

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

        if self.exit:
            x, y = self.exit
            stdscr.addch(
                y + self.offset_y,
                x + self.offset_x,
                "+",
                curses.color_pair(3),
            )
