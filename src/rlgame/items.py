import random

from rlgame.colors import ItemColor


class Item:
    identifier = "item"
    color_pair = ItemColor.pair_number
    chars = ["!"]
    chars_emoji = ["📦"]
    name = "Do not create raw Items"
    description = "A mysterious item"
    tier = 1
    stack_size = 1

    @property
    def char(self):
        return random.choice(self.chars)

    def apply(self, player):
        player.inventory.remove_item(self)
        self.apply_effect(player)
        self.log_message(player)

    def apply_effect(self, player):
        pass

    def log_message(self, player):
        player.game.add_log_message(f"Used {self.name}")


class Weapon(Item):
    identifier = "weapon"
    chars = ["/"]
    chars_emoji = ["🔫"]  # Emoji for weapon (sword): "🗡️"
    damage_potential = 0
    range = 1
    noise = 0
    piercing = 0
    magazine = 0
    magazine_capacity = 0
    splash_range = 0
    splash_reduction = 0
    stack_size = 0

    def apply_effect(self, player):
        if player.equipped_weapon:
            player.inventory.add_item(player.equipped_weapon)
        player.equip_weapon(self)

    def log_message(self, player):
        player.game.add_log_message(f"Equipped {self.name}")


class Armor(Item):
    identifier = "armor"
    chars = ["["]
    chars_emoji = ["🛡️"]
    protection = 0
    stack_size = 0

    def apply_effect(self, player):
        player.equip_armor(self)

    def log_message(self, player):
        player.game.add_log_message(f"Put on {self.name}")


class KevlarVest(Armor):
    identifier = "armor_kevlar"
    name = "Kevlar Vest"
    description = "A bulletproof vest. Reduces hits by 2."
    protection = 1
    tier = 2


class PlateCarrier(Armor):
    identifier = "armor_plate_carrier"
    name = "Plate Carrier"
    description = "A heavy plate carrier. Reduces hits by 3."
    protection = 2
    tier = 3


class SoftBodyArmor(Armor):
    identifier = "armor_soft_body_armor"
    name = "Soft Body Armor"
    description = "A light body armor. Reduces hits by 1."
    protection = 1
    tier = 1


class TwoPieceSuit(Armor):
    identifier = "armor_two_piece_suit"
    name = "Two Piece Suit"
    description = "A two piece suit. Looks good, but doesn't protect much."
    protection = 0
    tier = 1


class HeavyPlatedArmor(Armor):
    identifier = "armor_heavy_plated"
    name = "Heavy Plated Armor"
    description = "An extremely heavy armor with high protection."
    protection = 3
    tier = 4


class StimPack(Item):
    identifier = "item_stimpack"
    name = "Stimpack"
    description = "A syringe filled with a red fluid. Heals 10 health."
    stack_size = 2
    tier = 2

    def apply_effect(self, player):
        player.heal(10)


class Lockpick(Item):
    identifier = "item_lockpick"
    name = "Lockpick"
    description = "A tool used to open locked doors or containers."
    stack_size = 3
    tier = 1

    def apply_effect(self, player):
        if not player.game.current_room.exit:
            player.game.add_log_message("You use the lockpick.")
            player.game.current_room.create_exit()


class Bandage(Item):
    identifier = "item_bandage"
    name = "Bandage"
    description = "A roll of bandages. Heals 5 health."
    stack_size = 5
    tier = 1

    def apply_effect(self, player):
        player.heal(5)


class Slingshot(Weapon):
    identifier = "weapon_slingshot"
    name = "Slingshot"
    description = "A simple ranged weapon that fires small stones."
    range = 10
    noise = 0
    damage_potential = 1
    magazine = 1
    magazine_capacity = 1
    tier = 1


class Pistol(Weapon):
    identifier = "weapon_pistol"
    name = "Pistol"
    description = "A standard 9mm handgun"
    range = 12
    noise = 2
    damage_potential = 1
    magazine = 6
    magazine_capacity = 6
    tier = 1


class Revolver(Weapon):
    identifier = "weapon_revolver"
    name = "Revolver"
    description = "A .357 revolver"
    range = 10
    noise = 3
    piercing = 1
    damage_potential = 2
    magazine = 6
    magazine_capacity = 6
    tier = 1


class Shotgun(Weapon):
    identifier = "weapon_shotgun"
    name = "Shotgun"
    description = "A 12-gauge shotgun"
    range = 5
    noise = 4
    damage_potential = 4
    magazine = 2
    magazine_capacity = 2
    tier = 2


class Crossbow(Weapon):
    identifier = "weapon_crossbow"
    name = "Crossbow"
    description = "A silent and deadly ranged weapon."
    range = 15
    noise = 0
    damage_potential = 3
    magazine = 1
    magazine_capacity = 1
    tier = 2


class AssaultRifle(Weapon):
    identifier = "weapon_ar"
    name = "Assault Rifle"
    description = "A 9mm assault rifle."
    range = 20
    damage_potential = 3
    noise = 3
    piercing = 2
    magazine = 24
    magazine_capacity = 24
    tier = 3


class SniperRifle(Weapon):
    identifier = "weapon_sniper_rifle"
    name = "Sniper Rifle"
    description = "A long-range rifle with high damage."
    range = 30
    damage_potential = 5
    noise = 4
    piercing = 3
    magazine = 5
    magazine_capacity = 5
    tier = 3


class MachineGun(Weapon):
    identifier = "weapon_machine_gun"
    name = "Machine Gun"
    description = "A 7.62mm machine gun."
    range = 15
    noise = 5
    damage_potential = 4
    piercing = 3
    magazine = 50
    magazine_capacity = 50
    tier = 4
