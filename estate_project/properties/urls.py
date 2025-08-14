# properties/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Главная — функция index
    path('', views.index, name='index'),

    # Детали — класс
    path('property/<int:prop_id>/', views.PropertyDetailView.as_view(), name='property_detail'),

    # Остальные — классы
    path('team/', views.TeamView.as_view(), name='team'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]