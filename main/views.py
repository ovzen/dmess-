from django.contrib.auth.models import User
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import action
from rest_framework import mixins

from main import serializers
from main.models import Dialog, Contact, WikiPage, Message, UserProfile
from main.permissions import IsAdminUserOrReadOnly


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


class UserViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin,
                  CountModelMixin,
                  viewsets.GenericViewSet):
    """
    ViewSet для работы с профилями пользователей.
    Не имеет возможности создать нового пользователя.
    """
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAdminUserOrReadOnly]
    search_fields = ['id', 'username', 'first_name', 'last_name', 'email']

    @action(detail=True, methods=['post'])
    def add_contact(self, request, pk=None):
        user = self.get_object()
        contact, created = Contact.objects.get_or_create(user=request.user, contact=user)
        return Response(
            {'status': f'{user.username} {"successfully added" if created else "is already"} in your contact list'}
        )


class ContactViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ContactSerializer

    def get_queryset(self):
        user = self.request.user
        return Contact.objects.filter(user=user)


class DialogViewSet(viewsets.ModelViewSet, CountModelMixin):
    """
    ViewSet для работы с диалогами
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.DialogSerializer
    queryset = Dialog.objects.all()
    filterset_fields = ['users', 'name', 'id']

    def get_queryset(self):
        user = self.request.user
        return Dialog.objects.filter(users=user)

    @action(detail=True, methods=['post'])
    def read_messages(self, request, pk=None):
        """
        Отмечает все сообщения в данном диалоге прочитанными,
        исключая отправленные самим пользователем.
        В ответ возвращает количество прочитанных сообщений.
        :param request:
        :param pk:
        :return: Response
        """
        dialog = self.get_object()
        unread_messages = dialog.message_set.exclude(user=request.user).filter(is_read=False)
        count = unread_messages.count()
        unread_messages.update(is_read=True)
        for message in unread_messages:
            message.save()

        return Response(
            {'status': f'{count} messages were read'}
        )


class MessageViewSet(viewsets.ModelViewSet, CountModelMixin):
    """
    Send all messages from chat
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.MessageSerializer
    queryset = Message.objects.all()
    search_fields = ['text']
    filterset_fields = '__all__'


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.MyTokenObtainPairSerializer


class WikiPageViewSet(viewsets.ModelViewSet, CountModelMixin):
    """
    ViewSet для работы с вики-страницей
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.WikiPageSerializer
    queryset = WikiPage.objects.all()
    filterset_fields = ['title', 'dialog', 'message']


def landing_view(request):
    context = {
        'online_stat': UserProfile.objects.filter(is_online=True).count(),
        'registers_stat': User.objects.count(),
        'messages_stat': Message.objects.count()
    }
    return render(request, 'landing.html', context)
