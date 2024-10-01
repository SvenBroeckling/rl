import random

from enemies import Enemy


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

        num_enemies = random.randint(2, 4)
        for _ in range(num_enemies):
            enemy_x = random.randint(1, self.width - 2)
            enemy_y = random.randint(1, self.height - 2)
            speed = random.randint(0, 2)
            health = random.randint(5, 10)
            shooting_skill = random.randint(1, 3)
            new_enemy = Enemy(
                self.game, enemy_x, enemy_y, speed, health, shooting_skill, self
            )
            new_enemy.equip_weapon(random.choice(self.game.get_available_weapons()))
            self.enemies.append(new_enemy)

    def move_enemies(self):
        for enemy in self.enemies:
            enemy.update_movement()
            if enemy.can_move():
                dx, dy = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                new_x = enemy.x + dx
                new_y = enemy.y + dy
                if 0 <= new_x < self.width and 0 <= new_y < self.height:
                    enemy.move(dx, dy)
