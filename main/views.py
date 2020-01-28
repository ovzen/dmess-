import datetime
from abc import ABC

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from main import serializers
from dmess.settings import BASE_ADDRESS

from main.models import Status
from main.serializers import StatusSerializer

from .models import Dialog
from .serializers import DialogSerializer

class CreateUserView(CreateAPIView):
    # Класс регистрации пользователей
    # model используется только для информации
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny  # Or anon users can't register
    ]
    serializer_class = serializers.UserSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.username
        # ...
        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



def get_base_context():
    context = {
        'menu': [
            {'link_name': 'index', 'text': 'Главная'},
            {'link_name': 'dialogs', 'text': 'Диалоги'},
            {'link_name': 'about', 'text': 'Информация'},
            {'link_name': 'admin:index', 'text': 'Админ-панель'},
            {'link_name': 'mypage', 'text': 'Личный кабинет'},
        ],
        'index_link_name': 'index',
        'title': 'untitled',
    }
    return context



def index_chat(request, chat_number):
    context = get_base_context()
    context['title'] = 'Главная страница - Dmess'
    context['main_header'] = 'Digital Messages'
    context['chat_number'] = chat_number
    return render(request, 'chat/index.html', context)


def index_page(request):
    context = get_base_context()
    # context['title'] = 'Основной чат'
    context['main_header'] = 'Digital Messages'
    return render(request, 'index.html', context)


def register_page(request):
    context = get_base_context()
    # context['title'] = 'Основной чат'
    context['main_header'] = 'Digital Messages'
    return render(request, 'registration/registration.html', context)


def sitemap_page(request):
    context = get_base_context()
    context['base_address'] = BASE_ADDRESS
    return render(request, 'sitemap.xml', context)


@login_required
def dialog_page(request):
    context = get_base_context()
    context['title'] = 'Диалоги - Dmess'
    context['main_header'] = 'Диалоги'
    # Код диалога
    if False:  # Заглушка

        context['not_auth'] = False
    else:
        context['not_auth'] = True
        context['error'] = 'Вы не авторизованы!'
    return render(request, 'dialogs.html', context)


def about_page(request):
    context = get_base_context()
    context['title'] = 'Информация - Dmess'
    context['main_header'] = 'Информация'
    return render(request, 'about.html', context)


def my_page(request):
    context = get_base_context()
    context['title'] = 'Личный кабинет - Dmess'
    context['main_header'] = 'Личный кабинет'

    user = request.user
    context['status'] = Status.objects.filter(user=user)
    return render(request, 'mypage.html', context)


class StatusView(APIView):
    def get(self, request):
        statuses = Status.objects.all()
        # Сериализация статуса  (т.е. конвертация из объектов в формат JSON)
        serializer = StatusSerializer(statuses, many=True)
        return Response({"statuses": serializer.data})

    def post(self, request):
        """Метод для создания статуса"""
        status = request.data.get("status")

        # Create an article from the above data
        serializer = StatusSerializer(data=status)
        if serializer.is_valid(raise_exception=True):
            status_saved = serializer.save()
        return Response({"success": "Статус '{}' успешно создан".format(status_saved.status)})

    def put(self, request, pk):
        """
        Метод для обработки запроса на обновление статьи.
        Метод должен принять параметр  pk из URL, найти требуемый экземпляр из базы и
        запустить сериалайзер на обновление
        """
        saved_status = get_object_or_404(Status.objects.all(), pk=pk)
        data = request.data.get('status')
        # partial=True - необходимо для возможности обноления только некоторых полей
        serializer = StatusSerializer(instance=saved_status, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            status_saved = serializer.save()
        return Response({
            "success": "Статус '{}' успешно обновлен".format(status_saved.status)
        })

    def delete(self, request, pk):
        # Get object with this pk
        status = get_object_or_404(Status.objects.all(), pk=pk)
        status.delete()
        return Response({
            "message": "Статус с id `{}` был удален.".format(pk)
        }, status=204)


class DialogView(APIView):
    def get(self, request):
        dialogs = Dialog.objects.all()
        serializer = DialogSerializer(dialogs, many=True)
        return Response({"dialogs": serializer.data})

    def post(self, request):
        dialog = request.data.get('dialog')
        # Create an dialog from the above data
        serializer = DialogSerializer(data=dialog)
        if serializer.is_valid(raise_exception=True):
            article_saved = serializer.save()
        return Response({"success": "Dialog '{}' created successfully".format(article_saved.title)})

