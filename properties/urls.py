# properties/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PropertyListView.as_view(), name='index'),
    path('property/<int:pk>/', views.PropertyDetailView.as_view(), name='property_detail'),
    path('team/', views.TeamView.as_view(), name='team'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', views.LogoutUserView.as_view(), name='logout'),
]