import curses

from .room_base import RoomBase


class Hallway(RoomBase):
    def generate(self):
        return [
            [self.game.TILES["hallway"] for _ in range(self.width)]
            for _ in range(self.height)
        ]

    @property
    def name(self):
        return "Hallway"

    def draw(self, stdscr):
        super().draw(stdscr)
        self.draw_room_entries()

    def draw_room_entries(self):
        for room in self.game.available_rooms:
            tile = self.game.TILES["door"]
            if room.was_entered:
                tile = self.game.TILES["door_explored"]
            if room.is_cleared:
                tile = self.game.TILES["door_cleared"]

            x, y = room.hallway_entry
            self.game.stdscr.addch(
                y + self.offset_y,
                x + self.offset_x,
                tile,
                curses.color_pair(3),
            )
