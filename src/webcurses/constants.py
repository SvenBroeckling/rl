HTML_COLOR_CLASSES = [
    "black",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "white",
]

# Bright colors

HTML_COLOR_CLASSES += [f"bright-{color}" for color in HTML_COLOR_CLASSES]

# Extended 6x6x6 cube colors (R, G, B values)
# Algorithm to calculate the color code:
# 16 + 36 * R + 6 * G + B
# where R, G, B are in [0, 5]

HTML_COLOR_CLASSES += [
    f"rgb-{r}-{g}-{b}" for r in range(6) for g in range(6) for b in range(6)
]

# Grayscale colors
HTML_COLOR_CLASSES += [f"gray-{i}" for i in range(8, 238, 10)]
