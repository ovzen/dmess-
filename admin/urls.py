from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import InviteViewSet, RegisterStatView, UserStatView, GitlabMetricsView

router = SimpleRouter()
router.register(r'invites', InviteViewSet, basename='invite')
urlpatterns = router.urls
urlpatterns.append(path('register/stat/', RegisterStatView.as_view(), name='register-stat'))
urlpatterns.append(path('users/stat/', UserStatView.as_view(), name='user-stat'))
urlpatterns.append(path('gitlabmetrics/', GitlabMetricsView.as_view(), name='gitlabmetrics'))
