from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
from .models import GPSTracker, LocationHistory, GeofenceZone, GeofenceAlert
from scooters.models import Scooter
from bookings.models import Booking
import json
from datetime import datetime, timedelta
from twilio.rest import Client

@login_required
def tracking_dashboard(request):
    """Display tracking dashboard for admin users."""
    if not request.user.is_staff:
        return redirect('home')
    
    trackers = GPSTracker.objects.select_related('scooter').all()
    geofence_zones = GeofenceZone.objects.all()
    
    # Get recent alerts
    recent_alerts = GeofenceAlert.objects.select_related(
        'zone', 'tracker', 'tracker__scooter'
    ).order_by('-timestamp')[:10]
    
    return render(request, 'tracking/dashboard.html', {
        'trackers': trackers,
        'geofence_zones': geofence_zones,
        'recent_alerts': recent_alerts
    })

@login_required
def scooter_location(request, scooter_id):
    """View location history for a specific scooter."""
    scooter = get_object_or_404(Scooter, id=scooter_id)
    
    # Check if user has permission to view this scooter's location
    if not request.user.is_staff:
        # Check if user has an active booking for this scooter
        has_booking = Booking.objects.filter(
            user=request.user,
            scooter=scooter,
            status='active'
        ).exists()
        if not has_booking:
            return redirect('home')
    
    # Get location history for the last 24 hours
    history = LocationHistory.objects.filter(
        tracker__scooter=scooter,
        timestamp__gte=datetime.now() - timedelta(days=1)
    ).order_by('timestamp')
    
    return render(request, 'tracking/location.html', {
        'scooter': scooter,
        'history': history
    })

@csrf_exempt
@require_POST
def update_location(request):
    """Update scooter location from GPS tracker."""
    try:
        data = json.loads(request.body)
        
        # Verify API key
        api_key = request.headers.get('X-API-Key')
        if api_key != settings.GPS_TRACKER_API_KEY:
            return JsonResponse({'error': 'Invalid API key'}, status=401)
        
        tracker = get_object_or_404(GPSTracker, device_id=data['device_id'])
        
        # Update tracker status
        tracker.last_seen = datetime.now()
        tracker.battery_level = data.get('battery_level', tracker.battery_level)
        tracker.save()
        
        # Create location history
        location = LocationHistory.objects.create(
            tracker=tracker,
            latitude=data['latitude'],
            longitude=data['longitude'],
            speed=data.get('speed'),
            heading=data.get('heading'),
            accuracy=data.get('accuracy')
        )
        
        # Check geofence violations
        geofences = GeofenceZone.objects.filter(is_active=True)
        for zone in geofences:
            # Simple circular geofence check
            from math import radians, sin, cos, sqrt, atan2
            
            R = 6371e3  # Earth's radius in meters
            lat1 = radians(float(zone.center_latitude))
            lon1 = radians(float(zone.center_longitude))
            lat2 = radians(float(location.latitude))
            lon2 = radians(float(location.longitude))
            
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
            c = 2 * atan2(sqrt(a), sqrt(1-a))
            distance = R * c
            
            if distance <= float(zone.radius):
                # Create geofence alert
                alert = GeofenceAlert.objects.create(
                    zone=zone,
                    tracker=tracker,
                    alert_type='enter'
                )
                
                # Send WhatsApp notification if configured
                if hasattr(settings, 'TWILIO_ACCOUNT_SID') and settings.TWILIO_ACCOUNT_SID:
                    try:
                        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        message = client.messages.create(
                            from_=f'whatsapp:{settings.WHATSAPP_PHONE_NUMBER}',
                            body=f'Alert: Scooter {tracker.scooter.name} has entered geofence zone {zone.name}',
                            to=f'whatsapp:{settings.ADMIN_PHONE_NUMBER}'
                        )
                    except Exception as e:
                        print(f"WhatsApp notification failed: {e}")
        
        return JsonResponse({'status': 'success'})
        
    except (json.JSONDecodeError, KeyError):
        return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def manage_geofences(request):
    """Manage geofence zones."""
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        center_latitude = request.POST.get('center_latitude')
        center_longitude = request.POST.get('center_longitude')
        radius = request.POST.get('radius')
        
        GeofenceZone.objects.create(
            name=name,
            description=description,
            center_latitude=center_latitude,
            center_longitude=center_longitude,
            radius=radius
        )
        
        return redirect('tracking:manage_geofences')
    
    zones = GeofenceZone.objects.all()
    return render(request, 'tracking/manage_geofences.html', {'zones': zones})
