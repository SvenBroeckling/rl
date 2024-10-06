import curses
import random

from rlgame import curses_colors
from rlgame.tiles import WallTile, DoorTile


class RoomBase:
    def __init__(
        self, game, min_width=20, max_width=100, min_height=20, max_height=100
    ):
        self.height = random.randint(min_height, max_height)
        self.width = random.randint(min_width, max_width)
        self.was_entered = False
        self.exit = None
        self.game = game
        self.tiles = self.generator.generate_room()
        self.create_exit()

    @property
    def name(self):
        raise NotImplementedError("name method must be implemented in subclass")

    @property
    def generator(self):
        raise NotImplementedError("generator method must be implemented in subclass")

    def create_exit(self):
        return None

    def position_player(self, player):
        if self.exit:
            player.x, player.y = self.exit
        else:
            player.x, player.y = self.width // 2, self.height // 2

    def is_walkable(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x].is_walkable
        return False

    def get_map_position_in_viewport(self, map_x, map_y) -> tuple | None:
        """Convert map coordinates to viewport coordinates. Return None if the map position is not in the viewport."""
        player = self.game.player
        viewport_width = self.game.viewport_width
        viewport_height = self.game.viewport_height
        offset_x = player.x - viewport_width // 2
        offset_y = player.y - viewport_height // 2

        x = map_x - offset_x
        y = map_y - offset_y

        if 0 <= y < viewport_height and 0 <= x < viewport_width:
            return x, y
        return None

    def draw_map(self, player):
        """Draw the map around the player in the viewport."""
        viewport_width = self.game.viewport_width
        viewport_height = self.game.viewport_height
        offset_x = player.x - viewport_width // 2
        offset_y = player.y - viewport_height // 2

        for y in range(viewport_height):
            for x in range(viewport_width):
                if 0 <= y + offset_y < self.height and 0 <= x + offset_x < self.width:
                    tile = self.tiles[y + offset_y][x + offset_x]
                else:
                    tile = WallTile(self.game)

                if self.game.player.is_in_view_distance(x + offset_x, y + offset_y):
                    tile.is_discovered = True
                    self.game.stdscr.addch(y, x, tile.char, tile.color | curses.A_BOLD)
                else:
                    if tile.is_discovered:
                        self.game.stdscr.addch(y, x, tile.char, tile.color)
                    else:
                        self.game.stdscr.addch(y, x, " ", curses_colors.COLOR_GRAY_118)

    def draw(self, stdscr):
        self.draw_map(self.game.player)

        if self.exit:
            if pos := self.get_map_position_in_viewport(*self.exit):
                x, y = pos
                door_tile = DoorTile(self.game)
                stdscr.addch(
                    y,
                    x,
                    door_tile.char,
                    door_tile.color,
                )
