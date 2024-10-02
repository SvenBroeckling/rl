#!/usr/bin/env python

from flask import Flask, render_template
from flask_socketio import SocketIO

from webcurses.webcurses import wrap_curses_app


app = Flask(__name__)
socketio = SocketIO(app)


def screen_update_callback(screen):
    with app.app_context():
        socketio.emit("screen_update", {"screen": screen})


wrapper = wrap_curses_app(
    "rlgame.game.Game",
    34,
    100,
    screen_update_callback=screen_update_callback,
    emoji=False,
)


@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("connect")
def connect(data):
    """Send the initial screen to the client."""


@socketio.on("resize")
def handle_resize(data):
    """Handle screen resize events."""
    width = data["width"]
    height = data["height"]
    # web_curses.resize(width, height)


@socketio.on("key_press")
def handle_key_press(data):
    """Handle key press events from the client."""
    key = data["key"]
    wrapper.handle_key_press(key)


def run_server():
    socketio.run(app, debug=True)


if __name__ == "__main__":
    run_server()
