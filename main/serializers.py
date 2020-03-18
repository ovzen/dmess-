from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from main.models import Dialog, UserProfile

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


class UserRegSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=150)
    date_joined = serializers.DateTimeField()

    class Meta:
        model = User
        fields = ("username", "date_joined")
        
    
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'

class DialogSerializer(serializers.Serializer):
    create_date = serializers.DateTimeField()
    last_change = serializers.DateTimeField()
    name = serializers.CharField(max_length=200)
    users = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), many=True)
    last_message = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Dialog.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.last_change = validated_data.get('last_change', instance.last_change)
        instance.name = validated_data.get('name', instance.name)
        instance.users = validated_data.get('users', instance.users)
        instance.last_message = validated_data.get('last_message', instance.last_message)
        instance.save()
        return instance


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.username
        # ...
        return token
