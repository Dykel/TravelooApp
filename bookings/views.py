from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.conf import settings
from .models import Booking, Contract
from .forms import BookingForm
from scooters.models import Scooter
from payments.models import Invoice
import uuid
from datetime import datetime, timedelta
from twilio.rest import Client

@login_required
def booking_create(request, scooter_id):
    """Create a new booking."""
    scooter = get_object_or_404(Scooter, id=scooter_id)
    
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Check if scooter is available
            conflicting_bookings = Booking.objects.filter(
                scooter=scooter,
                start_date__lt=end_date,
                end_date__gt=start_date,
                status__in=['confirmed', 'active']
            )
            
            if conflicting_bookings.exists():
                messages.error(request, 'Scooter is not available for the selected dates.')
                return redirect('scooters:detail', scooter_id=scooter.id)
            
            with transaction.atomic():
                # Create booking
                booking = form.save(commit=False)
                booking.user = request.user
                booking.scooter = scooter
                booking.booking_reference = str(uuid.uuid4())[:8].upper()
                
                # Calculate total amount
                duration = end_date - start_date
                days = duration.days
                hours = duration.seconds // 3600
                
                if days > 0:
                    total_amount = days * scooter.daily_rate
                    if hours > 0:
                        total_amount += scooter.daily_rate
                else:
                    total_amount = max(1, hours) * scooter.hourly_rate
                
                booking.total_amount = total_amount
                booking.save()
                
                # Create contract
                contract = Contract.objects.create(
                    booking=booking,
                    contract_file=f'contracts/{booking.booking_reference}.pdf'
                )
                
                # Create invoice
                invoice = Invoice.objects.create(
                    booking=booking,
                    invoice_number=f'INV-{booking.booking_reference}',
                    amount=total_amount,
                    tax_amount=total_amount * 0.15,  # 15% VAT
                    total_amount=total_amount * 1.15,
                    due_date=timezone.now() + timedelta(days=1)
                )
                
                # Send WhatsApp notification if configured
                if hasattr(settings, 'TWILIO_ACCOUNT_SID') and settings.TWILIO_ACCOUNT_SID:
                    try:
                        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        message = client.messages.create(
                            from_=f'whatsapp:{settings.WHATSAPP_PHONE_NUMBER}',
                            body=f'Your booking {booking.booking_reference} has been confirmed! Total amount: ${booking.total_amount}',
                            to=f'whatsapp:{request.user.phone_number}'
                        )
                    except Exception as e:
                        print(f"WhatsApp notification failed: {e}")
                
                messages.success(request, 'Booking created successfully!')
                return redirect('bookings:detail', booking_id=booking.id)
    else:
        initial = {}
        if 'start_date' in request.GET:
            initial['start_date'] = request.GET['start_date']
        if 'end_date' in request.GET:
            initial['end_date'] = request.GET['end_date']
        form = BookingForm(initial=initial)
    
    return render(request, 'bookings/create.html', {
        'form': form,
        'scooter': scooter
    })

@login_required
def booking_detail(request, booking_id):
    """View booking details."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    return render(request, 'bookings/detail.html', {'booking': booking})

@login_required
def my_bookings(request):
    """List user's bookings."""
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'bookings/list.html', {'bookings': bookings})

@login_required
def booking_cancel(request, booking_id):
    """Cancel a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status not in ['pending', 'confirmed']:
        messages.error(request, 'This booking cannot be cancelled.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
        
        # Send WhatsApp notification
        if hasattr(settings, 'TWILIO_ACCOUNT_SID') and settings.TWILIO_ACCOUNT_SID:
            try:
                client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                message = client.messages.create(
                    from_=f'whatsapp:{settings.WHATSAPP_PHONE_NUMBER}',
                    body=f'Your booking {booking.booking_reference} has been cancelled.',
                    to=f'whatsapp:{request.user.phone_number}'
                )
            except Exception as e:
                print(f"WhatsApp notification failed: {e}")
        
        messages.success(request, 'Booking cancelled successfully.')
        return redirect('bookings:my_bookings')
    
    return render(request, 'bookings/cancel.html', {'booking': booking})
