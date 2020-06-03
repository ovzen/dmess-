"""
Сериализаторы главных моделей базы данных.
Преимущественно относятся к клиентской и общей части приложения.
"""

from django.contrib.auth.models import User
from rest_framework import serializers

from main import models


class UserProfileSerializer(serializers.ModelSerializer):
    """
    The UserProfile Serializer
    """
    status = serializers.CharField(read_only=True)

    class Meta:
        model = models.UserProfile
        exclude = ('user', 'is_online', 'last_online')


class UserSerializer(serializers.ModelSerializer):
    """
    The User Serializer
    """
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile', 'is_staff')
        read_only_fields = ('is_staff',)

    def update(self, instance, validated_data):
        """
        Обновляет поля в моделе пользователя и профиль,
        привязанный к ней
        :param User instance: экземляр пользователя
        :param dict validated_data: валидированные данные
        :return: сохраненный экземляр пользователя
        :rtype: User
        """
        profile_data = validated_data.pop('profile')
        for key, value in validated_data.items():
            setattr(instance, key, value)
        for key, value in profile_data.items():
            setattr(instance.profile, key, value)
        instance.save()
        instance.profile.save()
        return instance


class MessageSerializer(serializers.ModelSerializer):
    """
    The Message Serializer
    """
    name = serializers.CharField(read_only=True)
    extension = serializers.CharField(read_only=True)

    class Meta:
        model = models.Message
        fields = '__all__'


class DialogSerializer(serializers.ModelSerializer):
    """
    The Dialog Serializer
    """
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
    """
    The Contact Serializer
    """
    class Meta:
        model = models.Contact
        fields = ['id', 'contact']


class WikiPageSerializer(serializers.ModelSerializer):
    """
    The WikiPageSerializer
    """
    class Meta:
        model = models.WikiPage
        fields = '__all__'
        read_only_fields = ['image']
