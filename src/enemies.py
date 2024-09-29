import curses

ENEMY_CHAR = "E"
COLOR_ENEMY = 2


class Enemy:
    def __init__(self, x, y, speed, health, room):
        self.x = x
        self.y = y
        self.room = room
        self.char = ENEMY_CHAR
        self.speed = speed  # Speed defines how often the enemy moves (0 is fastest)
        self.current_speed = 0  # Current speed counter
        self.health = health

    def draw(self, stdscr):
        stdscr.addch(
            self.y + self.room.offset_y,
            self.x + self.room.offset_x,
            self.char,
            curses.color_pair(COLOR_ENEMY),
        )

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def update_movement(self):
        self.current_speed += 1

    def can_move(self):
        if self.current_speed >= self.speed:
            self.current_speed = 0  # Reset speed counter after moving
            return True
        return False
