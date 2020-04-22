from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
import json

from main.models import Message, Dialog, UserProfile


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
                'author': author.username,
                'create_date': message_obj.create_date
            }
        )

    # Receive message from dialog group
    def chat_message(self, event):
        message = event['message']
        author = event['author']
        create_date = event['create_date']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'create_date': create_date
        }))


class System(WebsocketConsumer):
    def connect(self):
        User = UserProfile.objects.get(user=self.scope['user'])
        User.is_online = True
        User.save()
        async_to_sync(self.channel_layer.group_add)(
            'system',
            self.channel_name
        )

        # Join dialog group

        self.accept()

    def disconnect(self, close_code):
        # Leave dialog group
        User = UserProfile.objects.get(user=self.scope['user'])
        print('exit')
        User.is_online = False
        User.save()

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        type = text_data_json['type']
        author = self.scope["user"]
        if author == "":
            author = 'AnonymousUser'
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            'system',
            {
                'type': 'chat_message',
                'message_type': type,
                'message': message,
            }
        )

    # Receive message from dialog group
    def chat_message(self, event):
        message = event['message']
        message_type = event['message_type']
        print('send')

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'message_type': message_type
        }))