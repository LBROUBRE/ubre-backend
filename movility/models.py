# TODO: on_delete = CASCADE

from django.db import models
from django.urls import reverse
import uuid
from ubrebackend.app.profile.models import UserProfile

class Vehiculos(models.Model):
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


class Solicitudes(models.Model):
    origen = models.CharField(max_length=50, blank=False)
    destino = models.CharField(max_length=50, blank=False)
    fechaHoraSalida = models.DateTimeField(blank=True, default=None)
    fechaHoraLlegada = models.DateTimeField(blank=True, default=None)
    usuario = models.ForeignKey(UserProfile, related_name='solicitudes', default=None, on_delete=models.CASCADE)
    STATES_CHOICES = {
        ('PE', 'Pending'),
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('PA', 'Passed'),
    }
    estado = models.CharField(max_length=2, choices=STATES_CHOICES, default="PE")
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
    PERMISO_CHOICES = (  # El tipo de vehículo que puede conducir
        ('T', 'Turismos'),
        ('B', 'Buses')
    )
    permisoConduccion = models.CharField(max_length=1, choices=PERMISO_CHOICES)

    def __str__(self):
        return '%s %s %s %s' % (self.dni, self.name, self.last_name, self.permisoConduccion)


class Rutas(models.Model):
    origen = models.CharField(max_length=50, blank=False, unique=False)
    destino = models.CharField(max_length=50, blank=False, unique=False)
    geometry = models.CharField(max_length=131072, blank=False, unique=False)
    vehiculo = models.ForeignKey(Vehiculos, default=None, related_name="rutas", on_delete=models.DO_NOTHING)
    # conductor = models.ForeignKey(Conductores, related_name='rutas', default=None, on_delete=models.DO_NOTHING)

    def __str__(self):
        return '%s %s' % (self.origen, self.destino)


class Tarificacion(models.Model):
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


class ParadasVirtuales(models.Model):
    coordenadas = models.CharField(max_length=50, blank=False, unique=False)  # latitud, longitud

    def __str__(self):
        return '%s ' % self.coordenadas


class Steps(models.Model):
    parada = models.ForeignKey(ParadasVirtuales, related_name="steps", on_delete=models.CASCADE)  # latitud, longitud
    fechaHora = models.DateTimeField()
    solicitudes = models.ForeignKey(Solicitudes, related_name="steps", null=True, blank=True,
                                    on_delete=models.CASCADE)
    rutas = models.ForeignKey(Rutas, related_name="steps", blank=True, on_delete=models.CASCADE)  # TODO: to check

    def __str__(self):
        return '%s %s ' % (self.parada, self.fechaHora)

