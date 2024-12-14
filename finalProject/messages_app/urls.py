from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_app, name='message_app'),
    path('api/messages/', views.message_api, name='message-api'),
]
