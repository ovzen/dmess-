from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from main.models import Dialog, UserProfile, Contact, WikiPage
from main.models import Message
from main.permissions import IsOwnerOrReadOnly
from main.serializers import MessageSerializer, ContactSerializer
from main.serializers import UserSerializer, DialogSerializer, MyTokenObtainPairSerializer, UserProfileSerializer, \
    WikiPageSerializer
from rest_framework.filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action

User = get_user_model()


# noinspection PyUnresolvedReferences
class CountModelMixin:
    """
    Add count action to ModelViewSet
    """

    @action(detail=False)
    def count(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        content = {'count': queryset.count()}
        return Response(content)


class UserView(ListCreateAPIView):
    """
    Registration of new user
    + get method for getting list of all users
    """
    permission_classes = (AllowAny,)
    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = '__all__'


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

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(user=user)


class DialogViewSet(viewsets.ModelViewSet, CountModelMixin):
    """
    ViewSet для работы с диалогами
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = DialogSerializer
    queryset = Dialog.objects.all()
    filterset_fields = ('users', 'name', 'id')

    def get_queryset(self):
        user = self.request.user
        return Dialog.objects.filter(users=user)



class MessageViewSet(viewsets.ModelViewSet, CountModelMixin):
    """
    Send all messages from chat
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = MessageSerializer
    queryset = Message.objects.all()
    search_fields = ('text',)
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ('dialog', 'user')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class WikiPageViewSet(viewsets.ModelViewSet, CountModelMixin):
    """
    ViewSet для работы с вики-страницей
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WikiPageSerializer
    queryset = WikiPage.objects.all()
    filterset_fields = ('title', 'dialog', 'message')
