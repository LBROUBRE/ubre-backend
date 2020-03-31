from django.urls import path
from .views import *

urlpatterns = [
    path('users/', usuarios_list),
    path('users/<pk>/', usuarios_detail),
    path('request/<str:pk>/<str:origin>/<str:dest>/<string:req_date>', RouteResponseView.as_view()),
]