var socket = io();

socket.on("connect", function () {
  socket.emit("connected", { data: "I'm connected!" });
});

var terminalDiv = document.getElementById("terminal");

// Send initial screen size to server
function sendResizeEvent() {
  socket.emit("resize", {
    width: Math.floor(window.innerWidth / 10), // Approximate width in characters
    height: Math.floor(window.innerHeight / 20), // Approximate height in characters
  });
}

// Update terminal display
socket.on("screen_update", function (data) {
  terminalDiv.innerHTML = data.screen;
});

// Capture key presses and send to server
window.addEventListener("keydown", function (event) {
  socket.emit("key_press", { key: event.key });
});

// Handle window resize
window.addEventListener("resize", function () {
  sendResizeEvent();
});

// Send initial resize event on load
sendResizeEvent();
