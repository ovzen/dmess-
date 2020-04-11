from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import InviteViewSet, StatisticsView

router = SimpleRouter()
router.register(r'invites', InviteViewSet)
urlpatterns = router.urls
urlpatterns.append(path('statistics/', StatisticsView.as_view()))
