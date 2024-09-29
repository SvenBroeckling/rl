import random

from enemies import Enemy


class EnemiesMixin:
    def __init__(self, game):
        self.game = game
        self.enemies = []
        self.create_enemies()

    def draw_enemies(self, stdscr):
        for enemy in self.enemies:
            enemy.draw(stdscr)

    def create_enemies(self):
        self.enemies = []

        num_enemies = random.randint(5, 10)
        for _ in range(num_enemies):
            enemy_x = random.randint(1, self.width - 2)
            enemy_y = random.randint(1, self.height - 2)
            speed = random.randint(0, 2)
            new_enemy = Enemy(enemy_x, enemy_y, speed, 10, self)
            self.enemies.append(new_enemy)

        self.game.add_log_message(f"Generated {num_enemies} enemies.")

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.update_movement()
            if enemy.can_move():
                dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                new_x = enemy.x + dx
                new_y = enemy.y + dy
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    enemy.move(dx, dy)
