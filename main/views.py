from django.contrib.auth.models import User
from django.core.files.storage import default_storage
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework import mixins

from main import serializers
from main.models import Dialog, Contact, WikiPage, Message, UserProfile
from main.permissions import IsAdminUserOrReadOnly


# noinspection PyUnresolvedReferences
class CountModelMixin:
    """
    Добавляет действие count (количество) к ModelViewSet
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
    search_fields = ['username', 'first_name', 'last_name', 'email']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_contact(self, request, pk=None):
        user = self.get_object()
        contact, created = Contact.objects.get_or_create(user=request.user, contact=user)
        return Response(status=201 if created else 400)


class ContactViewSet(mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.ContactSerializer

    def get_queryset(self):
        """
        Фильтрует queryset контактов по тем, в которых состоит пользователь
        """
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
        """
        Фильтрует queryset диалогов по тем, в которых состоит пользователь
        """
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
    ViewSet для работы с сообщениями
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.MessageSerializer
    queryset = Message.objects.all()
    search_fields = ['text']
    filterset_fields = '__all__'
    ordering_fields = ['id', 'create_date']

    def get_queryset(self):
        """
        Фильтрует queryset сообщений по текущему пользователю
        """
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        else:
            return Message.objects.filter(dialog__users=user)

    @action(detail=False, methods=['post'])
    def image_upload(self, request):
        """
        Принимает на вход картинку, загружает ее на сервер и отдает
        обратно ссылку на файл.
        :param request:
        :return: Response
        """
        image = request.FILES['image']
        image_name = default_storage.save(image.name, image)
        image_url = default_storage.url(image_name)
        return Response({"image_url": image_url})


class WikiPageViewSet(viewsets.ModelViewSet, CountModelMixin):
    """
    ViewSet для работы с вики-страницей
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.WikiPageSerializer
    queryset = WikiPage.objects.all()
    filterset_fields = ['title', 'dialog', 'message']

    def get_queryset(self):
        """
        Фильтрует queryset вики-страниц по тем, в диалоге которых состоит юзер
        """
        user = self.request.user
        if user.is_staff:
            return super().get_queryset()
        else:
            return WikiPage.objects.filter(dialog__users=user)


def landing_view(request):
    context = {
        'online_stat': UserProfile.objects.filter(is_online=True).count(),
        'registers_stat': User.objects.count(),
        'messages_stat': Message.objects.count()
    }
    return render(request, 'landing.html', context)
