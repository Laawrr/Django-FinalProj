from django.urls import path
from . import views

urlpatterns = [
    path('', views.message_app, name='message_app'),  
]
