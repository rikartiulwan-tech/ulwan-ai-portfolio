from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/inquiry/', views.submit_inquiry, name='submit_inquiry'),
    path('api/chat/', views.ai_chat, name='ai_chat'),
]