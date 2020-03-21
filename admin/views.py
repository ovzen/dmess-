from rest_framework import viewsets

from admin.models import Invite
from admin.serializers import InviteSerializer


class InviteViewSet(viewsets.ModelViewSet):
    serializer_class = InviteSerializer
    queryset = Invite.objects.all()
