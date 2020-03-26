from rest_framework.decorators import action
from rest_framework.generics import RetrieveUpdateAPIView, get_object_or_404, ListCreateAPIView
from rest_framework.generics import ListAPIView
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from main.models import Dialog, UserProfile, Contact
from main.models import Message
from main.permissions import IsOwnerOrReadOnly
from main.serializers import MessageSerializer, ContactSerializer
from main.serializers import UserSerializer, DialogSerializer, MyTokenObtainPairSerializer, UserProfileSerializer


User = get_user_model()


class UserView(ListCreateAPIView):
    """
    Registration of new user
    + get method for getting list of all users
    """
    permission_classes = (AllowAny,)
    model = User
    queryset = User.objects
    serializer_class = UserSerializer


class MessageView(ListAPIView):
    """
    Send all messages from chat
    """
    permission_classes = (AllowAny,)
    model = Message
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.all().filter(dialog_id=self.request.query_params.get('chat_id'))


class UserProfileView(RetrieveUpdateAPIView):
    """
    View для просмотра и обновления данных о пользователе
    Обновление данных доступно только для владельцев профиля
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = (IsOwnerOrReadOnly,)


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = ContactSerializer
    queryset = Contact.objects.all()


class DialogViewSet(viewsets.ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = DialogSerializer
    queryset = Dialog.objects.all()

    def get_queryset(self):
        id = self.request.query_params.get('id')
        for_user = self.request.query_params.get('for_user')
        name = self.request.query_params.get('name')
        if id:
            dialogs = Dialog.objects.filter(id=id)
        elif for_user:
            dialogs = Dialog.objects.filter(users=self.request.user)
        elif name:
            dialogs = Dialog.objects.filter(name=name)
        else:
            dialogs = Dialog.objects.all()
        return dialogs


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class ActivityFeedView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        registrations = User.objects.all()
        user_reg_serializer = UserSerializer(registrations, many=True)
        dialogs = Dialog.objects.all()
        dialog_serializer = DialogSerializer(dialogs, many=True)
        return Response({
            'registrations': user_reg_serializer.data,
            'dialogs': dialog_serializer.data,
        })
