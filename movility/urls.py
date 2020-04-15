from django.urls import path
from .views import *

urlpatterns = [
    # Users
    path('users/', usuarios_list),
    path('users/<pk>', usuarios_detail),

    # Requests
    path('requests/', solicitudes_list),
    path('requests/<pk>', solicitudes_detail),

    # Drivers
    path('drivers/', conductores_list),
    path('drivers/<pk>', conductores_detail),

    # Taxes
    path('taxes/', tarificacion_list),
    path('taxes/<pk>', tarificacion_detail),

    # VirtualStops
    path('stops/', stops_list),
    path('stops/<pk>', stops_detail),

    # Vehicles
    path('vehicles/', vehiculos_list),
    path('vehicles/<pk>', vehiculos_detail),

    # Routes
    path('routes/', rutas_list),
    path('routes/<pk>', rutas_detail),
    
    # Test
    path('test/', test_vroom), # TODO remove

]