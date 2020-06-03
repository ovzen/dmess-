# coding=utf-8
"""
Главные модели базы данных.
Преимущественно относятся к клиентской и общей части приложения.
"""

import uuid

from coverage.annotate import os
from django.contrib.auth.models import User
from django.db import models
from django.utils.timesince import timesince


class UserProfile(models.Model):
    """
    Реализует хранение дополнительных данных о пользователе, таких как
    аватар, статус и т.п.
    """

    user = models.OneToOneField(
        to=User, on_delete=models.CASCADE,
        related_name='profile',
        primary_key=True
    )
    avatar = models.ImageField(
        upload_to='avatars',
        null=True,
        blank=True,
        width_field="width_field",
        height_field="height_field"
    )
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)
    bio = models.CharField(max_length=70, default="Hey there! I'm using dmess")
    is_online = models.BooleanField(default=False)
    last_online = models.DateTimeField(auto_now=True)

    def status(self):
        """
        Формирует строку статуса пользователя.
        :return: строка статуса
        """
        return (f'last seen {timesince(self.last_online)} ago'
                if not self.is_online else 'online')


class Contact(models.Model):
    """
    Реализует хранение контактов.
    Каждая сущность уникальна.
    """
    user = models.ForeignKey(
        to=User, on_delete=models.CASCADE,
        related_name='users'
    )
    contact = models.ForeignKey(
        to=User, on_delete=models.CASCADE,
        related_name='contacts'
    )

    class Meta:
        unique_together = ['user', 'contact']


class Dialog(models.Model):
    """
    Реализует сущность диалога
    """
    create_date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User)
    name = models.CharField(max_length=200, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    def last_message(self):
        """
        :return: Последнее сообщение в диалоге
        :rtype: Message
        """
        return self.message_set.order_by('-create_date').first()

    def unread_messages(self):
        """
        Возвращает количество непрочитанных сообщений в диалоге
        для каждого пользователя, в виде словаря.
        :return: Словарь вида user_id: message_count
        :rtype: dict
        """
        messages = self.message_set.filter(is_read=False)
        return {user.id: messages.exclude(user=user).count()
                for user in self.users.get_queryset()}


class Message(models.Model):
    """
    Реализует хранение сообщений в диалоге.
    """
    text = models.TextField(max_length=2000)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    dialog = models.ForeignKey(to=Dialog, on_delete=models.CASCADE)
    create_date = models.DateTimeField(auto_now_add=True)
    image_url = models.CharField(max_length=200, default=False, null=True)
    is_read = models.BooleanField(default=False)

    @property
    def extension(self):
        """
        :return: Расширение приложенного файла
        """
        return os.path.splitext(self.image_url)[1]

    @property
    def name(self):
        """
        :return: Имя приложенного файла
        """
        return os.path.basename(self.image_url)


class WikiPage(models.Model):
    """
    Реализует хранение вики-страниц.
    В текущем релизе проекта не используется.
    """
    dialog = models.ForeignKey(to=Dialog, on_delete=models.CASCADE)
    message = models.OneToOneField(to=Message, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='wiki',
        height_field=None,
        width_field=None,
        max_length=100,
        blank=True,
    )
    text_markdown = models.TextField(max_length=2000)
    text_html = models.TextField(max_length=2000, blank=True)
