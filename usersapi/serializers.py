from .models import Users
from rest_framework import serializers

class UsersSerializer(serializers.ModelSerializer):
    dni = serializers.CharField(required=True)
    name = serializers.CharField(required=True, max_length=25)
    last_name = serializers.CharField(required=True, max_length=50)
    email = serializers.EmailField(required=True)
    tlf = serializers.IntegerField(required=True)
    age = serializers.IntegerField(required=False)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de User, dado el 'validated_data'
        """
        return Users.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('validated_data', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.tlf = validated_data.get('tlf', instance.tlf)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance

    class Meta:
        model = Users
        fields = ['dni', 'name', 'last_name', 'email', 'tlf', 'age']