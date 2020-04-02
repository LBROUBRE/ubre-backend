from django.urls import path
from .views import usuarios_list, usuarios_detail, solicitudes_list

urlpatterns = [
    path('users/', usuarios_list),
    path('users/<pk>/', usuarios_detail),
    path('requests/', solicitudes_list),
]