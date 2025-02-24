from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Scooter, MaintenanceRecord
from .forms import ScooterSearchForm, MaintenanceRecordForm
from bookings.models import Booking
from datetime import datetime, timedelta

def home(request):
    """Homepage view showing available scooters and search functionality."""
    search_form = ScooterSearchForm(request.GET)
    scooters = Scooter.objects.filter(status='available')

    if search_form.is_valid():
        if search_form.cleaned_data.get('start_date'):
            start_date = search_form.cleaned_data['start_date']
            end_date = search_form.cleaned_data['end_date']
            
            # Exclude scooters that are booked during the selected period
            booked_scooters = Booking.objects.filter(
                Q(start_date__lte=end_date) & Q(end_date__gte=start_date),
                status__in=['confirmed', 'active']
            ).values_list('scooter_id', flat=True)
            
            scooters = scooters.exclude(id__in=booked_scooters)

    paginator = Paginator(scooters, 9)  # Show 9 scooters per page
    page = request.GET.get('page')
    scooters = paginator.get_page(page)

    return render(request, 'scooters/home.html', {
        'scooters': scooters,
        'search_form': search_form
    })

def scooter_detail(request, scooter_id):
    """Detailed view of a specific scooter."""
    scooter = get_object_or_404(Scooter, id=scooter_id)
    maintenance_records = scooter.maintenance_records.all()[:5]
    
    # Get scooter availability for next 7 days
    today = datetime.now().date()
    availability = []
    for i in range(7):
        date = today + timedelta(days=i)
        bookings = Booking.objects.filter(
            scooter=scooter,
            start_date__date__lte=date,
            end_date__date__gte=date,
            status__in=['confirmed', 'active']
        )
        availability.append({
            'date': date,
            'available': not bookings.exists()
        })

    return render(request, 'scooters/detail.html', {
        'scooter': scooter,
        'maintenance_records': maintenance_records,
        'availability': availability
    })

@login_required
def maintenance_record_create(request, scooter_id):
    """Create a maintenance record for a scooter."""
    scooter = get_object_or_404(Scooter, id=scooter_id)
    
    if request.method == 'POST':
        form = MaintenanceRecordForm(request.POST)
        if form.is_valid():
            maintenance_record = form.save(commit=False)
            maintenance_record.scooter = scooter
            maintenance_record.save()
            
            # Update scooter status if under maintenance
            if form.cleaned_data.get('under_maintenance'):
                scooter.status = 'maintenance'
                scooter.save()
            
            messages.success(request, 'Maintenance record created successfully.')
            return redirect('scooter_detail', scooter_id=scooter.id)
    else:
        form = MaintenanceRecordForm()

    return render(request, 'scooters/maintenance_form.html', {
        'form': form,
        'scooter': scooter
    })

def scooter_location(request, scooter_id):
    """View current location of a scooter."""
    scooter = get_object_or_404(Scooter, id=scooter_id)
    latest_location = scooter.locations.first()  # Get most recent location

    return render(request, 'scooters/location.html', {
        'scooter': scooter,
        'location': latest_location
    })
