from django.contrib import admin
from django.urls import path
from . import views


app_name = 'User'

urlpatterns = [
    path('', views.home_view, name="home"),
    path('signup/', views.signup_view, name="signup"),
    path('logout/', views.logout_view, name="logout"),
    path('login/', views.login_view, name="login")
]
