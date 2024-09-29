from rooms import Room
from tiles import TILES


class Hallway:
    def __init__(self, map_width, map_height):
        self.map_width = map_width
        self.map_height = map_height
        self.tiles = self.generate()

    def generate(self):
        # Generates the overworld map with doors leading to rooms
        overworld = [
            [
                TILES["hallway"] if x % 5 != 0 or y % 5 != 0 else TILES["door"]
                for x in range(self.map_width)
            ]
            for y in range(self.map_height)
        ]
        return overworld

    def draw(self, stdscr):
        for y, row in enumerate(self.tiles):
            for x, tile in enumerate(row):
                if tile == TILES["hallway"]:
                    stdscr.addch(y, x, tile)
                elif tile == TILES["door"]:
                    stdscr.addch(y, x, tile)
