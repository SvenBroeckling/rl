import curses

from constants import TILES
from room_base import RoomBase


class Hallway(RoomBase):
    def generate(self):
        return [
            [TILES["hallway"] for x in range(self.width)] for y in range(self.height)
        ]

    @property
    def name(self):
        return "Hallway"

    def draw(self, stdscr):
        super().draw(stdscr)
        self.draw_room_entries()

    def draw_room_entries(self):
        for room in self.game.available_rooms:
            tile = TILES["door"]
            if room.was_entered:
                tile = TILES["door_explored"]
            if room.is_cleared:
                tile = TILES["door_cleared"]

            x, y = room.hallway_entry
            self.game.stdscr.addch(
                y + self.offset_y,
                x + self.offset_x,
                tile,
                curses.color_pair(3),
            )
