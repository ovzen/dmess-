from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main import models
from main.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserProfile
        exclude = ('user',)


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'profile')

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
    user_detail = UserSerializer(source='user', read_only=True)

    class Meta:
        model = models.Message
        fields = '__all__'


class DialogSerializer(serializers.ModelSerializer):
    last_message = MessageSerializer(read_only=True)
    users_detail = UserSerializer(source='users', many=True, read_only=True)
    unread_messages = serializers.DictField(read_only=True)

    class Meta:
        model = models.Dialog
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    Username = serializers.CharField(source='user.username', read_only=True)
    Userstatus = serializers.BooleanField(source='user.profile.is_online', read_only=True)
    Contactname = serializers.CharField(source='contact.username', read_only=True)
    Contactstatus = serializers.BooleanField(source='contact.profile.is_online', read_only=True)

    class Meta:
        model = models.Contact
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=models.Contact.objects.all(),
                fields=['user', 'contact'],
                message='You have already added this contact.'
            )
        ]


class WikiPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WikiPage
        fields = '__all__'
        read_only_fields = ['image']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.username
        # ...
        return token
