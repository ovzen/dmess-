from django.urls import path

from . import views

urlpatterns = [
    path('<str:chat_number>/', views.index_chat, name='index')
]