class Item:
    identifier = "item"
    name = "Do not create raw Items"
    description = "A mysterious item"

    def apply(self, player):
        player.inventory.remove_item(self)
        self.apply_effect(player)
        self.log_message(player)

    def apply_effect(self, player):
        raise NotImplementedError("This should be implemented")

    def log_message(self, player):
        player.game.add_log_message(f"Used {self.name}")


class Weapon(Item):
    identifier = "weapon"
    damage_potential = 0
    range = 1
    piercing = 0
    magazine = 0
    magazine_capacity = 0
    splash_range = 0
    splash_reduction = 0

    def apply_effect(self, player):
        if player.equipped_weapon:
            player.inventory.add_item(player.equipped_weapon)
        player.equip_weapon(self)

    def log_message(self, player):
        player.game.add_log_message(f"Equipped {self.name}")


class Armor(Item):
    identifier = "armor"
    protection = 0

    def apply_effect(self, player):
        player.equip_armor(self)

    def log_message(self, player):
        player.game.add_log_message(f"Put on {self.name}")


class KevlarVest(Armor):
    identifier = "armor_kevlar"
    name = "Kevlar Vest"
    description = "A bulletproof vest. Reduces hits by 2."
    protection = 2


class PlateCarrier(Armor):
    identifier = "armor_plate_carrier"
    name = "Plate Carrier"
    description = "A heavy plate carrier. Reduces hits by 3."
    protection = 3


class SoftBodyArmor(Armor):
    identifier = "armor_soft_body_armor"
    name = "Soft Body Armor"
    description = "A light body armor. Reduces hits by 1."
    protection = 1


class StimPack(Item):
    identifier = "item_stimpack"
    name = "Stimpack"
    description = "A syringe filled with a red fluid. Heals 10 health."

    def apply_effect(self, player):
        player.health += 10


class Bandage(Item):
    identifier = "item_bandage"
    name = "Bandage"
    description = "A roll of bandages. Heals 5 health."

    def apply_effect(self, player):
        player.health += 5


class Pistol(Weapon):
    identifier = "weapon_pistol"
    name = "Pistol"
    description = "A standard 9mm handgun"
    range = 12
    damage_potential = 1
    magazine = 6
    magazine_capacity = 6


class Shotgun(Weapon):
    identifier = "weapon_shotgun"
    name = "Shotgun"
    description = "A 12-gauge shotgun"
    range = 5
    damage_potential = 4
    magazine = 2
    magazine_capacity = 2


class AssaultRifle(Weapon):
    identifier = "weapon_ar"
    name = "Assault Rifle"
    description = "A 9mm assault rifle."
    range = 20
    damage_potential = 3
    magazine = 24
    magazine_capacity = 24
