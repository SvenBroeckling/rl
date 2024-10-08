import curses

from .enemies import TutorialEnemy
from .room_base import RoomBase
from .room_generators import HallwayGenerator
from .tiles import DoorTile


class Hallway(RoomBase):
    def __init__(self, game, **kwargs):
        super().__init__(game, **kwargs)

    @property
    def generator(self):
        return HallwayGenerator(game=self.game, width=self.width, height=self.height)

    @property
    def name(self):
        return "Hallway"

    def set_challenge_rating(self):
        self.challenge_rating = 1

    def create_enemies(self):
        new_enemy = TutorialEnemy(
            game=self.game,
            x=self.width // 2,
            y=1,
            speed=1,
            health=3,
            shooting_skill=1,
            room=self,
        )
        new_enemy.reputation = 1
        new_enemy.set_starting_equipment(min_tier=1, max_tier=1)
        self.enemies = [new_enemy]

    def draw(self, stdscr):
        super().draw(stdscr)
        self.draw_room_entries()
        self.draw_enemies(stdscr)

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
                    curses.color_pair(tile.color),
                )
