const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/notifications/`;
const socket = new WebSocket(wsEndpoint);

// New event listener to capture incoming messages
socket.addEventListener("message", (event) => {
const messageData = JSON.parse(event.data);
console.log("Received notification:", messageData.message); // Log the received message to the console
showNotification(messageData.message);
});

function showNotification(notificationHTML) {
const notificationsContainer = document.getElementById("notifications");

// Create a new alert div
const alertDiv = document.createElement("div");
alertDiv.innerHTML = notificationHTML;

// Create the close button
const closeButton = document.createElement("button");
alertDiv.appendChild(closeButton);

notificationsContainer.appendChild(alertDiv);
}

socket.onopen = (event) => {
console.log("WebSocket connection opened!");
};

socket.onclose = (event) => {
console.log("WebSocket connection closed!");
};