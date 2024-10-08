#!/usr/bin/env python
import base64
import gzip
import os
import uuid
import atexit
from io import BytesIO

from flask import Flask, render_template, session
from flask_socketio import SocketIO
from flask_session import Session

from webcurses.wrapper import wrap_curses_app


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_sessions"
app.config["SESSION_PERMANENT"] = False

Session(app)
socketio = SocketIO(app, manage_session=False)

SESSION_APPS = {}


def compress_screen(screen):
    """
    Compresses the screen using gzip and returns the compressed screen
    as a base64 encoded string.
    """
    compressed_data = BytesIO()
    with gzip.GzipFile(fileobj=compressed_data, mode="wb") as f:
        f.write(screen.encode("utf-8"))  # Write the screen data as bytes

    return base64.b64encode(compressed_data.getvalue()).decode()


def screen_update_callback(screen):
    with app.app_context():
        socketio.emit("screen_update", {"screen": compress_screen(screen)})


def on_shutdown():
    for _, wrapper in SESSION_APPS.items():
        if wrapper.thread.is_alive():
            wrapper.thread.join()
    SESSION_APPS.clear()


# Register the shutdown function
atexit.register(on_shutdown)


@app.route("/")
def index():
    if "user_id" not in session:
        session["user_id"] = str(uuid.uuid4())
        print(f"Assigned new user ID: {session['user_id']}")
    else:
        print(f"User reconnected with ID: {session['user_id']}")
    return render_template("index.html")


@socketio.on("connect")
def connect(data):
    """Send the initial screen to the client."""

    if session["user_id"] not in SESSION_APPS:
        SESSION_APPS[session["user_id"]] = wrap_curses_app(
            "rlgame.game.Game",
            34,
            100,
            screen_update_callback=screen_update_callback,
            emoji=False,
        )


@socketio.on("resize")
def handle_resize(data):
    """Handle screen resize events."""
    width = data["width"]
    height = data["height"]
    # web_curses.resize(width, height)


@socketio.on("key_press")
def handle_key_press(data):
    """Handle key press events from the client."""
    SESSION_APPS[session["user_id"]].handle_key_press(data["key"])


def run_server():
    socketio.run(app, debug=True, port=5000, host="0.0.0.0")


if __name__ == "__main__":
    run_server()
