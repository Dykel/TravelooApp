from django.db import models
from scooters.models import Scooter

class GPSTracker(models.Model):
    scooter = models.OneToOneField(Scooter, on_delete=models.CASCADE, related_name='gps_tracker')
    device_id = models.CharField(max_length=100, unique=True)
    last_seen = models.DateTimeField(null=True, blank=True)
    battery_level = models.IntegerField(default=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Tracker for {self.scooter.name}"

class LocationHistory(models.Model):
    tracker = models.ForeignKey(GPSTracker, on_delete=models.CASCADE, related_name='location_history')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    speed = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    heading = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    accuracy = models.DecimalField(max_digits=5, decimal_places=2, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name_plural = 'Location histories'

class GeofenceZone(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    center_latitude = models.DecimalField(max_digits=9, decimal_places=6)
    center_longitude = models.DecimalField(max_digits=9, decimal_places=6)
    radius = models.DecimalField(max_digits=10, decimal_places=2)  # in meters
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class GeofenceAlert(models.Model):
    ALERT_TYPES = [
        ('enter', 'Enter'),
        ('exit', 'Exit'),
        ('dwell', 'Dwell'),
    ]

    zone = models.ForeignKey(GeofenceZone, on_delete=models.CASCADE, related_name='alerts')
    tracker = models.ForeignKey(GPSTracker, on_delete=models.CASCADE, related_name='geofence_alerts')
    alert_type = models.CharField(max_length=10, choices=ALERT_TYPES)
    timestamp = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
