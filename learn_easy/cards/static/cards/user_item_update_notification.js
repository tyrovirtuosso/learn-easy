let reconnectInterval = 1000; // Initial reconnect interval in milliseconds

function connectWebSocket() {
    const websocketProtocol = window.location.protocol === "https:" ? "wss" : "ws";
    const wsEndpoint = `${websocketProtocol}://${window.location.host}/ws/user_card_notifications/`;
    
    const socket = new WebSocket(wsEndpoint);

    socket.onopen = () => {
        console.log("WebSocket user_card_notifications opened!");
        reconnectInterval = 1000; // Reset the reconnect interval on successful connection
    };

    socket.addEventListener("message", (event) => {
        console.log("Received WebSocket message:", event.data);
        const card = JSON.parse(event.data);

        if (card.type === "card_update") {
            // Find the list card with the matching ID or add a new one
            let listCard = document.querySelector(`#card-list li[data-id="${card.id}"]`);

            if (listCard) {
                // Check if category information is available
                if (card.category !== undefined && card.category !== null && card.category !== "") {
                    let categoryElement = listCard.querySelector(".category-value");
                    if (categoryElement) {
                        categoryElement.textContent = card.category;
                    }
                }

                // Check if meaning information is available
                if (card.meaning !== undefined && card.meaning !== null && card.meaning !== "") {
                    // Update the word link
                    let wordElement = listCard.querySelector(".word");
                    if (wordElement) {
                        wordElement.href = card.detail_url;
                    }

                    // Update the delete link
                    let deleteLink = listCard.querySelector(".delete-link");
                    if (deleteLink) {
                        deleteLink.textContent = "Delete";
                        deleteLink.href = card.delete_url;
                    }
                }
            } else {
                // Create a new list card if it doesn't exist
                listCard = document.createElement("li");
                listCard.setAttribute("data-id", card.id);
            
                // Create the child elements for the new list card
                const wordElement = document.createElement("a");
                wordElement.className = "word";
                wordElement.textContent = card.word;
                listCard.appendChild(wordElement);

                // Add the colon ":" after the word
                listCard.appendChild(document.createTextNode(": "));
            
                const categoryElement = document.createElement("span");
                categoryElement.className = "category-value";
                listCard.appendChild(categoryElement);

                // Add two spaces after the category value
                listCard.appendChild(document.createTextNode("  "));
            
                const deleteLink = document.createElement("a");
                deleteLink.className = "delete-link";
                listCard.appendChild(deleteLink);
            
                // Append the new list card to the list
                document.getElementById("card-list").appendChild(listCard);
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