from .models import *
from rest_framework import serializers


"""""""""""""""""""""""""""
        Solicitudes
"""""""""""""""""""""""""""
class SolicitudesSerializer(serializers.ModelSerializer):
    origen = serializers.CharField(required=False)
    destino = serializers.CharField(required=False)
    fechaHoraSalida = serializers.DateTimeField(required=False)
    fechaHoraLlegada = serializers.DateTimeField(required=False)
    estado = serializers.CharField(required=False)
    precio = serializers.IntegerField(required=False)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de Solicitud, dado el 'validated_data'
        """
        return Solicitudes.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        if 'origen' in validated_data:
            instance.origen = validated_data.get('origen', instance.origen)
        if 'destino' in validated_data:
            instance.destino = validated_data.get('destino', instance.destino)
        if 'fechaHoraSalida' in validated_data:
            instance.fechaHoraSalida = validated_data.get('fechaHoraSalida', instance.fechaHoraSalida)
        if 'fechaHoraLlegada' in validated_data:
            instance.fechaHoraLlegada = validated_data.get('fechaHoraLlegada', instance.fechaHoraLlegada)
        if 'estado' in validated_data:
            instance.estado = validated_data.get('estado', instance.estado)
        if 'precio' in validated_data:
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
    dni = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    tlf = serializers.CharField(required=False)
    age = serializers.IntegerField(required=False)
    gender = serializers.CharField(required=False)
    solicitudes = SolicitudesSerializer(many=False)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de User, dado el 'validated_data'
        """
        return Usuarios.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de Solicitud creada, dado un 'validated_data'
        """
        if 'name' in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if 'last_name' in validated_data:
            instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'email' in validated_data:
            instance.email = validated_data.get('email', instance.email)
        if 'tlf' in validated_data:
            instance.tlf = validated_data.get('tlf', instance.tlf)
        if 'age' in validated_data:
            instance.age = validated_data.get('age', instance.age)
        if 'gender' in validated_data:
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
    coordenadas = serializers.CharField(required=False)
    fechaHora = serializers.DateTimeField(required=False)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de Conductor, dado el 'validated_data'
        """
        return Paradas.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Actualiza y retorna la instancia de User creada, dado un 'validated_data'
        """
        if 'coordenadas' in validated_data:
            instance.coordenadas = validated_data.get('coordenadas', instance.coordenadas)
        if 'fechaHora' in validated_data:
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
    origen = serializers.CharField(required=False) # identificador de la ubicación
    destino = serializers.CharField(required=False) # identificador de la ubicación
    geometry = serializers.CharField(required=False)
    paradas = ParadasSerializer(many=True)

    def create(self, validated_data):
        """
        Crea y retorna una nueva instancia de User, dado el 'validated_data'
        """
        ruta = Rutas.objects.create(
            origen=validated_data.get("origen"),
            destino=validated_data.get("destino"),
            geometry=validated_data.get("geometry"),
            vehiculo=validated_data.get("vehiculo")
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
        if 'origen' in validated_data:
            instance.origen = validated_data.get('origen', instance.origen)
        if 'destino' in validated_data:
            instance.destino = validated_data.get('destino', instance.destino)
        if 'geometry' in validated_data:
            instance.geometry = validated_data.get('geometry', instance.geometry)
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
        if 'matricula' in validated_data:
            instance.matricula = validated_data.get('matricula', instance.matricula)
        if 'modelo' in validated_data:
            instance.modelo = validated_data.get('modelo', instance.modelo)
        if 'plazas' in validated_data:
            instance.plazas = validated_data.get('plazas', instance.plazas)
        if 'consumo' in validated_data:
            instance.consumo = validated_data.get('consumo', instance.consumo)
        if 'motor' in validated_data:
            instance.motor = validated_data.get('motor', instance.motor)
        if 'categoria' in validated_data:
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
    dni = serializers.CharField(required=False)
    name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    tlf = serializers.CharField(required=False)
    gender = serializers.CharField(required=False)
    permisoConduccion = serializers.CharField(required=False)
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
        if 'dni' in validated_data:
            instance.dni = validated_data.get('dni', instance.dni)
        if 'name' in validated_data:
            instance.name = validated_data.get('name', instance.name)
        if 'last_name' in validated_data:
            instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'email' in validated_data:
            instance.email = validated_data.get('email', instance.email)
        if 'tlf' in validated_data:
            instance.tlf = validated_data.get('tlf', instance.tlf)
        if 'gender' in validated_data:
            instance.gender = validated_data.get('gender', instance.gender)
        if 'permisoConduccion' in validated_data:
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
        if 'user_type' in validated_data:
            instance.user_type = validated_data.get('user_type', instance.user_type)
        if 'discount' in validated_data:
            instance.discount = validated_data.get('discount', instance.discount)
        instance.save()
        return instance

    class Meta:
        model = Tarificacion
        fields = "__all__"

