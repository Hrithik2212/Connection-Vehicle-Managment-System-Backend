from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now, timedelta
from .models import Vehicle, Trip, Sensor, Maintenance , Owner
from .serializer import VehicleSerializer, TripSerializer, SensorSerializer, MaintenanceSerializer , OwnerSerializer
from django.db import models 
import random


@api_view(['GET'])
def total_distance_traveled(request, vehicle_id):
    try:
        # Get the vehicle with the specified vehicle_id
        vehicle = Vehicle.objects.get(id=vehicle_id)
    except Vehicle.DoesNotExist:
        return Response({'error': 'Vehicle not found'}, status=404)

    # Calculate the total distance traveled by this vehicle in the last 30 days
    last_30_days = now() - timedelta(days=30)
    total_distance = Trip.objects.filter(vehicle=vehicle, start_time__gte=last_30_days).aggregate(total=models.Sum('distance_traveled'))['total'] or 0

    # Serialize the vehicle data
    vehicle_data = VehicleSerializer(vehicle).data
    vehicle_data['total_distance_traveled'] = total_distance

    return Response(vehicle_data)

# 2. Detect Sensor Anomalies
@api_view(['GET'])
def sensor_anomalies(request):
    anomalies = Sensor.objects.filter(models.Q(sensor_reading__gt=120) | models.Q(sensor_reading__lt=10))
    data = []
    for anomaly in anomalies:
        vehicle_data = VehicleSerializer(anomaly.vehicle).data
        anomaly_data = {
            'vehicle': vehicle_data,
            'sensor_reading': anomaly.sensor_reading,
            'timestamp': anomaly.timestamp
        }
        data.append(anomaly_data)
    
    return Response(data)

# 3. Get Maintenance History
@api_view(['GET'])
def maintenance_history(request, vehicle_id):
    maintenance_records = Maintenance.objects.filter(vehicle_id=vehicle_id)
    serializer = MaintenanceSerializer(maintenance_records, many=True)
    return Response(serializer.data)

# 4. Find Vehicles with Frequent Trips
@api_view(['GET'])
def frequent_trips(request):
    last_7_days = now() - timedelta(days=7)
    data = []
    
    vehicles = Vehicle.objects.annotate(num_trips=models.Count('trip', filter=models.Q(trip__start_time__gte=last_7_days))).filter(num_trips__gt=5)
    
    for vehicle in vehicles:
        vehicle_data = VehicleSerializer(vehicle).data
        vehicle_data['num_trips'] = vehicle.num_trips
        data.append(vehicle_data)
    
    return Response(data)


@api_view(['POST'])
def populate_database(request):
    # Create Owners
    owner_names = ['Alice', 'Bob', 'Charlie', 'David', 'Eve']
    owners = []
    for name in owner_names:
        owner = Owner.objects.create(name=name, contact_info=f'{name.lower()}@example.com')
        owners.append(owner)

    # Create Vehicles
    vehicle_data = [
        {'make': 'Tesla', 'model': 'Model S', 'year': 2020, 'fuel_type': 'electric'},
        {'make': 'Toyota', 'model': 'Prius', 'year': 2018, 'fuel_type': 'hybrid'},
        {'make': 'Ford', 'model': 'F-150', 'year': 2019, 'fuel_type': 'gasoline'},
        {'make': 'Chevrolet', 'model': 'Bolt', 'year': 2021, 'fuel_type': 'electric'},
        {'make': 'BMW', 'model': 'i3', 'year': 2017, 'fuel_type': 'electric'},
    ]

    vehicles = []
    for i, data in enumerate(vehicle_data):
        vehicle = Vehicle.objects.create(
            make=data['make'],
            model=data['model'],
            year=data['year'],
            fuel_type=data['fuel_type'],
            owner=owners[i]
        )
        vehicles.append(vehicle)

    # Create Trips, Sensors, and Maintenance Records for Each Vehicle
    for vehicle in vehicles:
        # Create 10 Trips
        for _ in range(10):
            start_time = now() - timedelta(days=random.randint(1, 60))
            end_time = start_time + timedelta(hours=random.randint(1, 5))
            trip = Trip.objects.create(
                vehicle=vehicle,
                start_time=start_time,
                end_time=end_time,
                start_location='Location A',
                end_location='Location B',
                distance_traveled=round(random.uniform(50, 200), 2)
            )

            # Create Sensor Readings for Each Trip
            for _ in range(5):
                timestamp = start_time + timedelta(minutes=random.randint(1, 300))
                sensor_reading = round(random.uniform(0, 150), 2)  # Speed or fuel level
                Sensor.objects.create(
                    vehicle=vehicle,
                    sensor_reading=sensor_reading,
                    timestamp=timestamp
                )

        # Create 3 Maintenance Records
        for _ in range(3):
            maintenance_date = now() - timedelta(days=random.randint(30, 365))
            maintenance_type = random.choice(['Oil Change', 'Battery Replacement', 'Tire Rotation'])
            maintenance_cost = round(random.uniform(100, 1000), 2)
            Maintenance.objects.create(
                vehicle=vehicle,
                maintenance_type=maintenance_type,
                maintenance_date=maintenance_date.date(),
                maintenance_cost=maintenance_cost
            )

    return Response({'message': 'Database populated with sample data.'}, status=200)
