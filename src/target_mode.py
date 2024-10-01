import curses


class TargetMode:
    def __init__(self, enemies, game):
        self.enemies = enemies
        self.target_index = 0
        self.game = game
        self.target = 0
        self.game.status_line.set_status(
            "Target mode - Tab: switch target | f: attack | ESC: exit"
        )
        self.target_x = enemies[self.target_index].x
        self.target_y = enemies[self.target_index].y
        if self.has_line_of_sight(self.target_x, self.target_y):
            self.game.selected_enemy = enemies[self.target_index]

    def select_target(self):
        self.target_index = (self.target_index + 1) % len(self.enemies)
        self.target_x = self.enemies[self.target_index].x
        self.target_y = self.enemies[self.target_index].y
        if self.has_line_of_sight(self.target_x, self.target_y):
            self.game.selected_enemy = self.enemies[self.target_index]
        else:
            self.game.selected_enemy = None

    def attack_target(self):
        if not self.game.selected_enemy:
            self.game.add_log_message("No line of sight to target.")
            self.disable()
            return
        self.game.selected_enemy = self.enemies[self.target_index]
        self.game.player.attack(self.game.selected_enemy)
        self.disable()

    def disable(self):
        self.game.target_mode = None
        self.game.selected_enemy = None
        self.game.status_line.reset_status()

    def input_loop(self):
        self.game.target_mode = self
        while True:
            self.game.render()
            self.draw_target_line()
            key = self.game.stdscr.getch()
            if key in [ord("q"), 27]:
                self.disable()
                break
            if key == ord("\t"):
                self.select_target()
            elif key == ord("f"):
                self.attack_target()
                self.disable()
                break

    def has_line_of_sight(self, x, y):
        dx = x - self.game.player.x
        dy = y - self.game.player.y

        steps = max(abs(dx), abs(dy))
        for i in range(1, steps):
            x = self.game.player.x + int(i * dx / steps)
            y = self.game.player.y + int(i * dy / steps)

            if self.game.current_room.tiles[y][x] in [
                self.game.TILES["wall"],
            ]:
                return False
        return True

    def draw_target_line(self):
        if not self.game.target_mode:
            return
        dx = self.target_x - self.game.player.x
        dy = self.target_y - self.game.player.y

        steps = max(abs(dx), abs(dy))
        for i in range(1, steps):
            x = self.game.player.x + int(i * dx / steps)
            y = self.game.player.y + int(i * dy / steps)

            # respect line of sight - stop drawing if we hit a wall or obstacle
            if self.game.current_room.tiles[y][x] in [
                self.game.TILES["wall"],
            ]:
                break

            self.game.stdscr.addch(
                y + self.game.current_room.offset_y,
                x + self.game.current_room.offset_x,
                self.game.TILES["target_line"],
                curses.color_pair(self.game.COLORS["player"]),
            )
