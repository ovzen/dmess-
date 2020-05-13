from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main import models
from main.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    status = serializers.CharField()

    class Meta:
        model = models.UserProfile
        exclude = ('user','last_online')


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
    User = UserSerializer(read_only=True, source='user')
    Contact = UserSerializer(read_only=True, source='contact')

    class Meta:
        model = models.Contact
        fields = '__all__'
        extra_kwargs = {'user': {'write_only': True}, 'contact': {'write_only': True}}
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
