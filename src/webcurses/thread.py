import sys
import threading

from webcurses.webcurses import WebCurses


class CursesThreadWrapper:
    def __init__(
        self,
        thread,
        key_event,
        resize_event,
        key_queue,
    ):
        self.thread = thread
        self.key_event = key_event
        self.resize_event = resize_event
        self.key_queue = key_queue

    def handle_key_press(self, key):
        self.thread.key_queue.put(key)
        self.thread.key_event.set()

    def handle_resize(self, width, height):
        self.thread.web_curses.resize(width, height)
        self.thread.resize_event.set()


class CursesThread(threading.Thread):
    def __init__(
        self,
        curses_app_class_name,
        key_event,
        resize_event,
        key_queue,
        lines,
        columns,
        screen_update_callback=None,
        **kwargs,
    ):
        super().__init__()
        self.curses_app_class_name = curses_app_class_name
        self.web_curses = WebCurses(
            self, lines, columns, screen_update_callback=screen_update_callback
        )
        self.install_web_curses()

        self.resize_event = resize_event
        self.key_queue = key_queue
        self.curses_app = self.get_app_class()(self.web_curses.stdscr, **kwargs)
        self.key_event = key_event

    def install_web_curses(self):
        sys.modules["curses"] = self.web_curses

    def get_app_class(self):
        # import the curses_app_class_name by dot notation name
        module_name, class_name = self.curses_app_class_name.rsplit(".", 1)
        return __import__(module_name, fromlist=[class_name]).__dict__[class_name]

    def run(self):
        self.curses_app.game_loop()
