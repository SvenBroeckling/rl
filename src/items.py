class Item:
    identifier = "item"
    name = "Do not create raw Items"
    description = "A mysterious item"

    def apply(self, player):
        raise NotImplementedError("This should be implemented")


class Weapon(Item):
    identifier = "weapon"
    damage_potential = 0
    range = 1
    piercing = 0
    capacity = 0

    def apply(self, player):
        player.equip_weapon(self)


class Armor(Item):
    identifier = "armor"
    protection = 0

    def apply(self, player):
        player.equip_armor(self)


class HealingPotion(Item):
    identifier = "healing_potion"
    name = "Healing Potion"
    description = "A potion that heals you for 5 health."

    def apply(self, player):
        player.health += 5


class Pistol(Weapon):
    identifier = "weapon_pistol"
    name = "Pistol"
    description = "A standard 9mm handgun"
    range = 12
    damage_potential = 1
    capacity = 6


class AssaultRifle(Weapon):
    identifier = "weapon_ar"
    name = "Assault Rifle"
    description = "A 9mm assault rifle."
    range = 20
    damage_potential = 3
    capacity = 24
