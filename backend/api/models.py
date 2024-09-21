from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _
from django.db import models


class User(AbstractUser):
    name=models.CharField(_("Name of User"), blank=True, max_length=255)
    pass

class Owner(models.Model):
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    make = models.CharField(max_length=255)
    model = models.CharField(max_length=255)
    year = models.IntegerField()
    fuel_type = models.CharField(max_length=50)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.make} {self.model}"

class Trip(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    start_location = models.CharField(max_length=255)
    end_location = models.CharField(max_length=255)
    distance_traveled = models.DecimalField(max_digits=10, decimal_places=2)

class Sensor(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    sensor_reading = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField()

class Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    maintenance_type = models.CharField(max_length=255)
    maintenance_date = models.DateField()
    maintenance_cost = models.DecimalField(max_digits=10, decimal_places=2)
