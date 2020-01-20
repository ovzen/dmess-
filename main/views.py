import datetime
from abc import ABC

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from main import serializers
from dmess.settings import BASE_ADDRESS

# Класс регистрации пользователей


class CreateUserView(CreateAPIView):
    # model используется только для информации
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny # Or anon users can't register
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
        ],
        'index_link_name': 'index',
        'title': 'untitled',
    }
    return context


def index_chat(request):
    context = get_base_context()
    context['title'] = 'Главная страница - Dmess'
    context['main_header'] = 'Digital Messages'
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
