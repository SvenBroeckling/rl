import queue
import threading

from .thread import CursesThread, CursesThreadWrapper


def wrap_curses_app(
    curses_app_class_name: str,
    lines: int,
    columns: int,
    screen_update_callback=None,
    **app_kwargs,
):
    """
    Wrap a curses app in a Flask server.

    :param curses_app_class_name: The class of the curses app to run in dot notation.
    :param lines: The number of lines in the terminal.
    :param columns: The number of columns in the terminal.
    :param screen_update_callback: A callback function to call when the screen is updated.
    :param app_kwargs: Additional keyword arguments to pass to the curses app.
    """

    key_event = threading.Event()
    resize_event = threading.Event()
    key_queue = queue.Queue()
    thread = CursesThread(
        curses_app_class_name,
        key_event,
        resize_event,
        key_queue,
        lines,
        columns,
        screen_update_callback=screen_update_callback,
        **app_kwargs,
    )
    wrapper = CursesThreadWrapper(thread, key_event, resize_event, key_queue)
    threading.Thread(target=thread.run).start()
    return wrapper
