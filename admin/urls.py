from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import InviteViewSet, RegisterStatView, UserStatView, GitlabMetricsView

router = SimpleRouter()
router.register(r'invites', InviteViewSet)
urlpatterns = router.urls
urlpatterns.append(path('register/stat/', RegisterStatView.as_view()))
urlpatterns.append(path('users/stat/', UserStatView.as_view()))
urlpatterns.append(path('gitlabmetrics/', GitlabMetricsView.as_view()))
