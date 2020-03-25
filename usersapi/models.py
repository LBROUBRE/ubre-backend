from django.db import models
from django.urls import reverse

class Users(models.Model):
    dni = models.CharField(max_length=9, primary_key=True, default=0)
    name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email = models.EmailField()
    tlf = models.IntegerField(null=False)
    age = models.IntegerField()

    def __str__(self):
        return self.last_name, self.name
