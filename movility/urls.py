from django.urls import path
from .views import usuarios_list, usuarios_detail, solicitudes_list, _test_

urlpatterns = [
    path('users/', usuarios_list),
    path('users/<pk>/', usuarios_detail),
    path('requests/', solicitudes_list),
    path('test', _test_) # TODO remove
]