from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main.models import Dialog, UserProfile, Message

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        profile = UserProfile(user=user)
        profile.save()

        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = ("id", "username", "password", "first_name", "last_name", "email")


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'


class DialogSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), many=True)

    class Meta:
        model = Dialog
        fields = ('id', 'name', 'users')


class MessageSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(source='author.user.id')
    author = serializers.CharField(source='author.user.username')
    is_online = serializers.ImageField(source='author.is_online')
    avatar = serializers.ImageField(source='author.avatar')
    class Meta:
        model = Message
        fields = ('id', 'text', 'create_date', 'author_id', 'author', 'is_online', 'avatar')
        read_only_fields = ('create_date', )


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.username
        # ...
        return token
