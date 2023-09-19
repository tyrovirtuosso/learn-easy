const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/notifications/`;
const socket = new WebSocket(wsEndpoint);


socket.addEventListener("message", (event) => {
  const messageData = JSON.parse(event.data);
  console.log("Received notification:", messageData.message); // Log the received message to the console

  // If a new word is saved, add it to the list
  if (messageData.message.includes("Word") && messageData.message.includes("saved")) {
    const itemList = document.querySelector('ul');
    const newItem = document.createElement('li');
    newItem.id = `item-${messageData.item_id}`;
    newItem.innerHTML = `${messageData.word} <span class="category"></span>`;
    itemList.appendChild(newItem);
  }
  
  // Update category in item list
  if (messageData.item_id && messageData.category) {
    const itemElement = document.getElementById(`item-${messageData.item_id}`);
    if (itemElement) {
        const categoryElement = itemElement.querySelector('.category');
        if (categoryElement) 
        {
            categoryElement.textContent = messageData.category;
            // Add link to item detail and delete link after category is updated
            itemElement.innerHTML = `<a href="/items/item/${messageData.item_id}/">${messageData.word}</a> - <span class="category">${messageData.category}</span> 
                                     <a href="/items/delete/${messageData.item_id}/" onclick="return confirm('Are you sure you want to delete the item ${messageData.word}?')">Delete</a>`;
            // Refresh the page
            location.reload();
        }
    }
}
});

socket.onopen = (event) => {
  console.log("WebSocket connection opened!");
};

socket.onclose = (event) => {
  console.log("WebSocket connection closed!");
};