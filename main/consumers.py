import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer

from rest_framework import status
from django.core.serializers.json import DjangoJSONEncoder

from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import RetrieveModelMixin
from djangochannelsrestframework.observer import model_observer
from djangochannelsrestframework.permissions import IsAuthenticated

from main.models import Message, UserProfile
from main import models, serializers


class ChatConsumer(WebsocketConsumer):
    """
    Огромный легаси консьюмер. Древнее зло этого проекта
    """
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

        message_obj = Message(
            user=author, text=message, dialog_id=self.chat_number, image_url=image
        )
        message_obj.save()

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.chat_id,
            {
                'type': 'chat_message',
                'message': message,
                'author': author.id,
                'create_date': json.dumps(
                    message_obj.create_date, cls=DjangoJSONEncoder
                ),
                'image_url': image,
                'name': message_obj.name,
                'extension': message_obj.extension,
                'id': message_obj.id
            }
        )

    # Receive message from dialog group
    def chat_message(self, event):
        """
        Отправляет сообщение на сторону клиента.
        :param event: словарь со всеми приколюхами
        :type: dict
        :return: None
        """
        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': event['message'],
            'author': event['author'],
            'create_date': event['create_date'],
            'image_url': event['image_url'],
            'extension': event['extension'],
            'name': event['name'],
            'id': event['id']
        }))


class System(WebsocketConsumer):
    def connect(self):
        profile = UserProfile.objects.get(user=self.scope['user'])
        profile.is_online = True
        profile.save()
        async_to_sync(self.channel_layer.group_add)(
            'system',
            self.channel_name
        )

        # Join dialog group

        self.accept()

    def disconnect(self, close_code):
        # Leave dialog group
        user_id = self.scope['user'].id
        user = models.User.objects.get(pk=user_id)
        print('exit')
        user.profile.is_online = False
        user.profile.last_online = datetime.now()
        user.profile.save()

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
    """
    Консьюмер для получения данных об изменении диалогов пользователя,
    в которых были написаны сообщения.
    """
    async def connect(self):
        user = self.scope['user']
        group_name = f'dialogs_user_{user.id}'
        print(group_name)
        self.groups.append(group_name)
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


class UserAPIConsumer(RetrieveModelMixin, GenericAsyncAPIConsumer):
    """
    Ассинхронный консьюмер для получения обновленной информации о пользователях
    приложения по предварительной подписке. Подписки бывают двух видов:
    1. На пользователей из списка контактов. Для этого следует отправить:
    ```json
    {
        action: 'subscribe_to_contacts',
        request_id: <CLIENT_USER_ID: int>
    }
    ```
    2. На конкретного пользователя (Например, из диалога).
     Для этого следует отправить:
    ```json
    {
        action: 'subscribe_to_contacts',
        request_id: <CLIENT_USER_ID: int>,
        pk: <SUBSCRIPTION_USER_ID>
    }
    ```
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [
        IsAuthenticated
    ]

    @action()
    async def subscribe_to_contacts(self, **kwargs):
        """Действие подписки на список контактов"""
        user = self.scope['user']
        print(f'user {user.id} has subscribed to it\'s contact list')
        await self.user_change_handler.subscribe(user_contacts=user)
        return None, status.HTTP_201_CREATED

    @action()
    async def subscribe_to_user(self, pk, **kwargs):
        """Действие подписки на пользователя по его id"""
        user = await database_sync_to_async(self.get_object)(pk=pk)
        print(f'You have successfully subscribed to user'
              f' {user.username} with id: {user.id}')
        await self.user_change_handler.subscribe(user=user)
        return None, status.HTTP_201_CREATED

    async def handle_observed_action(self, **kwargs):
        """Формирует и отправляет ответ на сторону клиента"""
        print(kwargs)
        data, response_status = await self.retrieve(**kwargs)
        message_action = kwargs.pop('action')

        await self.reply(
            action=message_action,
            data=data,
        )

    @model_observer(models.User)
    async def user_change_handler(self, message, observer=None, **kwargs):
        """Наблюдатель за изменениями модели пользователя"""
        await self.handle_observed_action(**message)

    @user_change_handler.groups_for_signal
    def user_change_handler(self, instance: models.User, **kwargs):
        """
        Группы, в которые отправляется сигнал при событии
        изменения модели пользователя
        """
        yield f'-pk__{instance.pk}'
        for user in instance.users.all():
            yield f'-contacts__user__{user.pk}'

    @user_change_handler.groups_for_consumer
    def user_change_handler(self, user_contacts=None, user=None, **kwargs):
        """
        Группы, на которые создается подписка
        """
        if user_contacts is not None:
            yield f'-contacts__user__{user_contacts.pk}'
        if user is not None:
            yield f'-pk__{user.pk}'

    @model_observer(models.UserProfile)
    async def user_profile_change_handler(self, message, observer=None, **kwargs):
        """Наблюдатель за изменениями модели профиля пользователя"""
        await self.handle_observed_action(**message)

    @user_profile_change_handler.groups_for_signal
    def user_profile_change_handler(self, instance: models.UserProfile, **kwargs):
        """
        Группы, в которые отправляется сигнал при событии
        изменения модели профиля пользователя
        """
        yield f'-pk__{instance.user.pk}'
        for user in instance.user.users.all():
            yield f'-contacts__user__{user.pk}'

    @user_profile_change_handler.groups_for_consumer
    def user_change_handler(self, user_contacts=None, user=None, **kwargs):
        """
        Группы, на которые создается подписка
        """
        if user_contacts is not None:
            yield f'-contacts__user__{user_contacts.pk}'
        if user is not None:
            yield f'-pk__{user.pk}'
