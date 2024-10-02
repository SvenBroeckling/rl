import random

from .mixins import RoomWithEnemiesMixin
from .room_base import RoomBase


class Room(RoomBase, RoomWithEnemiesMixin):
    def __init__(self, game):
        super().__init__(game)
        self.hallway_entry = (0, 0)
        self.create_enemies()
        self.set_random_hallway_entry()

    @property
    def name(self):
        return "Room"

    @property
    def is_cleared(self):
        return not self.enemies

    def create_exit(self):
        self.exit = (self.width // 2, self.height - 1)

    def set_random_hallway_entry(self):
        x = random.randint(1, self.game.hallway.width - 2)
        y = random.randint(1, self.game.hallway.height - 2)
        self.hallway_entry = (x, y)

    def generate(self):
        tiles = self.generate_floor()
        tiles = self.generate_random_rumble(tiles)
        tiles = self.generate_obstacles(tiles)
        tiles = self.generate_walls(tiles)
        return tiles

    def generate_floor(self):
        return [
            [self.game.TILES["floor"] for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def generate_random_rumble(self, tiles):
        for y in range(self.height):
            for x in range(self.width):
                if random.random() > 0.2:
                    tiles[y][x] = self.game.TILES["rumble"]
        return tiles

    def generate_walls(self, tiles):
        for _ in range(random.randint(3, 5)):
            x = random.randint(1, self.width - 5)
            y = random.randint(1, self.height - 5)
            length = random.randint(3, 5)
            vertical = random.random() > 0.5
            for i in range(length):
                if vertical:
                    tiles[y + i][x] = self.game.TILES["wall"]
                else:
                    tiles[y][x + i] = self.game.TILES["wall"]
        return tiles

    def generate_obstacles(self, tiles):
        for _ in range(random.randint(3, 9)):
            x = random.randint(1, self.width - 5)
            y = random.randint(1, self.height - 5)
            width = random.randint(3, 5)
            height = random.randint(3, 5)
            for i in range(y, y + height):
                for j in range(x, x + width):
                    if random.random() > 0.5:
                        tiles[i][j] = self.game.TILES["obstacle"]
        return tiles
