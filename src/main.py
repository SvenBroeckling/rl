#!/usr/bin/env python3
import curses

from game import Game


def main(stdscr):
    game = Game(stdscr)
    game.game_loop()


if __name__ == "__main__":
    curses.wrapper(main)
