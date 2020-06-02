from django.contrib.auth.models import User
from rest_framework import serializers

from main import models


class UserProfileSerializer(serializers.ModelSerializer):
    status = serializers.CharField(read_only=True)

    class Meta:
        model = models.UserProfile
        exclude = ('user', 'is_online', 'last_online')


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile', 'is_staff')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        for key, value in profile_data.items():
            setattr(instance.profile, key, value)
        instance.profile.save()
        instance.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    name = serializers.CharField(read_only=True)
    extension = serializers.CharField(read_only=True)

    class Meta:
        model = models.Message
        fields = '__all__'


class DialogSerializer(serializers.ModelSerializer):
    last_message = MessageSerializer(read_only=True)
    unread_messages = serializers.DictField(read_only=True)

    class Meta:
        model = models.Dialog
        fields = '__all__'

    # def validate_users(self, value):
    #     supposed_dialog = models.Dialog.objects.filter(users__in=value)
    #     if supposed_dialog.exists():
    #         raise serializers.ValidationError(
    #             f'Dialog with users {value} in already exists.'
    #             f' check: /api/dialog/{supposed_dialog.first().id}/'
    #         )


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Contact
        fields = ['id', 'contact']


class WikiPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WikiPage
        fields = '__all__'
        read_only_fields = ['image']
