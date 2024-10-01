#!/usr/bin/env python3
import curses
import sys

from game import Game


def main(stdscr, no_emoji):
    game = Game(stdscr, no_emoji)
    game.game_loop()


if __name__ == "__main__":
    no_emoji = False

    if len(sys.argv) > 1 and sys.argv[1] == "--no-emoji":
        no_emoji = True
    curses.wrapper(main, no_emoji)
