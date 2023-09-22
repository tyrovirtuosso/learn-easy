let reconnectInterval = 1000; // Initial reconnect interval in milliseconds

function connectWebSocket() {
    const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
    const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/user_item_notifications/`;
    
    const socket = new WebSocket(wsEndpoint);

    socket.onopen = () => {
        console.log("WebSocket user_item_notifications opened!");
        reconnectInterval = 1000; // Reset the reconnect interval on successful connection
    };

    socket.addEventListener("message", (event) => {
        console.log("Received WebSocket message:", event.data);
        const item = JSON.parse(event.data);

        if (item.type === "item_update") {
            // Find the list item with the matching ID or add a new one
            let listItem = document.querySelector(`#item-list li[data-id="${item.id}"]`);

            if (listItem) {
                // Check if category information is available
                if (item.category !== undefined && item.category !== null && item.category !== "") {
                    let categoryElement = listItem.querySelector(".category-value");
                    if (categoryElement) {
                        categoryElement.textContent = item.category;
                    }
                }

                // Check if meaning information is available
                if (item.meaning !== undefined && item.meaning !== null && item.meaning !== "") {
                    // Update the word link
                    let wordElement = listItem.querySelector(".word");
                    if (wordElement) {
                        wordElement.href = item.detail_url;
                    }

                    // Update the delete link
                    let deleteLink = listItem.querySelector(".delete-link");
                    if (deleteLink) {
                        deleteLink.textContent = "Delete";
                        deleteLink.href = item.delete_url;
                    }
                }
            } else {
                // Create a new list item if it doesn't exist
                listItem = document.createElement("li");
                listItem.setAttribute("data-id", item.id);
            
                // Create the child elements for the new list item
                const wordElement = document.createElement("a");
                wordElement.className = "word";
                wordElement.textContent = item.word;
                listItem.appendChild(wordElement);

                // Add the colon ":" after the word
                listItem.appendChild(document.createTextNode(": "));
            
                const categoryElement = document.createElement("span");
                categoryElement.className = "category-value";
                listItem.appendChild(categoryElement);

                // Add two spaces after the category value
                listItem.appendChild(document.createTextNode("  "));
            
                const deleteLink = document.createElement("a");
                deleteLink.className = "delete-link";
                listItem.appendChild(deleteLink);
            
                // Append the new list item to the list
                document.getElementById("item-list").appendChild(listItem);
            }
        }
    });

    socket.onerror = (error) => {
        console.error("WebSocket error:", error);
    };

    socket.onclose = (event) => {
        if (event.wasClean) {
            console.log("WebSocket connection closed cleanly, code=" + event.code + ", reason=" + event.reason);
        } else {
            console.error("WebSocket connection died, code=" + event.code);

            // Attempt to reconnect with exponential backoff
            setTimeout(connectWebSocket, reconnectInterval);
            reconnectInterval *= 2; // Double the reconnect interval for exponential backoff
        }
    };
}

// Initial WebSocket connection
connectWebSocket();
// socket.close();