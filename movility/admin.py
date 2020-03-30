from django.contrib import admin
from .models import Usuarios, Vehiculos, Solicitudes, Rutas

# Register your models here.
admin.site.register(Usuarios)
admin.site.register(Vehiculos)
admin.site.register(Solicitudes)
admin.site.register(Rutas)