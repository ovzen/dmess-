from django.contrib.auth import get_user_model

# Create your views here.
from rest_framework.generics import CreateAPIView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from main.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    """
       Registration of new user
    """
    permission_classes = (AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


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
    """
        This text is the description for this API
    """
    serializer_class = MyTokenObtainPairSerializer
