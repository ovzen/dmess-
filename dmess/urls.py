"""dmess URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView

from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import SimpleRouter
from rest_framework_swagger.views import get_swagger_view

from dmess import settings
from main import views

router = SimpleRouter()

router.register(r'api/contacts', views.ContactViewSet, basename='contact')
router.register(r'api/dialog', views.DialogViewSet, basename='dialog')
router.register(r'api/messages', views.MessageViewSet, basename='message')
router.register(r'api/wiki', views.WikiPageViewSet, basename='wiki')
router.register(r'api/users', views.UserViewSet, basename='user')


schema_view = get_swagger_view(title='API')

urlpatterns = router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    path('api/accounts/', include('rest_registration.api.urls')),
    url(r'^docs/', schema_view),
    path('django_admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/admin/', include('admin.urls')),
    re_path('landing/', views.landing_view),
    re_path('auth/', TemplateView.as_view(template_name="auth.html"), name='Auth'),
    re_path(
        'admin/',
        staff_member_required(TemplateView.as_view(template_name="admin.html")),
        name="adminUI"
    ),
    re_path(
        '',
        login_required(TemplateView.as_view(template_name="index.html")),
        name="index",
    ),
    path('admin_tools/', include('admin_tools.urls')),
]
