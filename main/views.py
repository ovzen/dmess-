import random
import string

from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from main.models import Dialog, Invite
from main.serializers import UserSerializer, DialogSerializer, InviteSerializer


# Create your views here.


class UserView(CreateAPIView):
    """
       Registration of new user
    """
    permission_classes = (AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


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


class InviteCheckView(APIView):
    def get(self, request):
        code = request.GET.get('code', None)
        if not code:
            return Response({"error": 'code not specified'})
        invite_query = Invite.objects.filter(code=code)
        if invite_query.count() > 0:
            invite = invite_query.first()
            if invite.is_active:
                return Response({"status": True})
        return Response({"status": False})


class InviteListView(APIView):
    def get(self, request):
        invites = Invite.objects.all()
        serializer = InviteSerializer(invites, many=True)
        return Response({"invites": serializer.data})


class InviteCreateView(APIView):
    def get(self, request):
        code = ''.join(random.choice(string.ascii_letters) for _ in range(16))
        invites = Invite.objects.filter(code=code)
        while len(invites) > 0:
            code = ''.join(random.choice(string.ascii_letters) for _ in range(16))
            invites = Invite.objects.filter(code=code)
        invite = Invite(code=code)
        invite.save()
        serializer = InviteSerializer(invite)
        return Response({"invite": serializer.data})


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
