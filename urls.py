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
from django.urls import path, include
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('main.urls')),
    path('api/chat/', views.DialogView.as_view()),
    path('', views.index_page, name='index'),
    path('dialogs/', views.dialog_page, name='dialogs'),
    path('about/', views.about_page, name='about'),
    path('sitemap.xml', views.sitemap_page, name='about'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register_page, name='register' ),
    path('api/register/', views.CreateUserView.as_view(), name='api_register'),
    path('api/status/', views.StatusView.as_view()),
    path('api/status/<int:pk>', views.StatusView.as_view()),
    path('mypage/', views.my_page, name='mypage'),
    path('admin_tools/', include('admin_tools.urls')),
]