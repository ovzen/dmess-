from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/system/', consumers.System),
    re_path(r'ws/ChatUser/(?P<chat_number>\w+)/$', consumers.ChatConsumer),
]
