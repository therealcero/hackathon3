"""
URL configuration for AgriSense project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from app import views

urlpatterns = [
    path('', views.index, name='login'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('search_crops/', views.search_crops, name='search_crops'),
    path('send_message/', views.send_message, name='send_message'),
    path('send_request/', views.send_request, name='send_request'),
    path('image_search/', views.image_search, name='image_search'),
    # farmer
    path('farmer_chat/', views.farmer_chat, name='farmer_chat'),
    path('farmer_profile/', views.farmer_profile, name='farmer_profile'),
    path('farmer_profile_save/', views.farmer_profile_save, name='farmer_profile_save'),
    path('farmer_dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('farmer_notification/', views.farmer_notification, name='farmer_notification'),
    # expert
    path('expert_chat/', views.expert_chat, name='expert_chat'),
    path('expert_upload/', views.expert_upload, name='expert_upload'),
    path('expert_profile/', views.expert_profile, name='expert_profile'),
    path('expert_dashboard/', views.expert_dashboard, name='expert_dashboard'),
]