import curses

from constants import CHARS, COLORS


class Enemy:
    def __init__(self, x, y, speed, health, room):
        self.x = x
        self.y = y
        self.room = room
        self.char = CHARS["enemy"]
        self.speed = speed  # Speed defines how often the enemy moves (0 is fastest)
        self.current_speed = 0  # Current speed counter
        self.health = health
        self.shooting_skill = 1
        self.reputation_value = 1
        self.equipped_weapon = None
        self.equipped_armor = None

    def draw(self, stdscr):
        stdscr.addch(
            self.y + self.room.offset_y,
            self.x + self.room.offset_x,
            self.char,
            curses.color_pair(COLORS["enemy"]),
        )

    def draw_status(self, stdscr, panel_x):
        status_y = 13
        stdscr.addstr(
            status_y,
            panel_x + 1,
            "Enemy",
            curses.color_pair(COLORS["enemy"]) | curses.A_BOLD,
        )
        stdscr.addstr(
            status_y + 1,
            panel_x + 1,
            f"Health: {self.health}",
            curses.color_pair(COLORS["enemy"]),
        )
        stdscr.addstr(
            status_y + 2,
            panel_x + 1,
            f"Shooting Skill: {self.shooting_skill}",
            curses.color_pair(COLORS["enemy"]),
        )
        stdscr.addstr(
            status_y + 3,
            panel_x + 1,
            f"Reputation: {self.reputation_value}",
            curses.color_pair(COLORS["enemy"]),
        )

        stdscr.addstr(
            status_y + 5,
            panel_x + 1,
            f"Equipped Weapon:",
            curses.color_pair(COLORS["enemy"]),
        )
        stdscr.addstr(
            status_y + 6,
            panel_x + 1,
            f"{self.equipped_weapon if self.equipped_weapon else 'None'}",
            curses.color_pair(COLORS["enemy"]),
        )

        stdscr.addstr(
            status_y + 6,
            panel_x + 1,
            f"Equipped Armor:",
            curses.color_pair(COLORS["enemy"]),
        )
        stdscr.addstr(
            status_y + 7,
            panel_x + 1,
            f"{self.equipped_armor if self.equipped_armor else 'None'}",
            curses.color_pair(COLORS["enemy"]),
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
