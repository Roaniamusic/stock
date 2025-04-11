from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Autenticación de usuarios
    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='usuarios/logout.html'), name='logout'),
    
    # Gestión de usuarios
    path('registro/', views.register, name='register'),
    path('perfil/', views.profile, name='profile'),
    path('cambiar-password/', views.change_password, name='change_password'),
    path('lista-usuarios/', views.UserListView.as_view(), name='user_list'),
]