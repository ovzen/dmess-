from rest_framework.routers import SimpleRouter

from .views import InviteViewSet

router = SimpleRouter()
router.register(r'invites', InviteViewSet)
urlpatterns = router.urls
