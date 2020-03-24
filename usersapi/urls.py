from django.urls import path
from .views import *

urlpatterns = [
    path('', UsersList.as_view())
]