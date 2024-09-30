import curses


class Inventory:
    def __init__(self, game):
        self.game = game
        self.items = {}  # {identifier: {"key": key, "item": item, "amount":amount}}
        self.selected_identifier = None

    @property
    def next_free_key(self):
        """Returns the next available key for an item."""
        available_letters = "abcdefghilmnopqrstuvwxyzABCDEFGHILMNOPQRSTUVWXYZ"
        for letter in available_letters:
            if letter not in self.items:
                return letter
        return None

    def add_item(self, item):
        """Adds an item to the inventory. If it exists, increases its amount."""
        for key, item_data in self.items.items():
            if item_data["item"] == item:
                item_data["amount"] += 1
                return
        key = self.next_free_key
        if key:
            self.items[key] = {"key": key, "item": item, "amount": 1}

    def open_inventory(self, stdscr):
        """Opens the inventory modal and allows the player to select items."""

        if self.selected_identifier is None and self.items:
            self.selected_identifier = [key for key in self.items.keys()][0]

        while True:
            stdscr.clear()
            self.draw_inventory(stdscr)

            key = stdscr.getch()

            if key == ord("q"):
                break
            elif key == ord("\n"):
                return self.items[self.selected_identifier]["item"]
            elif key == ord("j"):
                keys = list(self.items.keys())
                index = keys.index(self.selected_identifier)
                index = (index + 1) % len(keys)
                self.selected_identifier = keys[index]
            elif key == ord("k"):
                keys = list(self.items.keys())
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
        height, width = stdscr.getmaxyx()
        title = "Inventory (Press 'q' to exit)"
        stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)

        for i, (identifier, item) in enumerate(self.items.items()):
            x = 2
            y = 3 + i
            amount_str = f"x{item['amount']}"
            item_str = f"{item["key"]} - {item["item"].name} ({amount_str})"

            if item == self.selected_identifier:
                stdscr.addstr(y, x, item_str, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item_str)

    def get_item_by_key(self, key):
        """Retrieve an item by its key (used for direct selection)."""
        for item_data in self.items.values():
            if item_data["key"] == key:
                return item_data["item"]
        return None
