from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio_home, name='inicio'),
    path('home/', views.home_redirect, name='home'),
]