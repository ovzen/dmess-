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
from django.urls import path, include, re_path
from rest_framework_swagger.views import get_swagger_view
from django.conf.urls import url
from dmess import settings
from main import views

schema_view = get_swagger_view(title='API')

urlpatterns = [
    url(r'^docs/', schema_view),

    path('django_admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),

    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.UserView.as_view()),
    path('api/dialog/', views.DialogView.as_view()),

    path("frontend/src/knowledgebase/",
         TemplateView.as_view(template_name="knowledgebase.html"),
         name="knowledgebase",
         ),
    path("frontend/src/allUsers/",
         TemplateView.as_view(template_name="allUser.html"),
         name="allUser",
         ),

    re_path('auth/', TemplateView.as_view(template_name="Auth.html"), name='Auth'),
    re_path('admin/',
            login_required(TemplateView.as_view(template_name="admin.html")),
            name="adminUI"),
    re_path('',
            login_required(TemplateView.as_view(template_name="index.html")),
            name="index",
            ),
    # path('api/status/', views.StatusView.as_view()),
    # path('api/status/<int:pk>', views.StatusView.as_view()),
    # path('mypage/', views.my_page, name='mypage'),
    path('admin_tools/', include('admin_tools.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
