import random

from .mixins import RoomWithEnemiesMixin
from .room_base import RoomBase
from .room_generators import SingleRoomGenerator


class Room(RoomBase, RoomWithEnemiesMixin):
    def __init__(self, game):
        super().__init__(game)
        self.hallway_entry = (0, 0)
        self.create_enemies()
        self.set_random_hallway_entry()

    @property
    def generator(self):
        return SingleRoomGenerator(game=self.game, width=self.width, height=self.height)

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
