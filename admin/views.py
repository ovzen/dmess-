from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from admin.models import Invite
from admin.serializers import InviteSerializer


class InviteViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = InviteSerializer
    queryset = Invite.objects.all()
