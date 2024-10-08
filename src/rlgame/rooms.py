import random

from .enemies import Enemy
from .room_base import RoomBase
from .room_generators import SingleRoomGenerator


class Room(RoomBase):
    def __init__(self, game):
        super().__init__(game)
        self.hallway_entry = (0, 0)
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

    def create_enemies(self):
        self.enemies = []

        amount = self.challenge_rating * random.randint(1, 3)
        for _ in range(amount):
            new_enemy = Enemy(
                game=self.game,
                x=random.randint(1, self.width - 2),
                y=random.randint(1, self.height // 2),
                speed=random.randint(0, 2),
                health=self.challenge_rating * random.randint(1, 3),
                shooting_skill=self.challenge_rating * random.randint(1, 2),
                room=self,
            )
            new_enemy.reputation = self.challenge_rating
            new_enemy.set_starting_equipment(
                min_tier=self.challenge_rating - 1, max_tier=self.challenge_rating
            )
            self.enemies.append(new_enemy)

    def create_exit(self):
        self.exit = (self.width // 2, self.height - 1)

    def set_random_hallway_entry(self):
        x = random.randint(1, self.game.hallway.width - 2)
        y = random.randint(1, self.game.hallway.height - 2)
        self.hallway_entry = (x, y)
