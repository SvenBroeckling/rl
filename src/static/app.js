let socket = io();
let terminalDiv = document.getElementById("terminal");

socket.on("connect", function () {
  socket.emit("connected", { data: "I'm connected!" });
  socket.emit("key_press", { key: " " });
});

socket.on("disconnect", function () {
  let terminalDiv = document.getElementById("terminal");
  terminalDiv.innerHTML = "Disconnected from server";
});

// Send initial screen size to server
function sendResizeEvent() {
  socket.emit("resize", {
    width: Math.floor(window.innerWidth / 10), // Approximate width in characters
    height: Math.floor(window.innerHeight / 20), // Approximate height in characters
  });
}

// Update terminal display
socket.on("screen_update", function (data) {
  let compressedData = Uint8Array.from(atob(data.screen), c => c.charCodeAt(0));
  let screenData = pako.inflate(compressedData, { to: "string" });
  terminalDiv.innerHTML = screenData;
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
