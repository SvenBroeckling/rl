import curses

from . import constants
from .hallway import Hallway
from .items import Armor, Item, Weapon
from .mixins import RoomWithEnemiesMixin
from .player import Player
from .rooms import Room
from .status_line import StatusLine


class Game:
    def __init__(self, stdscr, emoji=False):
        self.init_curses(stdscr)
        self.init_resources(emoji)

        self.status_line = StatusLine(self)

        self.hallway = Hallway(self)
        self.current_room = self.hallway
        self.available_rooms = []

        self.player = Player(
            self, self.current_room.width // 2, self.current_room.height // 2
        )
        self.player.set_starting_equipment()
        self.selected_enemy = None

        self.log_messages = []
        self.log_offset = None

    def init_curses(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.side_panel_width = 35
        self.screen_height, self.screen_width = stdscr.getmaxyx()
        self.map_width = self.screen_width - self.side_panel_width
        self.map_height = self.screen_height - 8  # 1 for status line, 4 for log

    def init_resources(self, emoji):
        self.available_items = self.get_available_items()
        self.available_weapons = self.get_available_weapons()
        self.available_armor = self.get_available_armor()

        if emoji:
            self.TILES = constants.TILES_EMOJI
            self.CHARS = constants.CHARS_EMOJI
        else:
            self.TILES = constants.TILES_ASCII
            self.CHARS = constants.CHARS_ASCII
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

    def draw_map(self):
        self.current_room.draw(self.stdscr)

    def draw_entities(self):
        self.player.draw(self.stdscr)
        if isinstance(self.current_room, RoomWithEnemiesMixin):
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
        if len(self.log_messages) < 4:
            offset_y = 4 - len(self.log_messages)

        log_start_y = self.screen_height - 6 + offset_y

        shown_messages_with_offset = self.log_messages[-4:]
        if self.log_offset is not None:
            shown_messages_with_offset = self.log_messages[
                self.log_offset : self.log_offset + 4
            ]

        for i, message in enumerate(shown_messages_with_offset, 1):
            self.stdscr.addstr(log_start_y + i, 0, message, curses.color_pair(7))

    def add_log_message(self, message):
        self.log_messages.append(message)
        self.deactivate_log_offset()

    def increase_log_offset(self):
        if self.log_offset is None:
            self.log_offset = 0
        elif self.log_offset + 4 < len(self.log_messages):
            self.log_offset += 1

    def decrease_log_offset(self):
        if self.log_offset is None:
            self.log_offset = len(self.log_messages) - 4
        elif self.log_offset is not None and self.log_offset > 0:
            self.log_offset -= 1

    def deactivate_log_offset(self):
        self.log_offset = None

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
        if key == curses.KEY_UP:
            self.decrease_log_offset()
        elif key == curses.KEY_DOWN:
            self.increase_log_offset()
        elif key == ord("q"):
            return False

        elif key == ord("i"):
            selected_item = self.player.inventory.open_inventory(self.stdscr)
            if selected_item:
                selected_item.apply(self.player)

        self.player.handle_input(key)
        if isinstance(self.current_room, RoomWithEnemiesMixin):
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
