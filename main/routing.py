"""
Main Routing
"""

from django.urls import re_path, path

from . import consumers

websocket_urlpatterns = [
    path('ws/chat/system/', consumers.System),
    path(
        'ws/dialog_notifications/',
        consumers.DialogNotificationConsumer,
        name='dialog_notifications'
    ),
    path('ws/users/', consumers.UserAPIConsumer),
    re_path(r'ws/chat/(?P<chat_number>[\w-]+)/$', consumers.ChatConsumer)
]
