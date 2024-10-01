import curses
import random

import constants
from hallway import Hallway
from inventory import Inventory
from items import Armor, Item, Weapon
from mixins import EnemiesMixin
from player import Player
from rooms import Room
from status_line import StatusLine


class Game:
    def __init__(self, stdscr, no_emoji=False):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.side_panel_width = 25
        self.screen_height, self.screen_width = stdscr.getmaxyx()
        self.update_game_dimensions()

        self.init_resources(no_emoji)

        self.status_line = StatusLine(stdscr)

        self.hallway = Hallway(self)
        self.current_room = self.hallway
        self.available_rooms = []

        self.player = Player(
            self.current_room.width // 2, self.current_room.height // 2, self
        )
        self.selected_enemy = None
        self.inventory = Inventory(self)
        self.available_items = self.get_available_items()
        self.available_weapons = self.get_available_weapons()
        self.available_armor = self.get_available_armor()

        for _ in range(3):
            item = random.choice(self.available_items)
            self.inventory.add_item(item)
        self.inventory.add_item(random.choice(self.available_weapons))

        # Initialize game states
        self.target_mode = None
        self.target_index = 0
        self.target_x = None
        self.target_y = None
        self.log_messages = []

    def init_resources(self, no_emoji):
        if no_emoji:
            self.TILES = constants.TILES_ASCII
            self.CHARS = constants.CHARS_ASCII
        else:
            self.TILES = constants.TILES_EMOJI
            self.CHARS = constants.CHARS_EMOJI
        self.COLORS = constants.COLORS

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

    def get_available_weapons(self):
        return [cls() for cls in Weapon.__subclasses__()]

    def get_available_armor(self):
        return [cls() for cls in Armor.__subclasses__()]

    def get_available_items(self):
        return [
            cls()
            for cls in Item.__subclasses__()
            if cls.__name__ not in ["Weapon", "Armor"]
        ]

    def create_available_rooms(self):
        for _ in range(10):
            self.available_rooms.append(Room(self))

    def update_game_dimensions(self):
        self.screen_height, self.screen_width = self.stdscr.getmaxyx()
        self.map_width = self.screen_width - self.side_panel_width
        self.map_height = self.screen_height - 7  # 1 for status line, 3 for log

    def draw_map(self):
        self.current_room.draw(self.stdscr)

    def draw_entities(self):
        self.player.draw(self.stdscr)
        if isinstance(self.current_room, EnemiesMixin):
            self.current_room.draw_enemies(self.stdscr)

    def draw_side_panel(self):
        panel_x = self.map_width
        self.player.draw_status(self.stdscr, panel_x)
        if self.selected_enemy:
            self.selected_enemy.draw_status(self.stdscr, panel_x)
        self.draw_log()

    def draw_room_name(self):
        self.stdscr.addstr(0, 0, self.current_room.name, curses.color_pair(7))

    def draw_log(self):
        offset_y = 0
        if len(self.log_messages) < 3:
            offset_y = 3 - len(self.log_messages)

        log_start_y = self.screen_height - 5 + offset_y
        for i, message in enumerate(self.log_messages[-3:], 1):
            self.stdscr.addstr(log_start_y + i, 0, message, curses.color_pair(7))

    def add_log_message(self, message):
        self.log_messages.append(message)

    def enter_room(self, room):
        self.current_room = room
        self.current_room.was_entered = True
        self.current_room.position_player(self.player)
        self.add_log_message("Entered a room.")

    def exit_room(self, room):
        self.current_room = self.hallway
        for available_room in self.available_rooms:
            if available_room == room:
                self.player.x, self.player.y = available_room.hallway_entry
                break
        self.add_log_message("Entered the hallway.")

    def handle_input(self, key):
        if key == ord("q"):
            return False
        elif key == ord("f"):
            if isinstance(self.current_room, EnemiesMixin):
                self.player.target(self.current_room.enemies)
        elif key == ord("i"):
            selected_item = self.inventory.open_inventory(self.stdscr)
            if selected_item:
                selected_item.apply(self.player)

        self.player.handle_input(key, self)
        if isinstance(self.current_room, EnemiesMixin):
            self.current_room.move_enemies()
        return True

    def render(self):
        self.stdscr.clear()
        self.draw_map()
        self.status_line.draw()
        self.draw_entities()
        self.draw_room_name()
        self.draw_side_panel()
        self.stdscr.refresh()

    def game_loop(self):
        self.init_colors()
        self.create_available_rooms()
        self.add_log_message("Welcome to the dungeon!")

        while True:
            self.render()
            if not self.handle_input(self.stdscr.getch()):
                break
