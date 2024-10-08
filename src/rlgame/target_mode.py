import curses

from rlgame.colors import PlayerColor


class TargetMode:
    def __init__(self, enemies, game):
        self.enemies = enemies
        self.game = game
        self.game.status_line.set_status(
            "Target mode - n: switch target | f: attack | ESC: exit"
        )
        self.target_index = self.target_index_for_enemy(self.find_closest_enemy())
        self.select_target(self.enemies[self.target_index])

    def target_index_for_enemy(self, enemy):
        return self.enemies.index(enemy)

    def find_closest_enemy(self):
        closest_enemy = None
        closest_distance = 9999
        for enemy in self.enemies:
            distance = abs(enemy.x - self.game.player.x) + abs(
                enemy.y - self.game.player.y
            )
            if distance < closest_distance:
                closest_distance = distance
                closest_enemy = enemy
        return closest_enemy

    def select_target(self, enemy):
        self.target_x = enemy.x
        self.target_y = enemy.y
        if not self.game.player.has_line_of_sight(enemy):
            self.game.selected_enemy = None
        elif not self.game.player.is_in_attack_range(enemy.x, enemy.y):
            self.game.selected_enemy = None
        else:
            self.game.selected_enemy = enemy

    def next_target(self):
        self.target_index = (self.target_index + 1) % len(self.enemies)
        self.select_target(self.enemies[self.target_index])

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
            self.game.stdscr.refresh()
            key = self.game.stdscr.getch()
            if key in [ord("q"), 27]:
                self.disable()
                break
            if key == ord("n"):
                self.next_target()
            elif key == ord("f"):
                self.attack_target()
                self.disable()
                break

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
            if self.game.current_room.tiles[y][x].breaks_line_of_sight:
                break

            # respect attack range - stop drawing if we hit the maximum attack range
            if not self.game.player.is_in_attack_range(x, y):
                break

            if pos := self.game.current_room.get_map_position_in_viewport(x, y):
                x, y = pos
                self.game.stdscr.addch(
                    y,
                    x,
                    "*",
                    curses.color_pair(PlayerColor.pair_number) | curses.A_BOLD,
                )
