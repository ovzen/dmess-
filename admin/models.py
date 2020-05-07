import datetime
import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class InviteAlreadyUsed(Exception):
    pass


class Invite(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    used_at = models.DateTimeField(default=None, blank=True, null=True)
    for_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True)

    def use(self, user):
        if not self.is_active:
            raise InviteAlreadyUsed(
                f'Invite with code {self.code} is already used'
            )
        self.is_active = False
        user.is_staff = True
        user.save()
        self.used_at = datetime.datetime.now()
        self.for_user = user
