from django.contrib import admin
from django.urls import path, include
from main.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('api-auth/', include('rest_framework.urls')),
    #path('', main_view, name="main_view"),
    #path('signup_view/', signup_view, name="signup_view"),
    #path('<str:ref_code>', main_view, name="main_view"),
]
