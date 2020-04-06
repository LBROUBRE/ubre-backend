from .models import *
from rest_framework import serializers


"""""""""""""""""""""""""""
        Solicitudes
"""""""""""""""""""""""""""
class SolicitudesSerializer(serializers.ModelSerializer):
    origen = serializers.CharField(required=True)
    destino = serializers.CharField(required=True)
    fechaHoraSalida = serializers.DateTimeField(required=True)
    fechaHoraLlegada = serializers.DateTimeField()
    estado = serializers.CharField(required=True)
    precio = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de Solicitud, dado el 'validated_data'
        """
        return Solicitudes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        instance.origen = validated_data('origen', instance.origen)
        instance.destino = validated_data('destino', instance.destino)
        instance.fechaHoraSalida = validated_data('fechaHoraSalida', instance.fechaHoraSalida)
        instance.fechaHoraLlegada = validated_data.get('fechaHoraLlegada', instance.fechaHoraLlegada)
        instance.estado = validated_data.get('estado', instance.estado)
        instance.precio = validated_data.get('precio', instance.precio)
        instance.save()
        return instance

    class Meta:
        model = Solicitudes
        fields = "__all__"
        extra_kwargs = {'paradas':{'required': False}}


"""""""""""""""""""""""""""
        Usuarios
"""""""""""""""""""""""""""

class UsuariosSerializer(serializers.ModelSerializer):
    dni = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    tlf = serializers.CharField(required=True)
    age = serializers.IntegerField(required=False)
    gender = serializers.CharField(required=False)
    solicitudes = SolicitudesSerializer(many=True)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de User, dado el 'validated_data'
        """
        return Usuarios.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de Solicitud creada, dado un 'validated_data'
        """
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.tlf = validated_data.get('tlf', instance.tlf)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        return instance

    class Meta:
        model = Usuarios
        fields = "__all__"
        extra_kwargs = {'solicitudes':{'required': False}}


"""""""""""""""""""""""""""
        Paradas
"""""""""""""""""""""""""""
class ParadasSerializer(serializers.ModelSerializer):
    coordenadas = serializers.CharField(required=True)
    fechaHora = serializers.DateTimeField(required=True)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de Conductor, dado el 'validated_data'
        """
        return Paradas.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        instance.coordenadas = validated_data.get('coordenadas', instance.coordenadas)
        instance.fechaHora = validated_data.get('fechaHora', instance.fechaHora)
        instance.save()
        return instance

    class Meta:
        model = Paradas
        fields = "__all__"
        extra_kwargs = {'solicitudes':{'required': False}}


"""""""""""""""""""""""""""
        Rutas
"""""""""""""""""""""""""""
class RutasSerializer(serializers.ModelSerializer):
    origen = serializers.CharField(required=True) # identificador de la ubicación
    destino = serializers.CharField(required=True) # identificador de la ubicación
    paradas = ParadasSerializer(many=True)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de User, dado el 'validated_data'
        """
        ruta = Rutas.objects.create(
            origen=validated_data.get("origen"),
            destino=validated_data.get("destino")
        )
        ruta.save()
        paradas = validated_data.get('paradas')
        for parada in paradas:
            Paradas.objects.create(rutas=ruta, **parada)
        return validated_data

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        instance.origen = validated_data('origen', instance.origen)
        instance.destino = validated_data('destino', instance.destino)
        instance.save()
        return instance

    class Meta:
        model = Rutas
        fields = "__all__"
        extra_kwargs = {'paradas':{'required': False}, 'solicitudes':{'required': False}}


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
    rutas = RutasSerializer(many=True, required=False)

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
        model = Vehiculos
        fields = "__all__"
        extra_kwargs = {'rutas':{'required': False}}

"""""""""""""""""""""""""""
        Conductores
"""""""""""""""""""""""""""
class ConductoresSerializer(serializers.ModelSerializer):
    dni = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    tlf = serializers.CharField(required=True)
    gender = serializers.CharField(required=False)
    permisoConduccion = serializers.CharField(required=True)
    rutas = RutasSerializer(many=True)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de Conductor, dado el 'validated_data'
        """
        return Conductores.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        instance.name = validated_data.get('name', instance.name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.tlf = validated_data.get('tlf', instance.tlf)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.permisoConduccion = validated_data.get('permisoConduccion', instance.permisoConduccion)
        instance.save()
        return instance

    class Meta:
        model = Conductores
        fields = "__all__"
        extra_kwargs = {'rutas':{'required': False}}

"""""""""""""""""""""""""""
        Tarificación
"""""""""""""""""""""""""""
class TarificacionSerializer(serializers.ModelSerializer):
    user_type = serializers.CharField(required=True)
    discount = serializers.DecimalField(required=True, max_digits=2, decimal_places=2)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de Conductor, dado el 'validated_data'
        """
        return Tarificacion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        instance.user_type = validated_data.get('user_type', instance.user_type)
        instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        return instance

    class Meta:
        model = Tarificacion
        fields = "__all__"

