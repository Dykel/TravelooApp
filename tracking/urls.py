from django.urls import path
from . import views

app_name = 'tracking'

urlpatterns = [
    path('dashboard/', views.tracking_dashboard, name='dashboard'),
    path('scooter/<int:scooter_id>/location/', views.scooter_location, name='scooter_location'),
    path('update-location/', views.update_location, name='update_location'),
    path('geofences/', views.manage_geofences, name='manage_geofences'),
]
