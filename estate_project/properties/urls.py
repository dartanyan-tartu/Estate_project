from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('property/<int:prop_id>/', views.property_detail, name='property_detail'),
    path('team/', views.team, name='team'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register_page, name='register'),
    path('profile/', views.profile_page, name='profile'),
    path('logout/', views.logout_page, name='logout')
]