import uuid
from django.db import models
from ubrebackend.app.user.models import User


class UserProfile(models.Model):
    dni = models.CharField(primary_key=True, max_length=9)
    #id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=50, unique=False)
    last_name = models.CharField(max_length=50, unique=False)
    tlf = models.CharField(max_length=10, unique=True, null=False, blank=False)
    age = models.PositiveIntegerField(null=False, blank=False)

    def __str__(self):
        return '%s %s %s' % (self.dni, self.name, self.last_name)

    class Meta:
        '''
        to set table name in database
        '''
        db_table = "profile"