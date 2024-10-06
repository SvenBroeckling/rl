import random
import curses

from .colors import PlayerColor
from .dice import DiceRoll
from .inventory import Inventory
from .room_base import RoomBase


class EntityBase:
    def __init__(self, game, x, y, speed=1, health=10, shooting_skill=1, room=None):
        self.inventory = Inventory(self)
        self.char = game.CHARS["player"]
        self.color = PlayerColor.pair_number
        self.x = x
        self.y = y
        self.game = game
        self._room = room
        self.speed = speed
        self.health = health
        self.shooting_skill = shooting_skill
        self.view_distance = 10
        self.equipped_weapon = None
        self.equipped_armor = None
        self.reputation = 0

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

    def after_move(self, new_x, new_y):
        pass

    def move(self, dx, dy):
        if self.room.is_walkable(self.x + dx, self.y + dy):
            self.x += dx
            self.y += dy
        self.after_move(self.x, self.y)

    def set_starting_equipment(self):
        for _ in range(3):
            item = random.choice(self.game.available_items)
            self.inventory.add_item(item)
        self.inventory.add_item(random.choice(self.game.available_weapons))
        self.equip_weapon(random.choice(self.game.get_available_weapons()))
        self.equip_armor(random.choice(self.game.get_available_armor()))

    def has_cover(self, x, y) -> int | None:
        dx = x - self.x
        dy = y - self.y
        steps = max(abs(dx), abs(dy))
        for i in range(1, steps):
            x = self.x + int(i * dx / steps)
            y = self.y + int(i * dy / steps)
            if self.room.tiles[y][x].provides_cover:
                return 3 + min(2, i)

    def equip_weapon(self, weapon):
        self.equipped_weapon = weapon

    def equip_armor(self, armor):
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
                f"Cover roll: [{cover_roll.result_string}] -> {cover_roll.successes} hits blocked."
            )
            hits -= cover_roll.successes
        return hits

    def reload_ammo(self):
        self.game.add_log_message("Reloading...")
        if self.equipped_weapon:
            self.equipped_weapon.magazine = self.equipped_weapon.magazine_capacity

    def has_ammo(self):
        if self.equipped_weapon:
            return self.equipped_weapon.magazine > 0
        return False

    def reduce_ammo(self):
        if self.equipped_weapon:
            self.equipped_weapon.magazine -= 1
            if self.equipped_weapon.magazine == 0:
                self.game.add_log_message("Out of ammo, reload!")

    def attack(self, enemy):
        if not self.has_ammo():
            self.game.add_log_message("Out of ammo!")
            return

        self.reduce_ammo()

        roll_string = f"{self.attack_power}d6"
        roll = DiceRoll(roll_string).roll()

        cover_str = "No cover"
        if enemy.has_cover(self.x, self.y):
            cover_str = f"Cover: {enemy.has_cover(self.x, self.y)}+"
        log_string = (
            f"Attacking with {roll_string}: [{roll.result_string}], {cover_str} ->"
        )

        if roll.successes == 0 and roll.critical_hits == 0:
            log_string += " Miss!"
        else:
            log_string += f" {roll.successes} hits (-{enemy.equipped_armor.protection} protection)"
            if roll.critical_hits:
                log_string += f" {roll.critical_hits} critical hits!"

        self.game.add_log_message(log_string)

        hits = enemy.roll_cover(roll.successes, self.x, self.y)
        enemy.health -= max(0, hits - enemy.equipped_armor.protection)
        critical_hits = enemy.roll_cover(roll.critical_hits, self.x, self.y)
        enemy.health -= max(0, critical_hits)

        if enemy.health <= 0:
            self.game.add_log_message("Enemy defeated.")
            self.reputation += enemy.reputation
            self.game.current_room.enemies.remove(enemy)

    def after_draw(self):
        pass

    def draw(self, stdscr):
        if pos := self.room.get_map_position_in_viewport(self.x, self.y):
            x, y = pos
            if self.is_in_view_distance(self.game.player.x, self.game.player.y):
                stdscr.addch(y, x, self.char, curses.color_pair(self.color))
