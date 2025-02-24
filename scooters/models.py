from django.db import models
from django.conf import settings

class Scooter(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('maintenance', 'Under Maintenance'),
        ('retired', 'Retired'),
    ]

    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='scooters/', null=True, blank=True)
    airtag_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.license_plate}"

    class Meta:
        ordering = ['name']

class ScooterLocation(models.Model):
    scooter = models.ForeignKey(Scooter, on_delete=models.CASCADE, related_name='locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    timestamp = models.DateTimeField(auto_now_add=True)
    battery_level = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['-timestamp']

class MaintenanceRecord(models.Model):
    scooter = models.ForeignKey(Scooter, on_delete=models.CASCADE, related_name='maintenance_records')
    date = models.DateField()
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    performed_by = models.CharField(max_length=100)
    next_maintenance_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['-date']
