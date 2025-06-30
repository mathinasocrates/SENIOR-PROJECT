from django.db import models

class EducationalResource(models.Model):
    RESOURCE_TYPES = [
        ('guide', 'Safety Guide'),
        ('video', 'Educational Video'),
        ('infographic', 'Infographic'),
        ('drill', 'Emergency Drill'),
    ]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    content = models.TextField(blank=True)
    file_upload = models.FileField(upload_to='education/', null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

class TrainingSession(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    capacity = models.IntegerField()
    registered_count = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.title} - {self.date}"