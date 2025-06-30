from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('api/latest/', views.api_latest_data, name='api_latest_data'),
    path('api/sensor-data/', views.receive_sensor_data, name='receive_sensor_data'),
]
