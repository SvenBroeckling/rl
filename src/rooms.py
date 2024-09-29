import random

from enemies import Enemy
from tiles import TILES


class Room:
    def __init__(self, game):
        self.height = random.randint(10, game.map_height)
        self.width = random.randint(10, game.map_width)
        self.name = "Room"
        self.game = game
        self.hallway_entry = (0, 0)
        self.enemies = []
        self.tiles = self.generate()
        self.create_enemies()
        self.set_random_hallway_entry()

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

    @property
    def offset_x(self):
        return (self.game.map_width - self.width) // 2

    @property
    def offset_y(self):
        return (self.game.map_height - self.height) // 2

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
