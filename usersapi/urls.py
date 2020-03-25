from django.urls import path
from .views import *
from usersapi import views

urlpatterns = [
    path('', views.users_list),
    path('<pk>/', views.users_detail),
]