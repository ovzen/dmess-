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
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import SimpleRouter
from django.urls import path, include, re_path
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url
from dmess import settings
from main import views

router = SimpleRouter()
router.register(r'api/contacts', views.ContactViewSet)
router.register(r'api/dialog', views.DialogViewSet)

schema_view = get_swagger_view(title='API')

urlpatterns = router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + [
    url(r'^docs/', schema_view),

    path('django_admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),

    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.UserView.as_view()),
    path('api/messages/', views.MessageView.as_view()),
    path('api/users/<int:pk>', views.UserProfileView.as_view()),
    path('api/activity_feed/', views.ActivityFeedView.as_view()),
    path('api/admin/', include('admin.urls')),
    re_path('auth/', TemplateView.as_view(template_name="Auth.html"), name='Auth'),
    re_path(
        'admin/',
        login_required(TemplateView.as_view(template_name="admin.html")),
        name="adminUI"
    ),
    re_path(
        '',
        login_required(TemplateView.as_view(template_name="index.html")),
        name="index",
    ),
    path('admin_tools/', include('admin_tools.urls')),

]
