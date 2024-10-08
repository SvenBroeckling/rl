import curses

from rlgame.item_stack import ItemStack


class Inventory:
    def __init__(self, game: "Game"):
        self.game = game
        self.item_stacks: dict[str, ItemStack] = {}
        self.selected_identifier: str | None = None

    def get_next_free_key(self):
        """Returns the next available key for an item."""
        available_letters = "abcdefghlmnopqrstuvwxyzABCDEFGHILMNOPQRSTUVWXYZ"
        for letter in available_letters:
            if letter not in self.item_stacks:
                return letter
        return None

    def add_item_stack(self, item_stack: ItemStack):
        """Adds an item stack to the inventory."""
        self.add_item(item_stack.item, item_stack.amount)

    def add_item(self, item: "Item", amount=1):
        """Adds an item to the inventory. If it exists, increases its amount."""
        for key, item_stack in self.item_stacks.items():
            if type(item_stack.item) is type(item):
                rest = item_stack.add_items(amount)
                if rest > 0:
                    self.item_stacks[self.get_next_free_key()] = ItemStack(
                        self.game, item, rest
                    )
                return

        self.item_stacks[self.get_next_free_key()] = ItemStack(self.game, item, amount)

    def clear(self):
        """Clears the inventory."""
        self.item_stacks = {}

    def remove_item(self, item: "Item", amount=1):
        """Removes an item from the inventory. If it exists, decreases its amount."""
        for key, item_stack in self.item_stacks.items():
            if item_stack.item == item:
                if item_stack.remove_items(amount):
                    del self.item_stacks[key]
                    self.selected_identifier = None
                return

    def open_inventory(self, stdscr):
        """Opens the inventory modal and allows the player to select items."""

        if self.selected_identifier is None and self.item_stacks:
            self.selected_identifier = [key for key in self.item_stacks.keys()][0]

        while True:
            stdscr.clear()
            self.draw_inventory(stdscr)

            key = stdscr.getch()

            if key == ord("i"):
                break
            elif key == ord("\n"):
                return self.item_stacks[self.selected_identifier].item
            elif key == ord("j"):
                keys = list(self.item_stacks.keys())
                index = keys.index(self.selected_identifier)
                index = (index + 1) % len(keys)
                self.selected_identifier = keys[index]
            elif key == ord("k"):
                keys = list(self.item_stacks.keys())
                index = keys.index(self.selected_identifier)
                index = (index - 1) % len(keys)
                self.selected_identifier = keys[index]
            elif ord("a") <= key <= ord("z"):
                char_key = chr(key)
                item = self.get_item_by_key(char_key)
                if item:
                    return item
            stdscr.refresh()

    def draw_inventory(self, stdscr):
        """Draws the inventory modal."""
        _, width = stdscr.getmaxyx()
        title = "Inventory (Press 'i' to exit)"
        stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)

        for i, (key, item_stack) in enumerate(self.item_stacks.items()):
            x = 2
            y = 3 + i
            item_str = f"{key} - {item_stack.item.name} ({item_stack.amount})"

            if key == self.selected_identifier:
                stdscr.addstr(y, x, item_str, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item_str)
        self.game.stdscr.refresh()

    def get_item_by_key(self, key: str):
        """Retrieve an item by its key (used for direct selection)."""
        for inventory_key, item_stack in self.item_stacks.items():
            if key == inventory_key:
                return item_stack.item
        return None
