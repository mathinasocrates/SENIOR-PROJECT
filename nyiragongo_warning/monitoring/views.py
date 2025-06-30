from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import VolcanicData, Station
import json

def dashboard(request):
    latest_data = VolcanicData.objects.first()
    stations = Station.objects.filter(is_active=True)
    recent_data = VolcanicData.objects.all()[:10]
    
    context = {
        'latest_data': latest_data,
        'stations': stations,
        'recent_data': recent_data,
    }
    return render(request, 'monitoring/dashboard.html', context)

def api_latest_data(request):
    latest = VolcanicData.objects.first()
    if latest:
        data = {
            'timestamp': latest.timestamp.isoformat(),
            'seismic_activity': latest.seismic_activity,
            'gas_emissions': latest.gas_emissions,
            'ground_deformation': latest.ground_deformation,
            'temperature': latest.temperature,
            'alert_level': latest.alert_level,
        }
        return JsonResponse(data)
    return JsonResponse({'error': 'No data available'})

@csrf_exempt
def receive_sensor_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            volcanic_data = VolcanicData.objects.create(
                seismic_activity=data.get('seismic_activity', 0),
                gas_emissions=data.get('gas_emissions', 0),
                ground_deformation=data.get('ground_deformation', 0),
                temperature=data.get('temperature', 0),
            )
            
            # Determine alert level based on thresholds
            alert_level = determine_alert_level(volcanic_data)
            volcanic_data.alert_level = alert_level
            volcanic_data.save()
            
            return JsonResponse({'status': 'success', 'alert_level': alert_level})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

def determine_alert_level(data):
    """Determine alert level based on sensor readings"""
    critical_count = 0
    warning_count = 0
    
    if data.seismic_activity > 5.0:
        critical_count += 1
    elif data.seismic_activity > 3.0:
        warning_count += 1
    
    if data.gas_emissions > 1000:
        critical_count += 1
    elif data.gas_emissions > 500:
        warning_count += 1
    
    if data.ground_deformation > 50:
        critical_count += 1
    elif data.ground_deformation > 25:
        warning_count += 1
    
    if data.temperature > 1200:
        critical_count += 1
    elif data.temperature > 1000:
        warning_count += 1
    
    if critical_count >= 2:
        return 'red'
    elif critical_count >= 1 or warning_count >= 3:
        return 'orange'
    elif warning_count >= 1:
        return 'yellow'
    else:
        return 'green'