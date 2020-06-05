"""
Маршрутизация WS соединений в приложении
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
    path('ws/messages/', consumers.MessageAPIConsumer),
]
