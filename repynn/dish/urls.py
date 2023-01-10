from django.urls import path
from . import views

app_name = 'dishes'

urlpatterns = [
    path('menu', views.dish_menu, name='dish_menu'),
    path('<int:pid>/', views.dish_detail, name="dish_detail")
]
