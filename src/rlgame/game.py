import curses

from . import constants
from .colors import ColorBase, PlayerColor, UIColor

from .hallway import Hallway
from .info_line import InfoLine
from .items import Armor, Item, Weapon
from .player import Player
from .rooms import Room
from .status_line import StatusLine


class Game:
    def __init__(self, stdscr, emoji=False):
        self.init_curses(stdscr)
        self.init_colors()

        self.emoji = emoji
        self.challenge_rating = 1

        self.status_line = StatusLine(self)
        self.info_line = InfoLine(self)
        self.log_messages = []
        self.log_offset = None

        self.hallway = Hallway(self)
        self.current_room = self.hallway
        self.available_rooms = []

        self.player = Player(
            self,
            self.current_room.width // 2,
            self.current_room.height - 2,
            shooting_skill=2,
        )
        self.player.set_starting_equipment(min_tier=1, max_tier=1)
        self.selected_enemy = None

    def init_curses(self, stdscr):
        self.stdscr = stdscr
        curses.curs_set(0)
        self.side_panel_width = 35
        self.screen_height, self.screen_width = stdscr.getmaxyx()
        self.viewport_width = self.screen_width - self.side_panel_width
        self.viewport_height = (
            self.screen_height - 6
        )  # 1 for status line, 1 for info, 4 for log

    def init_colors(self):
        curses.start_color()
        for color in ColorBase.__subclasses__():
            color().curses_init_pair()

    @staticmethod
    def get_available_weapons(tier_min=1, tier_max=9):
        return [
            cls() for cls in Weapon.__subclasses__() if tier_min <= cls.tier <= tier_max
        ]

    @staticmethod
    def get_available_armor(tier_min=1, tier_max=9):
        return [
            cls() for cls in Armor.__subclasses__() if tier_min <= cls.tier <= tier_max
        ]

    @staticmethod
    def get_available_items(tier_min=1, tier_max=9):
        return [
            cls()
            for cls in Item.__subclasses__()
            if cls.__name__ not in ["Weapon", "Armor"]
            and tier_min <= cls.tier <= tier_max
        ]

    def create_available_rooms(self):
        for _ in range(constants.ROOMS_PER_LEVEL):
            self.available_rooms.append(Room(self))

    def draw_side_panel(self):
        panel_x = self.viewport_width
        self.player.draw_status(self.stdscr, panel_x)
        if self.selected_enemy:
            self.selected_enemy.draw_status(self.stdscr, panel_x)

    def draw_room_name(self):
        s = f"{self.current_room.name} - Challenge Rating {self.current_room.challenge_rating}"
        self.stdscr.addstr(
            0, 0, s, curses.color_pair(UIColor.pair_number) | curses.A_BOLD
        )

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

        for i, (message, color_pair) in enumerate(shown_messages_with_offset, 1):
            self.stdscr.addstr(
                log_start_y + i, 0, message, curses.color_pair(color_pair)
            )

    def add_log_message(self, message, color_pair=None):
        if not color_pair:
            color_pair = UIColor.pair_number
        self.log_messages.append((message, color_pair))
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
        self.current_room.move_enemies()
        return True

    def render(self):
        self.stdscr.clear()
        self.current_room.draw(self.stdscr)
        self.status_line.draw()
        self.info_line.draw()
        self.player.draw(self.stdscr)
        self.draw_room_name()
        self.draw_side_panel()
        self.draw_log()
        self.stdscr.refresh()

    def restart_game(self):
        self.__init__(self.stdscr, emoji=self.emoji)
        self.add_log_message("Game restarted, obviously. You died.")
        self.game_loop()

    def game_loop(self):
        self.create_available_rooms()
        self.add_log_message("Welcome to the dungeon!")
        self.add_log_message(
            f"Clear {constants.ROOMS_PER_LEVEL} rooms to advance to the next level."
        )
        self.add_log_message(
            "There is an enemy in the hallway. Use 'f' to target it, and 'f' again to shoot."
        )

        while True:
            self.render()
            if not self.handle_input(self.stdscr.getch()):
                break
