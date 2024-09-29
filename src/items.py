class Item:
    def __init__(self, key, name, amount=1):
        self.key = key       # A unique key assigned to the item, e.g., 'a', 'b', etc.
        self.name = name     # The name of the item, e.g., "Health Potion"
        self.amount = amount # Number of items in the player's inventory

    def __str__(self):
        """String representation of the item for display in the inventory."""
        return f"[{self.key}] {self.name} (x{self.amount})"
