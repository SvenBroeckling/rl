class Item:
    def __init__(self, key, name, amount=1, value=0, is_weapon=False):
        self.key = key
        self.name = name
        self.amount = amount
        self.value = value
        self.is_weapon = is_weapon

    def __str__(self):
        if self.is_weapon:
            return f"[{self.key}] {self.name} - {self.value} dmg bonus"
        return f"[{self.key}] {self.name} (x{self.amount})"

    def apply(self, player):
        """Applies the item to the player."""

        player.hp -= self.value
