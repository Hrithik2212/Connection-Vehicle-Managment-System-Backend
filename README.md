# Create Owner
@api_view(['POST'])
def create_owner(request):
    serializer = OwnerSerializer(data=request.data)
    if serializer.is_valid():
        owner = serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Create Vehicle
@api_view(['POST'])
def create_vehicle(request):
    serializer = VehicleSerializer(data=request.data)
    if serializer.is_valid():
        vehicle = serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Create Trip
@api_view(['POST'])
def create_trip(request):
    serializer = TripSerializer(data=request.data)
    if serializer.is_valid():
        trip = serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Create Sensor Reading
@api_view(['POST'])
def create_sensor(request):
    serializer = SensorSerializer(data=request.data)
    if serializer.is_valid():
        sensor = serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

# Create Maintenance Record
@api_view(['POST'])
def create_maintenance(request):
    serializer = MaintenanceSerializer(data=request.data)
    if serializer.is_valid():
        maintenance = serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)




# 1. Retrieve Total Distance Traveled by Each Vehicle in the Last 30 Days
# @api_view(['GET'])
# def total_distance_traveled(request):
#     vehicles = Vehicle.objects.all()
#     data = []
#     last_30_days = now() - timedelta(days=30)
    
#     for vehicle in vehicles:
#         total_distance = Trip.objects.filter(vehicle=vehicle, start_time__gte=last_30_days).aggregate(total=models.Sum('distance_traveled'))['total'] or 0
#         vehicle_data = VehicleSerializer(vehicle).data
#         vehicle_data['total_distance_traveled'] = total_distance
#         data.append(vehicle_data)
    
#     return Response(data)