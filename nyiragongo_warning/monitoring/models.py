from django.db import models
from django.utils import timezone

class VolcanicData(models.Model):
    ALERT_LEVELS = [
        ('green', 'Green - Normal'),
        ('yellow', 'Yellow - Advisory'),
        ('orange', 'Orange - Watch'),
        ('red', 'Red - Warning'),
    ]
    
    timestamp = models.DateTimeField(default=timezone.now)
    seismic_activity = models.FloatField(help_text="Magnitude of seismic activity")
    gas_emissions = models.FloatField(help_text="SO2 levels in ppm")
    ground_deformation = models.FloatField(help_text="Ground movement in mm")
    temperature = models.FloatField(help_text="Crater temperature in Celsius")
    alert_level = models.CharField(max_length=10, choices=ALERT_LEVELS, default='green')
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"Data at {self.timestamp} - Alert: {self.alert_level}"

class Station(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name