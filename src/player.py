import curses


PLAYER_CHAR = "@"
COLOR_PLAYER = 1


class Player:
    def __init__(self, x, y, game):
        self.x = x
        self.y = y
        self.game = game
        self.char = PLAYER_CHAR
        self.speed = 1
        self.health = 10
        self.target_mode = False
        self.target_index = 0
        self.target_x = None
        self.target_y = None

    @property
    def offset_x(self):
        return (self.game.map_width - self.game.current_room.width) // 2

    @property
    def offset_y(self):
        return (self.game.map_height - self.game.current_room.height) // 2

    def draw(self, stdscr):
        stdscr.addch(
            self.y + self.offset_y,
            self.x + self.offset_x,
            self.char,
            curses.color_pair(COLOR_PLAYER),
        )

    def draw_status(self, stdscr, panel_x):
        status_y = 1
        stdscr.addstr(
            status_y,
            panel_x + 1,
            "Status",
            curses.color_pair(COLOR_PLAYER) | curses.A_BOLD,
        )
        stdscr.addstr(
            status_y + 1,
            panel_x + 1,
            f"Health: {self.health}",
            curses.color_pair(COLOR_PLAYER),
        )
        stdscr.addstr(
            status_y + 2,
            panel_x + 1,
            f"Speed: {self.speed}",
            curses.color_pair(COLOR_PLAYER),
        )
        stdscr.addstr(
            status_y + 3,
            panel_x + 1,
            f"Pos: ({self.x},{self.y})",
            curses.color_pair(COLOR_PLAYER),
        )

    def move(self, dx, dy, game):
        new_x = self.x + dx
        new_y = self.y + dy

        if (
            0 <= new_x < game.current_room.width
            and 0 <= new_y < game.current_room.height
        ):
            if game.current_room is game.hallway:
                for room in game.available_rooms:
                    if (new_x, new_y) == room.hallway_entry:
                        self.game.enter_room(room)
                        return
            self.x = new_x
            self.y = new_y

    def toggle_target_mode(self, enemies):
        self.target_mode = not self.target_mode
        if self.target_mode and enemies:
            self.target_index = 0
            self.target_x = enemies[self.target_index].x
            self.target_y = enemies[self.target_index].y

    def handle_target_mode(self, key, enemies):
        if key == ord("\t"):
            self.target_index = (self.target_index + 1) % len(enemies)
            self.target_x = enemies[self.target_index].x
            self.target_y = enemies[self.target_index].y
        elif key == ord("h"):
            self.target_x = max(0, self.target_x - 1)
        elif key == ord("j"):
            self.target_y = min(len(enemies) - 1, self.target_y + 1)
        elif key == ord("k"):
            self.target_y = max(0, self.target_y - 1)
        elif key == ord("l"):
            self.target_x = min(len(enemies) - 1, self.target_x + 1)

    def handle_input(self, key, game):
        if key == ord("h"):
            self.move(-1, 0, game)
        elif key == ord("j"):
            self.move(0, 1, game)
        elif key == ord("k"):
            self.move(0, -1, game)
        elif key == ord("l"):
            self.move(1, 0, game)
