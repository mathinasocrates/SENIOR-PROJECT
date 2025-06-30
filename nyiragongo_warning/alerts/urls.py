from django.urls import path
from . import views

urlpatterns = [
    path('', views.alerts_list, name='alerts_list'),
    path('subscribe/', views.subscribe, name='subscribe'),
]