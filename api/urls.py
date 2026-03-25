from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # 1. THE FRONTEND UI (This serves your beautiful HTML page)
    path('', views.index, name='home'), 

    # 2. THE BACKEND API (The invisible pipeline your JavaScript talks to)
    path('chat/', views.ChatbotView.as_view(), name='chat'), 
    
    # 3. ADMIN PORTAL
    path('add-hotel/', views.add_hotel_room, name='add_hotel_room'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('calculator/', views.carbon_calculator, name='calculator'),
    
]