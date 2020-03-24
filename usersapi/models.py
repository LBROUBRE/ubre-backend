from django.db import models

class Users(models.Model):
    name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    tlf = models.IntegerField()
    age = models.IntegerField()

    def __str__(self):
        return self.last_name, self.name