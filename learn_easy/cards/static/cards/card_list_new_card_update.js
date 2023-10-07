var socket = new WebSocket('ws://' + window.location.host + '/ws/cards/');
    
socket.onopen = function(e) {
    console.log("Connection opened!")
    socket.send(JSON.stringify({message: 'Hello, server!'}));
};

socket.onmessage = function(e) {
    console.log("message recieved")
    var data = JSON.parse(e.data);
    var cardName = data['card_name'];
    var cardId = data['card_id'];
    var cardTags = data['card_tags'];
    var cardDetailUrl = data['card_detail_url'];
    var deleteCardUrl = data['delete_card_url'];

    // Create the new card
    var li = document.createElement('li');
    li.dataset.id = cardId;

    var a = document.createElement('a');
    a.href = cardDetailUrl;
    a.textContent = cardName;
    li.appendChild(a);

    var spanCategory = document.createElement('span');
    spanCategory.className = 'category';
    var spanCategoryValue = document.createElement('span');
    spanCategoryValue.className = 'category-value';
    spanCategoryValue.textContent = cardTags.join(', ');
    spanCategory.appendChild(spanCategoryValue);
    li.appendChild(spanCategory);

    var spanActions = document.createElement('span');
    spanActions.className = 'actions';
    var aDelete = document.createElement('a');
    aDelete.href = deleteCardUrl;
    aDelete.className = 'delete-link';
    aDelete.textContent = 'Delete';
    aDelete.onclick = function() {
        return confirm('Are you sure you want to delete the card ' + cardName + '?');
    };
    spanActions.appendChild(aDelete);
    li.appendChild(spanActions);

    document.querySelector('#card-list').appendChild(li);
};

socket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};