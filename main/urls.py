from django.contrib import admin
from django.urls import path, include
from .views import *
from . import views


urlpatterns = [
    path('', index, name='home'),
    path('account', acc, name='acc'),
    path('register', views.register, name='reg'),
    path('login', views.login_user, name='login'),
    path("logout_user", views.logout_user, name='logout_user'),
]