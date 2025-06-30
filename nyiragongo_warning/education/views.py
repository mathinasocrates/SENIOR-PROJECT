from django.shortcuts import render
from .models import EducationalResource, TrainingSession

def resources(request):
    resources = EducationalResource.objects.all()
    featured = resources.filter(is_featured=True)
    return render(request, 'education/resources.html', {
        'resources': resources,
        'featured': featured
    })

def training(request):
    upcoming_sessions = TrainingSession.objects.filter(
        is_active=True,
        date__gte=timezone.now()
    ).order_by('date')
    return render(request, 'education/training.html', {
        'sessions': upcoming_sessions
    })
