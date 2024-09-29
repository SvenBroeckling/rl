import curses

from hallway import Hallway
from inventory import Inventory
from items import Item
from mixins import EnemiesMixin
from player import Player
from rooms import Room


class Game:
    def __init__(self, stdscr):
        self.stdscr = stdscr
        self.side_panel_width = 25
        self.screen_height, self.screen_width = stdscr.getmaxyx()
        self.update_game_dimensions()

        self.hallway = Hallway(self)
        self.current_room = self.hallway
        self.available_rooms = []

        self.player = Player(
            self.current_room.width // 2, self.current_room.height // 2, self
        )
        self.inventory = Inventory()

        self.inventory.add_item(Item("a", "Health Potion", 2))
        self.inventory.add_item(Item("b", "Mana Potion", 3))
        self.inventory.add_item(Item("c", "Sword"))

        # Initialize game states
        self.target_mode = False
        self.target_index = 0
        self.target_x = None
        self.target_y = None
        self.log_messages = []

    def create_available_rooms(self):
        for _ in range(10):
            self.available_rooms.append(Room(self))

    def init_colors(self):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)  # Player
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)  # Enemy
        curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Pickups, etc.
        curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(8, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(9, curses.COLOR_WHITE, curses.COLOR_BLACK)

    def update_game_dimensions(self):
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()
        self.map_width = self.screen_width - self.side_panel_width
        self.map_height = self.screen_height - 2

    def draw_map(self):
        self.current_room.draw(self.stdscr)

    def draw_entities(self):
        self.player.draw(self.stdscr)
        if isinstance(self.current_room, EnemiesMixin):
            self.current_room.draw_enemies(self.stdscr)

    def draw_side_panel(self):
        panel_x = self.map_width
        self.player.draw_status(self.stdscr, panel_x)
        self.draw_log(panel_x)

    def draw_room_name(self):
        self.stdscr.addstr(0, 0, self.current_room.name, curses.color_pair(7))

    def draw_log(self, panel_x):
        log_start_y = self.screen_height - 6
        for i, message in enumerate(self.log_messages[-4:], 1):
            self.stdscr.addstr(
                log_start_y + i,
                panel_x + 1,
                message[: self.side_panel_width - 2],
                curses.color_pair(7),
            )

    def add_log_message(self, message):
        self.log_messages.append(message)

    def enter_room(self, room):
        self.current_room = room
        self.player.x = self.current_room.width // 2
        self.player.y = self.current_room.height // 2
        self.add_log_message("Entered a room.")

    def game_loop(self):
        self.init_colors()
        self.create_available_rooms()
        self.add_log_message("Welcome to the dungeon!")
        self.add_log_message("Move with arrow keys")
        self.add_log_message("Press 'f' to target")
        self.add_log_message("Press 'q' to quit")

        while True:
            self.stdscr.clear()
            self.draw_map()
            self.draw_entities()
            self.draw_room_name()
            self.draw_side_panel()

            self.stdscr.refresh()
            key = self.stdscr.getch()

            if key == ord("q"):
                break
            elif key == ord("f"):
                if isinstance(self.current_room, EnemiesMixin):
                    self.player.toggle_target_mode(self.current_room.enemies)
            elif key == ord("i"):
                selected_item = self.inventory.open_inventory(self.stdscr)
                if selected_item:
                    self.add_log_message(f"Selected {selected_item.name}")

            if not self.player.target_mode:
                self.player.handle_input(key, self)
                if isinstance(self.current_room, EnemiesMixin):
                    self.current_room.move_enemies()
            else:
                if isinstance(self.current_room, EnemiesMixin):
                    self.player.handle_target_mode(key, self.current_room.enemies)
