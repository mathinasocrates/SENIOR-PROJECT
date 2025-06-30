from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Alert, Subscription
from monitoring.models import VolcanicData
import json

def alerts_list(request):
    active_alerts = Alert.objects.filter(is_active=True)
    return render(request, 'alerts/list.html', {'alerts': active_alerts})

def subscribe(request):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        email = request.POST.get('email')
        location = request.POST.get('location')
        
        subscription = Subscription.objects.create(
            phone_number=phone,
            email=email,
            location=location
        )
        
        return JsonResponse({'status': 'success', 'message': 'Subscription successful!'})
    
    return render(request, 'alerts/subscribe.html')