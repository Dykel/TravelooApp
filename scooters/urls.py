from django.urls import path
from . import views

app_name = 'scooters'

urlpatterns = [
    path('', views.home, name='home'),
    path('scooter/<int:scooter_id>/', views.scooter_detail, name='detail'),
    path('scooter/<int:scooter_id>/maintenance/create/',
         views.maintenance_record_create, name='maintenance_create'),
    path('scooter/<int:scooter_id>/location/',
         views.scooter_location, name='location'),
]
