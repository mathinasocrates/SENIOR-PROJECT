from celery import shared_task
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import VolcanicData
from alerts.models import Alert

@shared_task
def check_alert_conditions():
    """Check latest volcanic data and create alerts if necessary"""
    latest_data = VolcanicData.objects.first()
    if not latest_data:
        return
    
    if latest_data.alert_level in ['orange', 'red']:
        # Create alert if conditions are met
        alert_title = f"Volcanic Activity Alert - {latest_data.alert_level.upper()}"
        alert_message = f"Mount Nyiragongo showing elevated activity. Alert level: {latest_data.alert_level}"
        
        Alert.objects.create(
            title=alert_title,
            message=alert_message,
            alert_type='eruption' if latest_data.alert_level == 'red' else 'advisory',
            priority='critical' if latest_data.alert_level == 'red' else 'high'
        )
        
        # Send real-time update
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)('monitoring', {
            'type': 'send_volcanic_data',
            'data': {
                'alert_level': latest_data.alert_level,
                'message': alert_message
            }
        })

print("Django project structure created successfully!")
print("\nTo set up the project:")
print("1. Create a new Django project: django-admin startproject nyiragongo_warning")
print("2. Create apps: python manage.py startapp monitoring alerts education")
print("3. Install requirements: pip install -r requirements.txt")
print("4. Run migrations: python manage.py makemigrations && python manage.py migrate")
print("5. Create superuser: python manage.py createsuperuser")
print("6. Run server: python manage.py runserver")