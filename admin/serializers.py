from rest_framework import serializers

from admin.models import Invite


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = '__all__'
