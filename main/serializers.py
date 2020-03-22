from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from admin.models import Invite
from main.models import Dialog, UserProfile, Message, Friend

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    invite_code = serializers.UUIDField(required=False, allow_null=True, write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()

        code = self.validated_data['invite_code']
        if code:
            invite_object = Invite.objects.filter(code=code)
            if invite_object.exists():
                invite = invite_object.first()
                user.is_staff = invite.is_active
                user.save()
                invite.use(user)
                invite.save()

        profile = UserProfile(user=user)
        profile.save()
        return user

    class Meta:
        model = UserModel
        # Tuple of serialized model fields (see link [2])
        fields = (
            "id", "username", "password",
            "first_name", "last_name", "email",
            "invite_code", "is_staff"
        )


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
    id = serializers.IntegerField(read_only=True)
    create_date = serializers.DateTimeField(read_only=True)
    last_change = serializers.DateTimeField(read_only=True)
    name = serializers.CharField(max_length=200)
    users = serializers.PrimaryKeyRelatedField(queryset=UserModel.objects.all(), many=True)
    last_message = serializers.CharField(max_length=200, read_only=True)

    def create(self, validated_data):
        Dia = Dialog.objects.create(name=validated_data['name'])
        Dia.users.set(validated_data['users'])
        return Dia

    def update(self, instance, validated_data):
        instance.create_date = validated_data.get('create_date', instance.create_date)
        instance.last_change = validated_data.get('last_change', instance.last_change)
        instance.name = validated_data.get('name', instance.name)
        instance.users = validated_data.get('users', instance.users)
        instance.last_message = validated_data.get('last_message', instance.last_message)
        instance.save()
        return instance

    class Meta:
        model = Dialog
        fields = ('id', 'name', 'users', 'create_date', 'last_change', 'last_message')


class MessageSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(source='author.user.id')
    author = serializers.CharField(source='author.user.username')
    is_online = serializers.ImageField(source='author.is_online')
    avatar = serializers.ImageField(source='author.avatar')

    class Meta:
        model = Message
        fields = ('id', 'text', 'create_date', 'author_id', 'author', 'is_online', 'avatar')
        read_only_fields = ('create_date',)


class FriendSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    friend = UserSerializer(read_only=True)
    friend_id = serializers.IntegerField(write_only=True)

    def create(self, validated_data):
        friend = Friend.objects.create(
            user=self._context['request']._user,
            friend=UserModel.objects.get(id=validated_data['friend_id'])
        )
        friend.save()

        return friend

    class Meta:
        model = Friend
        fields = ('user', 'friend', 'friend_id')


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.username
        # ...
        return token
