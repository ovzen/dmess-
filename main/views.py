from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from main.models import Dialog, UserProfile, Friend
from main.models import Message
from main.permissions import IsOwnerOrReadOnly
from main.serializers import MessageSerializer, FriendSerializer
from main.serializers import UserSerializer, DialogSerializer, MyTokenObtainPairSerializer, UserProfileSerializer


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


class FriendView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = FriendSerializer

    def get(self, request):
        friends = Friend.objects.all()
        serializer = FriendSerializer(friends, many=True)
        return Response({"friends": serializer.data})

    def post(self, request):
        friend = request.data.get('friend')
        serializer = FriendSerializer(data=friend)
        if serializer.is_valid(raise_exception=True):
            friend_saved = serializer.save()
        return Response({
            "success": "Friend {} created successfully".format(friend_saved.friend_id),
            "friend_id": friend_saved.friend_id
        })

    def delete(self, request, pk):
        friend = get_object_or_404(Friend.objects.all(), pk=pk)
        friend.delete()
        return Response({
            "message": "Friend with id `{}` has been deleted.".format(pk)
        }, status=204)


class DialogView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = DialogSerializer
    def get(self, request, pk=None):

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

    def post(self, request, pk=None):
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

    def put(self, request, pk):
        saved_dialog = get_object_or_404(Dialog.objects.all(), pk=pk)
        data = request.data.get('dialog')
        serializer = DialogSerializer(instance=saved_dialog, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            dialog_saved = serializer.save()
        return Response({
            "success": "Dialog '{}' updated successfully".format(dialog_saved.title)
        })

    def delete(self, request, pk):
        dialog = get_object_or_404(Dialog.objects.all(), pk=pk)
        dialog.delete()
        return Response({
            "message": "Dialog with id `{}` has been deleted.".format(pk)
        }, status=204)


def get_base_context():
    return None


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
