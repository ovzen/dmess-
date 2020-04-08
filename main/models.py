# coding=utf-8
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from main.tasks import markdown_convert

class UserProfile(models.Model):
    """
    Реализует хранение дополнительных данных о пользователе, таких как
    аватар, статус и т.п.
    """

    user = models.OneToOneField(to=User, on_delete=models.CASCADE, primary_key=True)
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


class Contact(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='user')
    contact = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='contact')


class Dialog(models.Model):
    create_date = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(User)
    admin_only = models.BooleanField(default=False)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    # def get_title_from_names(self):
    #     return ', '.join(
    #         map(lambda user: user.first_name, self.users.all())
    #     )

    def last_message(self):
        return self.message_set.order_by('-create_date').first()


class Message(models.Model):
    text = models.TextField(max_length=2000)
    author = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE)
    dialog = models.ForeignKey(to=Dialog, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)


class WikiPage(models.Model):
    dialog = models.ForeignKey(to=Dialog, on_delete=models.CASCADE)
    message = models.OneToOneField(to=Message, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    image = models.ImageField(
        upload_to='wiki',
        height_field=None,
        width_field=None,
        max_length=100
    )
    text_markdown = models.TextField(max_length=2000)
    text_html = models.TextField(max_length=2000, blank=True, default=None)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not self.text_html:
            markdown_convert.delay(self)
        super().save(force_insert, force_update, using, update_fields)

