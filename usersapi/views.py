from rest_framework import generics
from .models import User
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk=self.kwargs['pk']
        )
        return obj