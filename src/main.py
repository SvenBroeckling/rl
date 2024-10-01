#!/usr/bin/env python3
import curses
import sys

from game import Game


def main(stdscr, emoji):
    game = Game(stdscr, emoji)
    game.game_loop()


if __name__ == "__main__":
    emoji = False

    if len(sys.argv) > 1 and sys.argv[1] == "--emoji":
        no_emoji = True
    curses.wrapper(main, emoji)
