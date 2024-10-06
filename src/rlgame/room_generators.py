import random

from rlgame.tiles import FloorTile, WallTile, ObstacleTile


class RoomGeneratorBase:
    def __init__(self, game, width, height):
        self.width = width
        self.height = height
        self.game = game

    def generate_room(self) -> list[list[str]]:
        raise NotImplementedError(
            "generate_room method must be implemented in subclass"
        )


class HallwayGenerator(RoomGeneratorBase):

    def generate_room(self) -> list[list["TileBase"]]:
        return [
            [FloorTile(self.game) for _ in range(self.width)]
            for _ in range(self.height)
        ]


class SingleRoomGenerator(RoomGeneratorBase):
    def generate_room(self) -> list[list[str]]:
        tiles = self.generate_floor()
        tiles = self.generate_obstacles(tiles)
        tiles = self.generate_walls(tiles)
        return tiles

    def generate_floor(self):
        return [
            [FloorTile(self.game) for _ in range(self.width)]
            for _ in range(self.height)
        ]

    def generate_walls(self, tiles):
        amount = self.width * self.height // 80
        for _ in range(amount):
            x = random.randint(1, self.width - 5)
            y = random.randint(1, self.height - 5)
            length = random.randint(3, 5)
            vertical = random.random() > 0.5
            for i in range(length):
                if vertical:
                    tiles[y + i][x] = WallTile(self.game)
                else:
                    tiles[y][x + i] = WallTile(self.game)
        return tiles

    def generate_obstacles(self, tiles):
        amount = self.width * self.height // 50

        for _ in range(amount):
            x = random.randint(1, self.width - 5)
            y = random.randint(1, self.height - 5)
            width = random.randint(3, 5)
            height = random.randint(3, 5)
            for i in range(y, y + height):
                for j in range(x, x + width):
                    if random.random() > 0.5:
                        tiles[i][j] = ObstacleTile(self.game)
        return tiles
