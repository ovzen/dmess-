from django.urls import path

from . import views

urlpatterns = [
    path('', views.index_chat, name='index'),
]