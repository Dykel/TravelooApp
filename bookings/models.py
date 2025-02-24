from django.db import models
from django.conf import settings
from scooters.models import Scooter

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    scooter = models.ForeignKey(Scooter, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    booking_reference = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.user.email}"

    class Meta:
        ordering = ['-created_at']

class Contract(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='contract')
    signed_by_customer = models.BooleanField(default=False)
    signed_date = models.DateTimeField(null=True, blank=True)
    contract_file = models.FileField(upload_to='contracts/')
    terms_accepted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Contract for {self.booking.booking_reference}"

class Insurance(models.Model):
    booking = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='insurance')
    policy_number = models.CharField(max_length=50)
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    provider = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Insurance for {self.booking.booking_reference}"
