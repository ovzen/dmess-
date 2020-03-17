from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView, get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from main.models import Dialog
from main.serializers import UserSerializer, DialogSerializer, MyTokenObtainPairSerializer



class UserView(CreateAPIView):
    """
       Registration of new user
    """
    permission_classes = (AllowAny,)
    model = get_user_model()
    serializer_class = UserSerializer


class DialogView(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, pk=None):

        id = request.query_params.get('id')
        for_user = request.query_params.get('for_user')
        if id:
            dialogs = Dialog.objects.filter(id=id)
        elif for_user:
            dialogs = Dialog.objects.filter(users=request.user)
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
