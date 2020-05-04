import datetime
import uuid

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Invite(models.Model):
    code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now=True)
    used_at = models.DateTimeField(default=None, blank=True, null=True)
    for_user = models.ForeignKey(to=User, on_delete=models.SET_NULL, blank=True, null=True)

    def use(self, user):
        if self.is_active:
            self.is_active = False
            self.used_at = datetime.datetime.now()
            self.for_user = user


class GitlabMetrics(models.Model):
    fetch_date = models.DateTimeField(auto_now_add=True)
    opened_issues = models.IntegerField()
    opened_merge_requests = models.IntegerField()
    current_branches = models.IntegerField()
    commits = models.IntegerField()