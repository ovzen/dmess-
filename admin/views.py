"""
Admin Views
"""

from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from admin.models import Invite, GitlabMetrics
from admin.serializers import InviteSerializer

from main.models import UserProfile

User = get_user_model()


# pylint: disable=too-many-ancestors
class InviteViewSet(viewsets.ModelViewSet):
    """
    The ViewSet for Invites
    """
    permission_classes = [IsAdminUser]
    serializer_class = InviteSerializer
    queryset = Invite.objects.all()


class RegisterStatView(APIView):
    """
    The StatisticView for today registrations count
    """
    def get(self, request):
        date = request.GET.get('date', None)
        if date is not None:
            registers_count = User.objects.filter(
                date_joined__startswith=date
            ).count()
        else:
            registers_count = User.objects.filter(
                date_joined__startswith=datetime.now().date()
            ).count()
        return Response({"count": registers_count})


class UserStatView(APIView):
    """
    The StatisticView for online users count
    """
    def get(self, request):
        online_count = UserProfile.objects.filter(is_online=True).count()
        return Response({"count": online_count})


class GitlabMetricsView(APIView):
    """
    The View for Gitlab Metrics
    """
    def get(self, request):
        data = [GitlabMetrics.objects.filter(key=key).last()
                for key, _ in GitlabMetrics.KEY_CHOICES]
        response = {item.get_key_display(): item.value for item in data}
        return Response(response)
