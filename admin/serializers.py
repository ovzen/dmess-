from rest_framework import serializers

from admin.models import Invite


class InviteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = '__all__'
        read_only_fields = ['used_at', 'for_user']
