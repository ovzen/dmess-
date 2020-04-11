from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

from admin.models import Invite
from admin.serializers import InviteSerializer
from datetime import datetime

from main.models import Message, UserProfile

User = get_user_model()


class InviteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = InviteSerializer
    queryset = Invite.objects.all()


class StatisticsView(APIView):
    def get(self, request):
        sign_ups_count = User.objects.filter(date_joined__startswith=datetime.now().date()).count()
        messages_count = Message.objects.filter(create_date__startswith=datetime.now().date()).count()
        online_count = UserProfile.objects.filter(is_online=True).count()
        return Response({"sign_ups_count": sign_ups_count, "messages_count": messages_count, "online_count": online_count})
