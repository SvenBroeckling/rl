import curses

from entity_base import EntityBase
from mixins import RoomWithEnemiesMixin
from target_mode import TargetMode


class Player(EntityBase):
    def __init__(self, game, x, y, speed=1, health=10, shooting_skill=1, room=None):
        super().__init__(game, x, y, speed, health, shooting_skill, room)
        self.target_mode = None
        self.target_index = 0
        self.target_x = None
        self.target_y = None

    def after_move(self, new_x, new_y):
        if self.game.current_room is self.game.hallway:
            for room in self.game.available_rooms:
                if (new_x, new_y) == room.hallway_entry:
                    self.game.enter_room(room)
                    return
        else:
            if self.game.current_room.exit:
                if (new_x, new_y) == self.game.current_room.exit:
                    self.game.exit_room(self.game.current_room)
                    return

    def target(self, enemies):
        if enemies:
            self.target_mode = TargetMode(enemies, self.game)
            self.target_mode.input_loop()

    def handle_input(self, key):
        if key == ord("h"):
            self.move(-1, 0)
        elif key == ord("j"):
            self.move(0, 1)
        elif key == ord("k"):
            self.move(0, -1)
        elif key == ord("l"):
            self.move(1, 0)
        elif key == ord("f"):
            if isinstance(self.room, RoomWithEnemiesMixin):
                self.target(self.room.enemies)
        elif key == ord("r"):
            self.reload_ammo()

    def after_draw(self):
        if self.target_mode:
            self.target_mode.draw_target_line()

    def draw_status(self, stdscr, panel_x):
        status_y = 1
        stdscr.addstr(
            status_y,
            panel_x + 1,
            "Status",
            curses.color_pair(self.game.COLORS["player"]) | curses.A_BOLD,
        )
        stdscr.addstr(
            status_y + 1,
            panel_x + 1,
            f"Reputation: {self.reputation}",
            curses.color_pair(self.game.COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 2,
            panel_x + 1,
            f"Health: {self.health}",
            curses.color_pair(self.game.COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 3,
            panel_x + 1,
            f"Shooting Skill: {self.shooting_skill}",
            curses.color_pair(self.game.COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 4,
            panel_x + 1,
            f"Speed: {self.speed}",
            curses.color_pair(self.game.COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 6,
            panel_x + 1,
            f"Equipped Weapon:",
            curses.color_pair(self.game.COLORS["player"]),
        )

        weapon_str = "None"
        if self.equipped_weapon:
            info_str = f"{self.equipped_weapon.name} {self.equipped_weapon.damage_potential}d6, {self.equipped_weapon.range}m"
            magazine_str = f"[{self.equipped_weapon.magazine}/{self.equipped_weapon.magazine_capacity}]"
            weapon_str = f"{info_str} {magazine_str}"

        stdscr.addstr(
            status_y + 7,
            panel_x + 1,
            weapon_str,
            curses.color_pair(self.game.COLORS["player"]),
        )

        stdscr.addstr(
            status_y + 9,
            panel_x + 1,
            f"Equipped Armor:",
            curses.color_pair(self.game.COLORS["player"]),
        )
        stdscr.addstr(
            status_y + 10,
            panel_x + 1,
            f"{self.equipped_armor if self.equipped_armor else 'None'}",
            curses.color_pair(self.game.COLORS["player"]),
        )
