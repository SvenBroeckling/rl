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


class Rock(Weapon):
    identifier = "weapon_rock"
    name = "Rock"
    description = "A fist-sized rock, good for throwing."
    range = 10
    damage_potential = 1


class Sword(Weapon):
    identifier = "weapon_sword"
    name = "Sword"
    description = "A short sword."
    range = 1
    damage_potential = 2
