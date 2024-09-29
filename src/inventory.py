import curses


class Inventory:
    def __init__(self, game):
        self.game = game
        self.items = []
        self.selected_index = 0

    def add_item(self, item):
        """Adds an item to the inventory. If it exists, increases its amount."""
        for inv_item in self.items:
            if inv_item.key == item.key:
                inv_item.amount += item.amount
                return
        self.items.append(item)

    def open_inventory(self, stdscr):
        """Opens the inventory modal and allows the player to select items."""

        while True:
            stdscr.clear()
            self.draw_inventory(stdscr)

            key = stdscr.getch()

            if key == ord("q"):
                break
            elif key == ord("\n"):
                selected_item = self.items[self.selected_index]
                if selected_item.is_weapon:
                    self.game.player.equip_weapon(selected_item)
                return selected_item
            elif key == ord("j"):
                self.selected_index = (self.selected_index + 1) % len(self.items)
            elif key == ord("k"):
                self.selected_index = (self.selected_index - 1) % len(self.items)
            elif ord("a") <= key <= ord("z"):
                char_key = chr(key)
                for i, item in enumerate(self.items):
                    if item.key == char_key:
                        self.selected_index = i
                        return item

            stdscr.refresh()

    def draw_inventory(self, stdscr):
        """Draws the inventory modal."""
        height, width = stdscr.getmaxyx()
        title = "Inventory (Press 'q' to exit)"
        stdscr.addstr(1, (width - len(title)) // 2, title, curses.A_BOLD)

        for i, item in enumerate(self.items):
            x = 2
            y = 3 + i
            item_str = str(item)

            if i == self.selected_index:
                stdscr.addstr(y, x, item_str, curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, item_str)

    def get_item_by_key(self, key):
        """Retrieve an item by its key (used for direct selection)."""
        for item in self.items:
            if item.key == key:
                return item
        return None
