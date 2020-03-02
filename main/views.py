from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.shortcuts import render

# Create your views here.

from rest_framework import serializers, permissions
from rest_framework.generics import CreateAPIView, ListCreateAPIView, ListAPIView, GenericAPIView, DestroyAPIView
from rest_framework.mixins import ListModelMixin

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from main.models import Dialog, Friend
from main.serializers import UserSerializer, DialogSerializer, FriendSerializer


class UserView(CreateAPIView, ListAPIView):
    permission_classes = (AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer
    queryset = model.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FriendView(CreateAPIView, ListAPIView):
    permission_classes = (AllowAny,)
    model = Friend
    serializer_class = FriendSerializer
    queryset = model.objects.all()

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class DialogView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request):
        id = request.query_params.get('id')
        if id:
            dialogs = Dialog.objects.filter(id=id)
        else:
            dialogs = Dialog.objects.all()
        serializer = DialogSerializer(dialogs, many=True)
        return Response({"dialogs": serializer.data})

    def post(self, request):
        # TODO make a chat name from the recipient's name
        user = get_user_model()
        dialog = {
            'name': 'Untitled3',
            'users': [request.user.id]
        }
        serializer = DialogSerializer(data=dialog)
        if serializer.is_valid(raise_exception=True):
            dialog_saved = serializer.save()
        return Response({
            "success": "dialog '{}' created successfully".format(dialog_saved.name),
            "id_dialog": dialog_saved.id
        })


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims
        token['name'] = user.username
        # ...
        return token


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


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
