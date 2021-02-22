from django.contrib import admin
from django.urls import path
from . import views


app_name = 'User'

urlpatterns = [
    path('', views.home_view, name="home"),
    path('logout/', views.logout_view, name="logout"),
    path('login/', views.login_view, name="login"),
    path('signup/', views.signup_view, name="signup"),
    path('sent/', views.activation_sent_view, name="activation_sent"),
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
]
