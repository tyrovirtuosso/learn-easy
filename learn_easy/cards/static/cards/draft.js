const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/notifications/`;
const socket = new WebSocket(wsEndpoint);


socket.addEventListener("message", (event) => {
  const messageData = JSON.parse(event.data);
  console.log("Received notification:", messageData.message); // Log the received message to the console


    // Create a new list item
    const newItem = document.createElement("li");

    // If the category is not yet available, just show the word
    if (!messageData.category) {
      newItem.textContent = messageData.word;
    } else {
      // If the category is available, make the word a link and show the category
      newItem.innerHTML = `<a href="/items/item/${messageData.item_id}/">${messageData.word}</a> <span>${messageData.category}</span> <a href="/items/delete/${messageData.item_id}/" onclick="return confirm('Are you sure you want to delete the item ${messageData.word}?')">Delete</a>`;
      
      // Refresh the page
      location.reload();
    }

    // Add the new item to the list
    document.querySelector("#item-list").appendChild(newItem);
    
    });



//   // If a new word is saved, add it to the list
//   if (messageData.message.includes("Word") && messageData.message.includes("saved")) {
//     const itemList = document.querySelector('ul');
//     const newItem = document.createElement('li');
//     newItem.id = `item-${messageData.item_id}`;
//     newItem.innerHTML = `${messageData.word} <span class="category"></span>`;
//     itemList.appendChild(newItem);
//   }
  
//   // Update category in item list
//   if (messageData.item_id && messageData.category) {
//     const itemElement = document.getElementById(`item-${messageData.item_id}`);
//     if (itemElement) {
//         const categoryElement = itemElement.querySelector('.category');
//         if (categoryElement) 
//         {
//             categoryElement.textContent = messageData.category;
//             // Add link to item detail and delete link after category is updated
//             itemElement.innerHTML = `<a href="/items/item/${messageData.item_id}/">${messageData.word}</a> - <span class="category">${messageData.category}</span> 
//                                      <a href="/items/delete/${messageData.item_id}/" onclick="return confirm('Are you sure you want to delete the item ${messageData.word}?')">Delete</a>`;
//             // Refresh the page
//             location.reload();
//         }
//     }
// }
// });

socket.onopen = (event) => {
  console.log("WebSocket connection opened!");
};

socket.onclose = (event) => {
  console.log("WebSocket connection closed!");
};