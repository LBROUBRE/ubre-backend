from django.urls import path
from .views import *

urlpatterns = [
    path('usuarios/', usuarios_list),
    path('usuarios/<pk>/', usuarios_detail),
    path('rutas/<str:origin>/<str:dest>', RouteResponseView.as_view()),
    path('solicitudes/', SolicitudesRegistrationView.as_view()),
    path('solicitudes/<pk>', solicitudes_detail)
]