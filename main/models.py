# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserSetting(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField(upload_to='avatars',
                               null=True,
                               blank=True,
                               width_field="width_field",
                               height_field="height_field")
    width_field = models.IntegerField(default=0)
    height_field = models.IntegerField(default=0)

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        else:
            return '/static/user.png'


class Friend(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user')
    friend = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='friend')


class Status(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.status


class Dialog(models.Model):
    create_date = models.DateTimeField(default=timezone.now, blank=True)
    last_change = models.DateTimeField(default=timezone.now, blank=True)
    name = models.CharField(max_length=200)
    users = models.ManyToManyField(User)
    last_message = models.CharField(max_length=200, blank=True)
    admin_only = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Message(models.Model):
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    dialog = models.ForeignKey(to=Dialog, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)


class Invite(models.Model):
    code = models.CharField(max_length=16)
    is_active = models.BooleanField()
