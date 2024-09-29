import random

from mixins import EnemiesMixin
from room_base import RoomBase
from tiles import TILES


class Room(RoomBase, EnemiesMixin):
    def __init__(self, game):
        super().__init__(game)
        self.hallway_entry = (0, 0)
        self.create_enemies()
        self.set_random_hallway_entry()

    @property
    def name(self):
        return "Room"

    def set_random_hallway_entry(self):
        x = random.randint(1, self.game.hallway.width - 2)
        y = random.randint(1, self.game.hallway.height - 2)
        self.hallway_entry = (x, y)

    def generate(self):
        return [
            [
                TILES["grass"] if random.random() > 0.2 else TILES["lava"]
                for _ in range(self.width)
            ]
            for _ in range(self.height)
        ]
