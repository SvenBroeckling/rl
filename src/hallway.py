import curses

from room_base import RoomBase
from tiles import TILES


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
            x, y = room.hallway_entry
            self.game.stdscr.addch(
                y + self.offset_y,
                x + self.offset_x,
                TILES["door"],
                curses.color_pair(3),
            )
