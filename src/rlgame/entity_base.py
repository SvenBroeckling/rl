import random
import curses

from .colors import PlayerColor
from .dice import DiceRoll
from .inventory import Inventory
from .item_stack import ItemStack
from .items import Weapon, Armor
from .room_base import RoomBase


class EntityBase:
    def __init__(self, game, x, y, speed=1, health=10, shooting_skill=1, room=None):
        self.inventory = Inventory(game)
        self.name = "Entity"
        self.char = "@"
        self.char_emoji = "🧍"
        self.color = PlayerColor.pair_number
        self.x = x
        self.y = y
        self.game = game
        self._room = room
        self.speed = speed
        self.health = health
        self.max_health = health
        self.shooting_skill = shooting_skill
        self.view_distance = 10
        self.equipped_weapon = None
        self.equipped_armor = None
        self.reputation = 0

    # Methods to be implemented by subclasses
    def after_move(self, new_x, new_y):
        pass

    def before_move(self, new_x, new_y):
        pass

    def after_death(self):
        pass

    @property
    def room(self) -> RoomBase:
        if self._room:
            return self._room
        return self.game.current_room

    @property
    def attack_power(self):
        if self.equipped_weapon:
            return self.shooting_skill + self.equipped_weapon.damage_potential
        return self.shooting_skill

    def is_in_view_distance(self, x, y) -> bool:
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.view_distance**2

    def is_in_attack_range(self, x, y) -> bool:
        if not self.equipped_weapon:
            return False
        return (x - self.x) ** 2 + (y - self.y) ** 2 <= self.equipped_weapon.range**2

    def has_line_of_sight(self, entity: "EntityBase"):
        dx = entity.x - self.x
        dy = entity.y - self.y

        steps = max(abs(dx), abs(dy))
        for i in range(1, steps):
            x = self.x + int(i * dx / steps)
            y = self.y + int(i * dy / steps)

            if self.room.tiles[y][x].breaks_line_of_sight:
                return False
        return True

    def move(self, dx, dy):
        self.before_move(self.x + dx, self.y + dy)
        if self.room.is_walkable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
            self.after_move(self.x, self.y)

    def set_starting_equipment(self, min_tier=1, max_tier=9):
        for _ in range(3):
            item = random.choice(self.game.get_available_items(min_tier, max_tier))
            self.inventory.add_item(item)
        self.equip_weapon(
            random.choice(self.game.get_available_weapons(min_tier, max_tier))
        )
        self.equip_armor(
            random.choice(self.game.get_available_armor(min_tier, max_tier))
        )

    def has_cover(self, x, y) -> int | None:
        dx = x - self.x
        dy = y - self.y
        steps = max(abs(dx), abs(dy))
        for i in range(1, steps):
            x = self.x + int(i * dx / steps)
            y = self.y + int(i * dy / steps)
            if self.room.tiles[y][x].provides_cover:
                return 3 + min(2, i)

    def equip_weapon(self, weapon: Weapon | None):
        self.equipped_weapon = weapon

    def equip_armor(self, armor: Armor | None):
        self.equipped_armor = armor

    def roll_cover(self, hits, attack_x, attack_y):
        if hits == 0:
            return 0

        cover = self.has_cover(attack_x, attack_y)
        if cover:
            cover_roll = DiceRoll(
                f"{hits}d6", minimum_roll=cover, crit_target=None
            ).roll()
            self.game.add_log_message(
                f"{self.name} cover roll: [{cover_roll.result_string}] -> {cover_roll.successes} hits blocked.",
                color_pair=self.color,
            )
            hits -= cover_roll.successes
        return hits

    def reload_ammo(self):
        self.game.add_log_message(f"{self.name}: reloading...", color_pair=self.color)
        if self.equipped_weapon:
            self.equipped_weapon.magazine = self.equipped_weapon.magazine_capacity

    def has_ammo(self):
        if self.equipped_weapon:
            return self.equipped_weapon.magazine > 0
        return False

    def reduce_ammo(self):
        if self.equipped_weapon:
            self.equipped_weapon.magazine -= 1

    def drop_inventory_to_floor(self, room: "RoomBase"):
        """Drops all items in inventory to the floor."""
        for item_stack in self.inventory.item_stacks.values():
            room.add_item_stack_to_floor(self.x, self.y, item_stack)
        if self.equipped_weapon:
            room.add_item_stack_to_floor(
                self.x, self.y, ItemStack(self.game, self.equipped_weapon, 1)
            )
            self.equip_weapon(None)
        if self.equipped_armor:
            room.add_item_stack_to_floor(
                self.x, self.y, ItemStack(self.game, self.equipped_armor, 1)
            )
            self.equip_armor(None)
        self.inventory.clear()

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def attack(self, enemy):
        from .player import Player  # TODO: Quick hack to avoid circular import

        if not self.has_ammo():
            self.game.add_log_message("Out of ammo!", color_pair=self.color)
            return

        self.reduce_ammo()

        roll_string = f"{self.attack_power}d6"
        roll = DiceRoll(roll_string).roll()

        cover_str = "No cover"
        if enemy.has_cover(self.x, self.y):
            cover_str = f"Cover: {enemy.has_cover(self.x, self.y)}+"
        log_string = f"{self.name}: attacking with {roll_string}: [{roll.result_string}], {cover_str} ->"

        if roll.successes == 0 and roll.critical_hits == 0:
            log_string += " Miss!"
        else:
            log_string += f" {roll.successes} hits (-{enemy.equipped_armor.protection} protection)"
            if roll.critical_hits:
                log_string += f" {roll.critical_hits} critical hits!"

        self.game.add_log_message(log_string, color_pair=self.color)

        hits = enemy.roll_cover(roll.successes, self.x, self.y)
        enemy.health -= max(0, hits - enemy.equipped_armor.protection)
        critical_hits = enemy.roll_cover(roll.critical_hits, self.x, self.y)
        enemy.health -= max(0, critical_hits)

        if enemy.health <= 0:
            if isinstance(enemy, Player):
                self.game.add_log_message("You died!", color_pair=self.color)
                self.game.restart_game()
                return
            self.game.add_log_message("Enemy defeated.", color_pair=self.color)
            self.reputation += enemy.reputation
            self.game.current_room.enemies.remove(enemy)
            enemy.drop_inventory_to_floor(self.game.current_room)
            enemy.after_death()

    def draw(self, stdscr):
        if pos := self.room.get_map_position_in_viewport(self.x, self.y):
            x, y = pos
            if self.is_in_view_distance(self.game.player.x, self.game.player.y):
                stdscr.addch(y, x, self.char, curses.color_pair(self.color))
