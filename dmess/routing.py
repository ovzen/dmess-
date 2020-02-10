from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import main.routing
from dmess.middleware import WebsocketAuthMiddleware

application = ProtocolTypeRouter({
    'websocket': WebsocketAuthMiddleware(
        URLRouter(
            main.routing.websocket_urlpatterns
        )
    ),
})