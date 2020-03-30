from .models import Usuarios, Rutas, Vehiculos, Solicitudes
from rest_framework import serializers

"""""""""""""""""""""""""""
        Usuarios
"""""""""""""""""""""""""""
class UsuariosSerializer(serializers.ModelSerializer):
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
        return Usuarios.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.tlf = validated_data.get('tlf', instance.tlf)
        instance.age = validated_data.get('age', instance.age)
        instance.save()
        return instance

    class Meta:
        model = Usuarios
        fields = ['dni', 'name', 'last_name', 'email', 'tlf', 'age']


"""""""""""""""""""""""""""
        Rutas
"""""""""""""""""""""""""""
class RutasSerializer(serializers.ModelSerializer):
    origen = serializers.IntegerField() # identificador de la ubicación
    destino = serializers.IntegerField() # identificador de la ubicación
    fechaHora = serializers.DateField()
    vehiculo = serializers.CharField(required=True)
    paradas = serializers.CharField(required=True)
    conductor = serializers.CharField(required=True)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de User, dado el 'validated_data'
        """
        return Rutas.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        instance.origen = validated_data('origen', instance.origen)
        instance.destino = validated_data('destino', instance.destino)
        instance.fechaHora = validated_data('fechaHora', instance.fechaHora)
        instance.vehiculo = validated_data.get('vehiculo', instance.vehiculo)
        instance.paradas = validated_data.get('paradas', instance.paradas)
        instance.conductor = validated_data.get('conductor', instance.conductor)
        instance.save()
        return instance

    class Meta:
        model = Rutas
        fields = ['origen', 'destino', 'fecha', 'vehiculo', 'paradas', 'conductor']


"""""""""""""""""""""""""""
        Vehiculos
"""""""""""""""""""""""""""
class VehiculosSerializer(serializers.ModelSerializer):
    matricula = serializers.CharField(required=True)
    modelo = serializers.CharField(required=True)
    plazas = serializers.IntegerField(required=True)
    consumo = serializers.IntegerField(required=True)
    motor = serializers.CharField(required=True)
    categoria = serializers.CharField(required=True)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de User, dado el 'validated_data'
        """
        return Vehiculos.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        instance.matricula = validated_data('matricula', instance.matricula)
        instance.modelo = validated_data('modelo', instance.modelo)
        instance.plazas = validated_data('plazas', instance.plazas)
        instance.consumo = validated_data.get('consumo', instance.consumo)
        instance.motor = validated_data.get('motor', instance.motor)
        instance.categoria = validated_data.get('categoria', instance.categoria)
        instance.save()
        return instance

    class Meta:
        model = Rutas
        fields = ['matricula', 'modelo', 'plazas', 'consumo', 'motor', 'categoria']


"""""""""""""""""""""""""""
        Solicitudes
"""""""""""""""""""""""""""
class SolicitudesSerializer(serializers.ModelSerializer):
    origen = serializers.CharField(required=True)
    destino = serializers.CharField(required=True)
    fechaHoraSalida = serializers.DateField(required=True)
    idUsuario = serializers.CharField(required=True)
    fechaHoraLlegada = serializers.DateTimeField()
    estado = serializers.CharField(required=True)
    precio = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de User, dado el 'validated_data'
        """
        return Solicitudes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        instance.origen = validated_data('origen', instance.origen)
        instance.destino = validated_data('destino', instance.destino)
        instance.fechaHoraSalida = validated_data('fechaHoraSalida', instance.fechaHoraSalida)
        instance.idUsuario = validated_data.get('idUsuario', instance.idUsuario)
        instance.fechaHoraLlegada = validated_data.get('fechaHoraLlegada', instance.fechaHoraLlegada)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.save()
        return instance

    class Meta:
        model = Rutas
        fields = ['origen', 'destino', 'fechaHoraSalida', 'idUsuario', 'fechaHoraLlegada', 'estado', 'precio']