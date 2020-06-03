"""
Dmess Routing
"""

from channels.routing import ProtocolTypeRouter, URLRouter
from dmess.middleware import WebsocketAuthMiddleware

import main.routing

application = ProtocolTypeRouter({
    'websocket': WebsocketAuthMiddleware(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})
