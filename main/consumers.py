from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from main.models import Message, Dialog


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.chat_number = self.scope['url_route']['kwargs']['chat_number']
        self.chat_id = 'chat_%s' % self.chat_number

        # Join dialog group
        async_to_sync(self.channel_layer.group_add)(
            self.chat_id,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave dialog group
        async_to_sync(self.channel_layer.group_discard)(
            self.chat_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        author = self.scope["user"]
        if author == "":
            author = 'AnonymousUser'

        message_obj = Message(user=author, text=message, dialog_id=self.chat_number)
        message_obj.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_id,
            {
                'type': 'chat_message',
                'message': message,
                'author': author.username
            }
        )

    # Receive message from dialog group
    def chat_message(self, event):
        message = event['message']
        author = event['author']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'author': author
        }))
