from django.urls import path
from .views import *

urlpatterns = [
    path('<str:origin>/<str:dest>', RouteResponseView.as_view())
]