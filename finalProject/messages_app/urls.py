from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_app, name='message_app'),
    path('get_messages/', views.get_messages, name='get_messages'),
]
