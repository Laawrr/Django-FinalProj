from django.urls import path
from . import views

urlpatterns = [
    path('post', views.message_app, name='message_app'),  
]
