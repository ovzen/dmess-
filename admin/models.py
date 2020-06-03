"""
Admin Models
"""

import uuid
from django.utils import timezone

from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class InviteAlreadyUsed(Exception):
    """
    The InviteAlreadyUsed Exception
    """


class Invite(models.Model):
    """
    The Invite Model
    """
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
        self.used_at = timezone.now()
        self.for_user = user


class GitlabMetrics(models.Model):
    """
    The Gitlab Metrics Model
    """
    OPENED_ISSUES = 1
    OPENED_MERGE_REQUESTS = 2
    CURRENT_BRANCHES = 3
    COMMITS = 4
    KEY_CHOICES = [
        (OPENED_ISSUES, 'opened_issues'),
        (OPENED_MERGE_REQUESTS, 'opened_merge_requests'),
        (CURRENT_BRANCHES, 'current_branches'),
        (COMMITS, 'commits'),
    ]
    fetch_date = models.DateTimeField(auto_now_add=True)
    key = models.IntegerField(choices=KEY_CHOICES, null=True, blank=True)
    value = models.CharField(max_length=25, blank=True)
