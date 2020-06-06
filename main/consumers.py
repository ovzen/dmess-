import json
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer, AsyncJsonWebsocketConsumer
from django.core.serializers.json import DjangoJSONEncoder
from djangochannelsrestframework import permissions
from djangochannelsrestframework.decorators import action
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import (
    RetrieveModelMixin,
    PatchModelMixin,
    UpdateModelMixin,
    CreateModelMixin,
    DeleteModelMixin,
)
from djangochannelsrestframework.observer import model_observer
from rest_framework import status

from main import models, serializers
from main.models import UserProfile


class System(WebsocketConsumer):
    def connect(self):
        user_id = self.scope['user'].id
        user = models.User.objects.get(pk=user_id)
        user.profile.is_online = True
        user.profile.save()
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
        action: 'subscribe_to_user',
        request_id: <CLIENT_USER_ID: int>,
        pk: <SUBSCRIPTION_USER_ID>
    }
    ```
    """
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [
        permissions.IsAuthenticated
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

    @action()
    async def unsubscribe_to_user(self, pk, **kwargs):
        """Действие подписки на пользователя по его id"""
        user = await database_sync_to_async(self.get_object)(pk=pk)

        print(f'ДИЗЛАЙК ОТПИСКА user'
              f' {user.username} with id: {user.id}')
        await self.user_change_handler.unsubscribe(user=user)
        return None, status.HTTP_204_NO_CONTENT

    async def handle_observed_action(self, **kwargs):
        """Формирует и отправляет ответ на сторону клиента"""
        print(kwargs)
        message_action = kwargs.get('action')
        if message_action == 'delete':
            data, response_status = {'id': kwargs['pk']}, status.HTTP_204_NO_CONTENT
        else:
            data, response_status = await self.retrieve(**kwargs)

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
        # for user in instance.users.all():
        #         #     print(f'СИГНАЛ ЮЗЕР -contacts__user__{user.pk}')
        #         #     yield f'-contacts__user__{user.pk}'

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
        # for user in instance.user.users.all():
        #     print(f'СИГНАЛ ПРОФИЛЬ -contacts__user__{user.pk}')
        #     yield f'-contacts__user__{user.pk}'

    @user_profile_change_handler.groups_for_consumer
    def user_change_handler(self, user_contacts=None, user=None, **kwargs):
        """
        Группы, на которые создается подписка
        """
        if user_contacts is not None:
            yield f'-contacts__user__{user_contacts.pk}'
        if user is not None:
            yield f'-pk__{user.pk}'


class MessageAPIConsumer(PatchModelMixin,
                         RetrieveModelMixin,
                         UpdateModelMixin,
                         CreateModelMixin,
                         DeleteModelMixin,
                         GenericAsyncAPIConsumer):
    queryset = models.Message.objects.all()
    serializer_class = serializers.MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def filter_queryset(self, queryset, **kwargs):
        user = self.scope.get('user')
        if user.is_staff:
            return queryset
        else:
            return queryset.filter(dialog__users=user)

    @database_sync_to_async
    def get_dialog(self, **kwargs):
        try:
            return models.Dialog.objects.get(**kwargs)
        except models.Dialog.DoesNotExist:
            return None

    @action()
    async def subscribe_to_messages_in_dialog(self, dialog_id, **kwargs):
        user = self.scope.get('user')
        dialog = await self.get_dialog(pk=dialog_id, users=user)
        print(dialog.id)
        print('ПОДПИСКААА')
        if dialog:
            await self.message_in_dialog_change_handler.subscribe(dialog=dialog)
            return None, status.HTTP_201_CREATED
        else:
            return None, status.HTTP_404_NOT_FOUND

    @action()
    async def unsubscribe_to_messages_in_dialog(self, dialog_id, **kwargs):
        user = self.scope.get('user')
        dialog = await self.get_dialog(pk=dialog_id, users=user)
        print(dialog.id)
        print('вы отписалист от диалога')
        if dialog:
            await self.message_in_dialog_change_handler.unsubscribe(dialog=dialog)
            return None, status.HTTP_204_NO_CONTENT
        else:
            return None, status.HTTP_404_NOT_FOUND

    @model_observer(models.Message)
    async def message_in_dialog_change_handler(self, message: dict, observer=None, **kwargs):
        print('hahaha', message)

        message_action = message.get('action')

        if message_action == 'delete':
            data, response_status = {'id': message['pk']}, status.HTTP_204_NO_CONTENT
        else:
            data, response_status = await self.retrieve(**message)

        await self.reply(
            action=message_action,
            data=data,
            status=response_status
        )

    @message_in_dialog_change_handler.groups_for_signal
    def message_in_dialog_change_handler(self, instance: models.Message, **kwargs):
        print('SIGNAL', f'-d__{instance.dialog_id}')
        yield f'-d__{instance.dialog_id}'

    @message_in_dialog_change_handler.groups_for_consumer
    def message_in_dialog_change_handler(self, dialog: models.Dialog, **kwargs):
        print('consumer', f'-d__{dialog.id}')
        yield f'-d__{dialog.id}'
