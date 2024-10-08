import curses

from .colors import EnemyColor, PlayerColor
from .entity_base import EntityBase


class Enemy(EntityBase):
    def __init__(self, game, x, y, speed=1, health=10, shooting_skill=1, room=None):
        super().__init__(game, x, y, speed, health, shooting_skill, room)
        self.char = "E"
        self.name = "Enemy"
        self.char_emoji = "👹"
        self.color = EnemyColor.pair_number
        self.current_speed = 0  # Current speed counter

    def update_movement(self):
        self.current_speed += 1

    def can_attack_player(self):
        return (
            self.has_line_of_sight(self.room.game.player)
            and self.is_in_attack_range(
                self.room.game.player.x, self.room.game.player.y
            )
            and self.has_ammo()
        )

    def can_move_by_speed(self):
        if self.current_speed >= self.speed:
            self.current_speed = 0  # Reset speed counter after moving
            return True
        return False

    def after_death(self):
        if not self.room.enemies:
            self.room.game.add_log_message("You defeated all enemies in the room.")
            self.room.game.add_log_message("The exit is now available.")
            self.room.create_exit()

    def draw_status(self, stdscr, panel_x):
        status_y = 13
        stdscr.addstr(
            status_y,
            panel_x + 1,
            f"Attack {self.room.game.player.attack_power}d6",
            curses.color_pair(PlayerColor.pair_number),
        )
        cover = self.room.game.player.has_cover(self.x, self.y)
        stdscr.addstr(
            status_y + 1,
            panel_x + 1,
            f"Cover {cover}+" if cover else "No Cover",
            curses.color_pair(PlayerColor.pair_number),
        )

        stdscr.addstr(
            status_y + 3,
            panel_x + 1,
            "Enemy",
            curses.color_pair(EnemyColor.pair_number) | curses.A_BOLD,
        )
        stdscr.addstr(
            status_y + 4,
            panel_x + 1,
            f"Health: {self.health}",
            curses.color_pair(EnemyColor.pair_number),
        )
        stdscr.addstr(
            status_y + 5,
            panel_x + 1,
            f"Shooting Skill: {self.shooting_skill}",
            curses.color_pair(EnemyColor.pair_number),
        )
        stdscr.addstr(
            status_y + 6,
            panel_x + 1,
            f"Reputation: {self.reputation}",
            curses.color_pair(EnemyColor.pair_number),
        )

        stdscr.addstr(
            status_y + 8,
            panel_x + 1,
            f"Equipped Weapon:",
            curses.color_pair(EnemyColor.pair_number),
        )
        stdscr.addstr(
            status_y + 9,
            panel_x + 1,
            f"{self.equipped_weapon.name if self.equipped_weapon else 'None'}",
            curses.color_pair(EnemyColor.pair_number),
        )

        stdscr.addstr(
            status_y + 10,
            panel_x + 1,
            f"Equipped Armor:",
            curses.color_pair(EnemyColor.pair_number),
        )
        armor_str = "None"
        if self.equipped_armor:
            armor_str = f"{self.equipped_armor.name} ({self.equipped_armor.protection} protection)"

        stdscr.addstr(
            status_y + 11,
            panel_x + 1,
            armor_str,
            curses.color_pair(EnemyColor.pair_number),
        )

        stdscr.addstr(
            status_y + 13,
            panel_x + 1,
            f"Attack {self.attack_power}d6",
            curses.color_pair(EnemyColor.pair_number),
        )
        cover = self.has_cover(self.room.game.player.x, self.room.game.player.y)
        stdscr.addstr(
            status_y + 14,
            panel_x + 1,
            f"Cover {cover}+" if cover else "No Cover",
            curses.color_pair(EnemyColor.pair_number),
        )


class TutorialEnemy(Enemy):
    def __init__(self, game, x, y, speed=1, health=10, shooting_skill=1, room=None):
        super().__init__(game, x, y, speed, health, shooting_skill, room)
        self.char = "E"
        self.name = "Tutorial Enemy"
        self.char_emoji = "👹"

    def after_death(self):
        self.room.game.add_log_message("You defeated the tutorial enemy.")
        self.room.game.add_log_message(
            "It dropped some items, have a look around. Use 'g' to pick up items."
        )
