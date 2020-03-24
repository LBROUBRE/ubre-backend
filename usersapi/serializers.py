from .models import Users
from rest_framework import serializers

class UsersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = (
            'name',
            'last_name',
            'email',
            'tlf',
            'age'
        )