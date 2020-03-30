from django.db import models
from django.urls import reverse

class Usuarios(models.Model):
    dni = models.CharField(max_length=9, primary_key=True, default=0)
    name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField()
    age = models.IntegerField()
    tlf = models.IntegerField(null=False)
    #solicitudes = models

    def __str__(self):
        return self.last_name, self.name

class Vehiculos (models.Model):
    matricula = models.CharField(max_length=7, blank=False)
    modelo = models.CharField(max_length=25, blank=False)
    plazas = models.IntegerField()
    consumo = models.IntegerField()
    motor = models.CharField(max_length=25)
    categoria = models.CharField(max_length=25)

    def __str__(self):
        return self.matricula, self.plazas

class Rutas (models.Model):
    origen = models.IntegerField(null=False)
    destino = models.IntegerField(null=False)
    fecha = models.DateTimeField()
    vehiculo = models.ForeignKey(Vehiculos, on_delete=models.DO_NOTHING)
    paradas = models.IntegerField(null=False)
    conductor = models.CharField(max_length=50)
    
    def __str__(self):
        return self.origen, self.destino, self.fecha

class Solicitudes (models.Model):
    origen = models.CharField(max_length=50)
    destino = models.CharField(max_length=50)
    fechaHoraSalida = models.DateField()
    idUsuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE)
    fechaHoraLlegada = models.DateField()
    estado = models.CharField(max_length=25, blank=False)
    precio = models.IntegerField()

    def __str__(self):
        return self.origen, self.destino, self.fechaHoraSalida, self.idUsuario