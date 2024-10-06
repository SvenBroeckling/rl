import random

from .enemies import Enemy


class RoomWithEnemiesMixin:
    def __init__(self, game):
        self.game = game
        self.enemies = []
        self.create_enemies()

    def draw_enemies(self, stdscr):
        for enemy in self.enemies:
            enemy.draw(stdscr)

    def create_enemies(self):
        self.enemies = []

        amount = self.width * self.height // 200
        for _ in range(amount):
            new_enemy = Enemy(
                game=self.game,
                x=random.randint(1, self.width - 2),
                y=random.randint(1, self.height - 2),
                speed=random.randint(0, 2),
                health=random.randint(5, 10),
                shooting_skill=random.randint(1, 3),
                room=self,
            )
            new_enemy.reputation = random.randint(1, 3)
            new_enemy.set_starting_equipment()
            self.enemies.append(new_enemy)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.update_movement()
            if enemy.can_move():
                dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                enemy.move(dx, dy)
