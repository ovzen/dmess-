'use strict';

(function init(){

    function createMessageNode(text) {
        let msgText = document.createElement('div');
        msgText.className = 'card-text';
        msgText.textContent = text;
        let msgBody = document.createElement('div');
        msgBody.className = 'card-body msg-body';
        let msgCard = document.createElement('div');
        msgCard.className = 'card text-white bg-primary';
        let msgRow = document.createElement('div');
        msgRow.className = 'row';
        let msgContainer = document.createElement('div');
        msgContainer.className = 'container msg-container';
        msgBody.append(msgText);
        msgCard.append(msgBody);
        msgRow.append(msgCard);
        msgContainer.append(msgRow);
        return msgContainer;
    }

    let msgArea = document.getElementById('messageArea');
    let msgForSend = document.getElementById('msgForSend');
    let sendButton = document.getElementById('sendButton');
    msgForSend.focus()

// TODO: make diolog groups
//    var chatSocket = new WebSocket(
//        'ws://' + window.location.host +
//        '/ws/chat/' + roomName + '/');

    let chatSocket = new WebSocket('ws://' + window.location.host + '/ws/chat/');

    chatSocket.onmessage = function(message) {
        let data = JSON.parse(message.data);
        let newMessage = createMessageNode(data.message);
        msgArea.prepend(newMessage);
    }

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

     msgForSend.onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            sendButton.click();
        }
    };

    sendButton.onclick = function(e) {
        if (msgForSend.value) {
            chatSocket.send(JSON.stringify({
                'message': msgForSend.value
            }));
            msgForSend.value = '';
        }
    }
}());