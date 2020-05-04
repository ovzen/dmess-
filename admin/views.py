from rest_framework import viewsets
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from admin.models import Invite, GitlabMetrics
from admin.serializers import InviteSerializer
from datetime import datetime

from main.models import UserProfile

User = get_user_model()


class InviteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = InviteSerializer
    queryset = Invite.objects.all()


class RegisterStatView(APIView):
    def get(self, request):
        date = request.GET.get('date', None)
        if date is not None:
            registers_count = User.objects.filter(date_joined__startswith=date).count()
        else:
            registers_count = User.objects.filter(date_joined__startswith=datetime.now().date()).count()
        return Response({"count": registers_count})


class UserStatView(APIView):
    def get(self, request):
        online_count = UserProfile.objects.filter(is_online=True).count()
        return Response({"count": online_count})


class GitlabMetricsView(APIView):
    def get(self, request):
        item = GitlabMetrics.objects.all().order_by('-id')[0]
        return Response({"date": item.fetch_date, "issues": item.opened_issues,
                         "merge_requests": item.opened_merge_requests,
                         "branches": item.current_branches,
                         "commits": item.commits})

