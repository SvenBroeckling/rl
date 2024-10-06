import curses

from .room_base import RoomBase
from .room_generators import HallwayGenerator
from .tiles import DoorTile


class Hallway(RoomBase):

    @property
    def generator(self):
        return HallwayGenerator(game=self.game, width=self.width, height=self.height)

    @property
    def name(self):
        return "Hallway"

    def draw(self, stdscr):
        super().draw(stdscr)
        self.draw_room_entries()

    def draw_room_entries(self):
        for room in self.game.available_rooms:
            tile = DoorTile(self.game)
            if room.was_entered:
                tile = DoorTile(self.game, cleared=True)
            if room.is_cleared:
                tile = DoorTile(self.game, visited=True)

            if pos := self.get_map_position_in_viewport(*room.hallway_entry):
                x, y = pos
                self.game.stdscr.addch(
                    y,
                    x,
                    tile.char,
                    tile.color,
                )
