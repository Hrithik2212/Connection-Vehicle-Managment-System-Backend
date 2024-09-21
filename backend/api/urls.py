from django.urls import path
from . import views

urlpatterns = [
    path('vehicles/<int:vehicle_id>/distance_traveled/', views.total_distance_traveled, name='total_distance_traveled'),
    path('vehicles/sensor_anomalies/', views.sensor_anomalies, name='sensor_anomalies'),
    path('vehicles/<int:vehicle_id>/maintenance_history/', views.maintenance_history, name='maintenance_history'),
    path('vehicles/frequent_trips/', views.frequent_trips, name='frequent_trips'),
    path('populate_database/', views.populate_database, name='populate_database'),
]
