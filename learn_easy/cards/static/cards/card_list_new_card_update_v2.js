var socket = new WebSocket('ws://' + window.location.host + '/ws/cards/');

socket.onopen = function(e) {
    console.log("Connection opened!")
    socket.send(JSON.stringify({message: 'Hello, server!'}));
};

socket.onmessage = function(e) {
    console.log("message recieved")
    var data = JSON.parse(e.data);
    var message = data['message'];
    if (message['event'] === 'New Card') {
        location.reload();
    }
};

socket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};