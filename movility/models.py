from django.db import models
from django.urls import reverse

class Usuarios(models.Model):
    dni = models.CharField(max_length=9, primary_key=True, default=0)
    name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField()
    age = models.IntegerField()
    tlf = models.IntegerField(null=False)

    def __str__(self):
        return '%s %s %s' % (self.dni, self.name, self.last_name)

class Vehiculos (models.Model):
    matricula = models.CharField(max_length=7, blank=False)
    modelo = models.CharField(max_length=25, blank=False)
    plazas = models.IntegerField()
    consumo = models.IntegerField()
    motor = models.CharField(max_length=25)
    categoria = models.CharField(max_length=25)

    def __str__(self):
        return '%s %s %s' % (self.matricula, self.modelo, self.plazas)

class Rutas (models.Model):
    origen = models.CharField(max_length=25, blank=False)
    destino = models.CharField(max_length=25, blank=False)
    fecha = models.DateTimeField()
    vehiculo = models.ForeignKey(Vehiculos, on_delete=models.DO_NOTHING)
    paradas = models.CharField(max_length=25, blank=False)
    conductor = models.CharField(max_length=25, blank=False)
    
    def __str__(self):
        return '%s %s %s' % (self.origen, self.destino, self.fecha)

class Solicitudes (models.Model):
    origen = models.CharField(max_length=25, blank=False)
    destino = models.CharField(max_length=25, blank=False)
    fechaHoraSalida = models.DateTimeField()
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    fechaHoraLlegada = models.DateTimeField()
    estado = models.CharField(max_length=25, blank=False)
    precio = models.IntegerField()

    def __str__(self):
        return '%s %s %s %s %s' % (self.origen, self.destino, self.fechaHoraSalida, self.fechaHoraLlegada, self.usuario)