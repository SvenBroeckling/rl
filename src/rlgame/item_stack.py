class FloorItemStacks:
    """An item stack on the floor of a room."""

    def __init__(self, room: "RoomBase"):
        self.room = room
        self.item_stacks: dict[tuple[int, int], "ItemStack"] = {}

    def add_item_stack(self, x: int, y: int, item_stack: "ItemStack"):
        """Adds an item stack to the floor."""
        self.item_stacks[(x, y)] = item_stack

    def remove_item_stack(self, x: int, y: int):
        """Removes an item stack from the floor."""
        del self.item_stacks[(x, y)]

    def get_item_stack(self, x: int, y: int) -> "ItemStack":
        """Returns an item stack from the floor."""
        return self.item_stacks.get((x, y), None)


class ItemStack:
    def __init__(self, game: "Game", item: "Item", amount: int):
        self.game = game
        self.item = item
        self.amount = amount

    def has_space_for_item(self, amount) -> bool:
        """Returns whether the stack has space for an item."""
        return self.amount + amount <= self.item.stack_size

    def add_items(self, amount: int) -> int:
        """Adds an item to the stack. Returns the amount that could not be added."""
        if self.has_space_for_item(amount):
            self.amount += amount
            return 0
        else:
            added = self.item.stack_size - self.amount
            self.amount = self.item.stack_size
            return amount - added

    def remove_items(self, amount) -> bool:
        """Removes an item from the stack. Returns True if the stack is empty."""
        self.amount -= amount
        if self.amount <= 0:
            return True
        return False
