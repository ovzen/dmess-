from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from admin.models import Invite
from main.models import Dialog, UserProfile, Message, Contact, WikiPage


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

        code = self.validated_data.get('invite_code')
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


class MessageSerializer(serializers.ModelSerializer):
    author_id = serializers.CharField(source='author.user.id')
    author = serializers.CharField(source='author.user.username')
    is_online = serializers.ImageField(source='author.is_online')
    avatar = serializers.ImageField(source='author.avatar')

    class Meta:
        model = Message
        fields = ('id', 'text', 'create_date', 'author_id', 'author', 'is_online', 'avatar')
        read_only_fields = ('create_date',)


class DialogSerializer(serializers.ModelSerializer):
    last_message = MessageSerializer(read_only=True)
    users_detail = UserSerializer(source='users', many=True, read_only=True)

    class Meta:
        model = Dialog
        fields = '__all__'


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        validators = [
            UniqueTogetherValidator(
                queryset=Contact.objects.all(),
                fields=['user', 'contact'],
                message='You have already added this contact.'
            )
        ]


class WikiPageSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=200)
    text = serializers.CharField(max_length=2000)
    image = serializers.ImageField(max_length=100, allow_empty_file=False, use_url=True)
    dialog = DialogSerializer(read_only=True)
    message = MessageSerializer(read_only=True)

    class Meta:
        model = WikiPage
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.username
        # ...
        return token
