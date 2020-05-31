from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
import json

from django.core.serializers.json import DjangoJSONEncoder

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
        image = text_data_json['image_url']
        author = self.scope["user"]
        if author == "":
            author = 'AnonymousUser'

        message_obj = Message(user=author, text=message, dialog_id=self.chat_number, image_url=image)
        message_obj.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_id,
            {
                'type': 'chat_message',
                'message': message,
                'author': author.id,
                'create_date': json.dumps(message_obj.create_date, cls=DjangoJSONEncoder),
                'image_url': image
            }
        )

    # Receive message from dialog group
    def chat_message(self, event):
        message = event['message']
        author = event['author']
        create_date = event['create_date']
        image = event['image_url']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': message,
            'author': author,
            'create_date': create_date,
            'image_url': image
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
        User.last_online = datetime.now()
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


class DialogNotificationConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # We're always going to accept the connection, though we may
        # close it later based on other factors.
        user = self.scope['user']
        group_name = f'dialogs_user_{user.id}'
        print(group_name)
        # The AsyncJsonWebsocketConsumer parent class has a
        # self.groups list already. It uses it in cleanup.
        self.groups.append(group_name)
        # This actually subscribes the requesting socket to the
        # named group:
        await self.channel_layer.group_add(
            group_name,
            self.channel_name,
        )
        await self.accept()

    async def notify(self, event):
        """
        This handles calls elsewhere in this codebase that look
        like:

            channel_layer.group_send(group_name, {
                'type': 'notify',  # This routes it to this handler.
                'content': json_message,
            })

        Don't try to directly use send_json or anything; this
        decoupling will help you as things grow.
        """
        await self.send_json(event["content"])
