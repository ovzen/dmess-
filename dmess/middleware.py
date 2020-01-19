from django.contrib.auth.models import User
from rest_framework_simplejwt.authentication import JWTTokenUserAuthentication


class SimpleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        cookie=request.META.get('HTTP_COOKIE').split(' Authentication=')
        if len(cookie) > 1:
            token = cookie[1].split(';')[0]
            # Code to be executed for each request before
            # the view (and later middleware) are called.
            val_token=JWTTokenUserAuthentication().get_validated_token(token)
            authenticated = JWTTokenUserAuthentication().get_user(val_token).id
            request.user = User.objects.get(id=authenticated)
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response