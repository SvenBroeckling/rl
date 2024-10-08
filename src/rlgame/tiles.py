import random

from rlgame.colors import WallColor, DoorColor, FloorColor


class TileBase:
    def __init__(self, game):
        self.game = game
        self.name = "Tile"
        self.chars = [" "]
        self.chars_emoji = [" "]
        self.provides_cover = False
        self.is_walkable = False
        self.is_discovered = False
        self.breaks_line_of_sight = False
        self.color = None

    @property
    def char(self):
        return random.choice(self.chars)


class EmptyTile(TileBase):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Empty"
        self.is_walkable = True
        self.breaks_line_of_sight = False
        self.chars = [" "]
        self.chars_emoji = [" "]
        self.color = FloorColor.pair_number


class WallTile(TileBase):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Wall"
        self.is_walkable = False
        self.breaks_line_of_sight = True
        self.provides_cover = True
        self.chars = ["#"]
        self.chars_emoji = ["#"]
        self.color = WallColor.pair_number


class FloorTile(TileBase):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Floor"
        self.is_walkable = True
        self.breaks_line_of_sight = False
        self.is_rumble = random.choice([True, False, False, False, False])
        self.chars = ["·", ","]
        self.chars_emoji = [".", ","]
        self.color = FloorColor.pair_number

    @property
    def char(self):
        if self.is_rumble:
            return self.chars[1]
        return self.chars[0]


class DoorTile(TileBase):
    def __init__(self, game, cleared=False, locked=False, visited=False):
        super().__init__(game)
        self.name = "Door"
        self.is_walkable = True
        self.breaks_line_of_sight = False
        self.chars = ["X", "x", " "]
        self.provides_cover = True
        self.chars_emoji = ["🚪"]
        self.color = DoorColor.pair_number
        self.visited = visited
        self.locked = locked
        self.cleared = cleared

    @property
    def char(self):
        if self.cleared:
            return self.chars[2]
        if self.visited:
            return self.chars[1]
        return self.chars[0]


class ObstacleTile(TileBase):
    def __init__(self, game):
        super().__init__(game)
        self.name = "Obstacle"
        self.is_walkable = False
        self.provides_cover = True
        self.breaks_line_of_sight = False
        self.chars = ["O"]
        self.chars_emoji = ["O"]
        self.color = WallColor.pair_number
