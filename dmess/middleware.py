from channels.auth import UserLazyObject
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth.models import User, AnonymousUser
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication



class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        try:
            cookie = request.META.get('HTTP_COOKIE').split(' Authentication=')
        except AttributeError:
            return self.get_response(request)
        if len(cookie) > 1:
            token = cookie[1].split(';')[0]
            # Code to be executed for each request before
            # the view (and later middleware) are called.
            val_token=JWTTokenUserAuthentication().get_validated_token(token)
            try:
                authenticated = JWTTokenUserAuthentication().get_user(val_token).id
                if authenticated:
                    request.user = User.objects.get(id=authenticated)
                else:
                    request.user = AnonymousUser
            except exceptions.AuthenticationFailed:
                request.user = AnonymousUser

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response

@database_sync_to_async
def get_user(scope):
    """
    Return the user model instance associated with the given scope.
    If no user is retrieved, return an instance of `AnonymousUser`.
    """
    cookie = str(dict(scope['headers'])[b'cookie'])[2:-1].split(' Authentication=')
    user = AnonymousUser
    if len(cookie) > 1:
        token = cookie[1].split(';')[0]
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        val_token = JWTTokenUserAuthentication().get_validated_token(token)
        try:
            authenticated = JWTTokenUserAuthentication().get_user(val_token).id
            if authenticated:
                user = User.objects.get(id=authenticated)
            else:
                user = AnonymousUser
        except exceptions.AuthenticationFailed:
            user = AnonymousUser
    return user


class WebsocketAuthMiddleware(BaseMiddleware):
    """
    Middleware which populates scope["user"] from a Django session.
    Requires SessionMiddleware to function.
    """

    def populate_scope(self, scope):
        # Make sure we have a session
        # Add it to the scope if it's not there already
        if "user" not in scope:
            scope["user"] = UserLazyObject()

    async def resolve_scope(self, scope):
        scope["user"]._wrapped = await get_user(scope)

