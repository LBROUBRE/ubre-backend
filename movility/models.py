from django.db import models
from django.urls import reverse

class Usuarios(models.Model):
    dni = models.CharField(max_length=9, primary_key=True, default="00000000T")
    name = models.CharField(max_length=25, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    age = models.PositiveIntegerField(null=False, blank=False)
    tlf = models.CharField(max_length=10, unique=True, null=False, blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='')

    def __str__(self):
        return '%s %s %s' % (self.dni, self.name, self.last_name)

class Vehiculos (models.Model):
    matricula = models.CharField(max_length=7, primary_key=True)
    modelo = models.CharField(max_length=25, unique=False)
    plazas = models.PositiveIntegerField(null=False, blank=False)
    consumo = models.PositiveIntegerField(null=False, blank=False)
    MOTOR_CHOICES = (
        ('E', 'Electric'),
        ('G', 'Gasolina'),
        ('D', 'Diesel'),
    )
    motor = models.CharField(max_length=1, choices=MOTOR_CHOICES)
    CATEGORY_CHOICES = (
        ('T', 'Turismo'),
        ('B', 'Bus'),
    )
    categoria = models.CharField(max_length=1, choices=CATEGORY_CHOICES)

    def __str__(self):
        return '%s %s %s' % (self.matricula, self.categoria, self.plazas)

class Solicitudes (models.Model):
    origen = models.CharField(max_length=25, blank=False)
    destino = models.CharField(max_length=25, blank=False)
    fechaHoraSalida = models.DateTimeField(blank=False)
    usuario = models.ForeignKey(Usuarios, related_name='solicitudes', default=None, on_delete=models.CASCADE)
    fechaHoraLlegada = models.DateTimeField(blank=False)
    STATES_CHOICES = {
        ('PE', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('PA', 'Passed'),
    }
    estado = models.CharField(max_length=2, choices=STATES_CHOICES)
    precio = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s %s %s %s %s' % (self.origen, self.destino, self.fechaHoraSalida, self.fechaHoraLlegada, self.usuario)

class Conductores(models.Model):
    dni = models.CharField(max_length=9, primary_key=True, default=0)
    name = models.CharField(max_length=25, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    email = models.EmailField(max_length=255, unique=True)
    tlf = models.CharField(max_length=10, unique=True, null=False, blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='O')
    PERMISO_CHOICES = ( # El tipo de vehículo que puede conducir
        ('T', 'Turismos'),
        ('B', 'Buses')
    )
    permisoConduccion = models.CharField(max_length=1, choices=PERMISO_CHOICES)

    def __str__(self):
        return '%s %s %s %s' % (self.dni, self.name, self.last_name, self.permisoConduccion)

class Rutas (models.Model):
    origen = models.CharField(max_length=25, blank=False, unique=False)
    destino = models.CharField(max_length=25, blank=False, unique=False)
    vehiculo = models.ForeignKey(Vehiculos, related_name="rutas", on_delete=models.DO_NOTHING)
    #paradas = models.ForeignKey(Paradas, related_name="rutas", on_delete=models.DO_NOTHING)
    conductor = models.ForeignKey(Conductores, related_name='rutas', default=None, on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s %s' % (self.origen, self.destino)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['origen', 'destino'], name='unique_rutas')
        ]


class Tarificacion (models.Model):
    USER_CHOICES = (
        ('J', 'Jubilado'),
        ('I', 'Infantil'),
        ('A', 'Adulto'),
        ('P', 'Pensionistas'),
    )
    userType = models.CharField(max_length=1, choices=USER_CHOICES)
    discount = models.DecimalField(max_digits=2, decimal_places=2, default=0.0)
    
    def __str__(self):
        return '%s %s ' % (self.userType, self.discount)

class Paradas (models.Model):
    coordenadas = models.CharField(primary_key=True, max_length=255) #latitud, longitud
    fechaHora = models.DateTimeField()
    solicitudes = models.ManyToManyField(Solicitudes, related_name="paradas", blank=True)
    rutas = models.ManyToManyField(Rutas, related_name="paradas", blank=True)

    def __str__(self):
        return '%s %s ' % (self.coordenadas, self.fechaHora)