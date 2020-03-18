from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListCreateAPIView, ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from main.models import Dialog, UserProfile, Message
from main.permissions import IsOwnerOrReadOnly
from main.serializers import UserSerializer, DialogSerializer, MyTokenObtainPairSerializer, UserProfileSerializer, \
    MessageSerializer


class UserView(CreateAPIView):
    """
    Registration of new user
    """
    permission_classes = (AllowAny,)
    model = get_user_model()
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


class DialogView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = DialogSerializer

    def get(self, request):
        id = request.query_params.get('id')
        for_user = request.query_params.get('for_user')
        name = request.query_params.get('name')
        if id:
            dialogs = Dialog.objects.filter(id=id)
        elif for_user:
            dialogs = Dialog.objects.filter(users=request.user)
        elif name:
            dialogs = Dialog.objects.filter(name=name)
        else:
            dialogs = Dialog.objects.all()
        dialog_serializer = DialogSerializer(dialogs, many=True)
        return Response({"dialogs": dialog_serializer.data})

    def post(self, request):
        # TODO make a chat name from the recipient's name
        dialog = {
            'name': request.data['name'],
            'users': [request.user.id]
        }
        serializer = DialogSerializer(data=dialog)
        if serializer.is_valid(raise_exception=True):
            dialog_saved = serializer.save()
        return Response({
            "success": "dialog '{}' created successfully".format(dialog_saved.name),
            "id_dialog": dialog_saved.id
        })


def get_base_context():
    return None


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
