from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = 'account'

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('homepage/', views.homepage, name='homepage'),
    path('aboutus/', views.aboutUs, name='about_us'),
]
