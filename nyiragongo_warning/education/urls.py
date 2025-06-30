from django.urls import path
from . import views

urlpatterns = [
    path('', views.resources, name='education_resources'),
    path('training/', views.training, name='training_sessions'),
]
