import curses

from constants import CHARS, COLORS
from dice import DiceRoll
from target_mode import TargetMode


class Player:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.game = game
        self.char = CHARS["player"]
        self.speed = 1
        self.health = 10
        self.reputation = 0
        self.shooting_skill = 1
        self.equipped_weapon = None
        self.equipped_armor = None
        self.target_mode = None
        self.target_index = 0
        self.target_x = None
        self.target_y = None

    @property
    def offset_x(self):
        return (self.game.map_width - self.game.current_room.width) // 2

    @property
    def offset_y(self):
        return (self.game.map_height - self.game.current_room.height) // 2

    def move(self, dx, dy, game):
        new_x = self.x + dx
        new_y = self.y + dy

        if (
            0 <= new_x < game.current_room.width
            and 0 <= new_y < game.current_room.height
        ):
            if game.current_room is game.hallway:
                for room in game.available_rooms:
                    if (new_x, new_y) == room.hallway_entry:
                        self.game.enter_room(room)
                        return
            else:
                if game.current_room.exit:
                    if (new_x, new_y) == game.current_room.exit:
                        self.game.exit_room(game.current_room)
                        return
            self.x = new_x
            self.y = new_y

    def attack(self, enemy):
        attack_power = self.shooting_skill
        successes = DiceRoll(f"{attack_power}d6+0").roll()
        enemy.health -= successes
        self.game.add_log_message(f"Player attacked enemy for {successes} damage.")
        if self.game.selected_enemy.health <= 0:
            self.game.add_log_message("Enemy defeated.")
            self.game.current_room.enemies.remove(self.game.selected_enemy)

    def target(self, enemies):
        self.target_mode = TargetMode(enemies, self.game)
        self.target_mode.input_loop()

    def handle_input(self, key, game):
        if key == ord("h"):
            self.move(-1, 0, game)
        elif key == ord("j"):
            self.move(0, 1, game)
        elif key == ord("k"):
            self.move(0, -1, game)
        elif key == ord("l"):
            self.move(1, 0, game)

    def draw(self, stdscr):
        stdscr.addch(
            self.y + self.offset_y,
            self.x + self.offset_x,
            self.char,
            curses.color_pair(COLORS["player"]),
        )
        if self.target_mode:
            self.target_mode.draw_target_line()

    def draw_status(self, stdscr, panel_x):
        status_y = 1
        stdscr.addstr(
            status_y,
            panel_x + 1,
            "Status",
            curses.color_pair(COLORS["player"]) | curses.A_BOLD,
        )
        stdscr.addstr(
            status_y + 1,
            panel_x + 1,
            f"Reputation: {self.reputation}",
            curses.color_pair(COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 2,
            panel_x + 1,
            f"Health: {self.health}",
            curses.color_pair(COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 3,
            panel_x + 1,
            f"Shooting Skill: {self.shooting_skill}",
            curses.color_pair(COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 4,
            panel_x + 1,
            f"Speed: {self.speed}",
            curses.color_pair(COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 6,
            panel_x + 1,
            f"Equipped Weapon:",
            curses.color_pair(COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 7,
            panel_x + 1,
            f"{self.equipped_weapon if self.equipped_weapon else 'None'}",
            curses.color_pair(COLORS["player"]),
        )

        stdscr.addstr(
            status_y + 8,
            panel_x + 1,
            f"Equipped Armor:",
            curses.color_pair(COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 9,
            panel_x + 1,
            f"{self.equipped_armor if self.equipped_armor else 'None'}",
            curses.color_pair(COLORS["player"]),
        )
