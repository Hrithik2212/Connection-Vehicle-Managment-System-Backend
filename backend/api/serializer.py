from rest_framework import serializers
from .models import User 
from .models import Vehicle, Trip, Sensor, Maintenance, Owner


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'name']


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'name', 'contact_info']


class VehicleSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)

    class Meta:
        model = Vehicle
        fields = ['id', 'make', 'model', 'year', 'fuel_type', 'owner_name']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ['id', 'vehicle', 'start_time', 'end_time', 'start_location', 'end_location', 'distance_traveled']

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'vehicle', 'sensor_reading', 'timestamp']

class MaintenanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Maintenance
        fields = ['id', 'vehicle', 'maintenance_type', 'maintenance_date', 'maintenance_cost']
