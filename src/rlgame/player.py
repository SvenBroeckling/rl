import curses

from .colors import PlayerColor
from .entity_base import EntityBase
from .item_stack import ItemStack
from .items import Weapon, Armor
from .target_mode import TargetMode


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
        self.set_floor_info()

    def set_floor_info(self):
        item_stack = self.room.floor_item_stacks.get_item_stack(self.x, self.y)
        if item_stack is not None:
            self.game.info_line.set_info(f"On floor: {item_stack.item.name}")
            return
        self.game.info_line.set_info(self.room.tiles[self.y][self.x].name)

    def switch_weapon_from_floor(self, weapon):
        if self.equipped_weapon:
            self.room.floor_item_stacks.add_item_stack(
                self.x, self.y, ItemStack(self.game, self.equipped_weapon, 1)
            )
        self.equipped_weapon = weapon
        self.game.add_log_message(f"Equipped {weapon.name}")

    def switch_armor_from_floor(self, armor):
        if self.equipped_armor:
            self.room.floor_item_stacks.add_item_stack(
                self.x, self.y, ItemStack(self.game, self.equipped_armor, 1)
            )
        self.equipped_armor = armor
        self.game.add_log_message(f"Equipped {armor.name}")

    def pick_up_item(self):
        item_stack = self.room.floor_item_stacks.get_item_stack(self.x, self.y)
        if item_stack is not None:
            if isinstance(item_stack.item, Weapon):
                self.switch_weapon_from_floor(item_stack.item)
            elif isinstance(item_stack.item, Armor):
                self.switch_armor_from_floor(item_stack.item)
            else:
                self.inventory.add_item_stack(item_stack)
        else:
            self.game.add_log_message("There is nothing to pick up")

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
            self.target(self.room.enemies)
        elif key == ord("r"):
            self.reload_ammo()
        elif key == ord("g"):
            self.pick_up_item()

    def draw_status(self, stdscr, panel_x):
        status_y = 1
        stdscr.addstr(
            status_y,
            panel_x + 1,
            "Status",
            curses.color_pair(PlayerColor.pair_number) | curses.A_BOLD,
        )
        stdscr.addstr(
            status_y + 1,
            panel_x + 1,
            f"Reputation: {self.reputation}",
            curses.color_pair(PlayerColor.pair_number),
        )
        stdscr.addstr(
            status_y + 2,
            panel_x + 1,
            f"Health: {self.health}",
            curses.color_pair(PlayerColor.pair_number),
        )
        stdscr.addstr(
            status_y + 3,
            panel_x + 1,
            f"Shooting Skill: {self.shooting_skill}",
            curses.color_pair(PlayerColor.pair_number),
        )
        stdscr.addstr(
            status_y + 4,
            panel_x + 1,
            f"Speed: {self.speed}",
            curses.color_pair(PlayerColor.pair_number),
        )
        stdscr.addstr(
            status_y + 6,
            panel_x + 1,
            f"Equipped Weapon:",
            curses.color_pair(PlayerColor.pair_number),
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
            curses.color_pair(PlayerColor.pair_number),
        )

        stdscr.addstr(
            status_y + 9,
            panel_x + 1,
            f"Equipped Armor:",
            curses.color_pair(PlayerColor.pair_number),
        )
        armor_str = "None"
        if self.equipped_armor:
            armor_str = f"{self.equipped_armor.name} ({self.equipped_armor.protection} protection)"

        stdscr.addstr(
            status_y + 10,
            panel_x + 1,
            armor_str,
            curses.color_pair(PlayerColor.pair_number),
        )
