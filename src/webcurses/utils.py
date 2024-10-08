from .constants import KEY_MAP, HTML_COLOR_CLASSES


def get_key_code(key: str) -> int | None:
    """
    Gets the integer key code for the provided key.
    """
    if key in KEY_MAP:
        return KEY_MAP[key]

    try:
        if len(key) == 1:
            return ord(key)
    except TypeError:
        pass

    return 0


def html_color_class_name_to_hex(color_class_name):
    """Convert an HTML color class name to a hex color code."""
    if color_class_name.startswith("rgb-"):
        _, r, g, b = color_class_name.split("-")
        r = int(r)
        g = int(g)
        b = int(b)
        r = (r * 51) // 255
        g = (g * 51) // 255
        b = (b * 51) // 255
        return f"#{r:02x}{g:02x}{b:02x}"
    elif color_class_name.startswith("gray-"):
        gray = int(color_class_name.split("-")[1])
        gray = (gray * 255) // 100
        return f"#{gray:02x}{gray:02x}{gray:02x}"
    elif color_class_name.startswith("bright-"):
        return html_color_class_name_to_hex(color_class_name[7:])
    else:
        return color_class_name


def curses_color_pair_to_html_color_pair(curses_color_pair):
    """Convert a curses color pair to an HTML color pair."""
    fg, bg = curses_color_pair
    fg = html_color_class_name_to_hex(HTML_COLOR_CLASSES[fg])
    bg = html_color_class_name_to_hex(HTML_COLOR_CLASSES[bg])
    return fg, bg
