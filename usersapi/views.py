from rest_framework import generics
from .models import Users
from .serializers import UsersSerializer
from django.shortcuts import get_object_or_404

class UsersList(generics.ListCreateAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(
            queryset,
            pk=self.kwargs['pk']
        )
        return obj