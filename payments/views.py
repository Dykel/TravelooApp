from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Payment, Invoice, Refund
from bookings.models import Booking
import hmac
import hashlib
import json
import uuid
from datetime import datetime, timedelta
from twilio.rest import Client

@login_required
def payment_create(request, booking_id):
    """Initialize a new payment for a booking."""
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    
    if booking.status != 'pending':
        messages.error(request, 'This booking cannot be paid for.')
        return redirect('bookings:detail', booking_id=booking.id)
    
    # Generate unique transaction ID
    transaction_id = f"TXN-{uuid.uuid4().hex[:8].upper()}"
    
    # Create payment record
    payment = Payment.objects.create(
        booking=booking,
        amount=booking.total_amount,
        payment_method='mcb_juice',
        status='pending',
        transaction_id=transaction_id
    )
    
    # MCB Juice payment initialization
    merchant_id = settings.MCB_JUICE_MERCHANT_ID
    api_key = settings.MCB_JUICE_API_KEY
    
    # Create payment data
    payment_data = {
        'merchantId': merchant_id,
        'orderId': transaction_id,
        'amount': str(booking.total_amount),
        'currency': 'MUR',
        'description': f'Scooter rental booking {booking.booking_reference}',
        'customerEmail': request.user.email,
        'customerMobile': request.user.phone_number,
        'returnUrl': request.build_absolute_uri(f'/payments/callback/{transaction_id}/'),
    }
    
    # Generate signature
    signature_string = f"{merchant_id}|{transaction_id}|{payment_data['amount']}|MUR"
    signature = hmac.new(
        api_key.encode(),
        signature_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    payment_data['signature'] = signature
    
    return render(request, 'payments/create.html', {
        'booking': booking,
        'payment': payment,
        'payment_data': payment_data,
        'mcb_juice_url': settings.MCB_JUICE_API_URL
    })

@csrf_exempt
@require_POST
def payment_callback(request, transaction_id):
    """Handle MCB Juice payment callback."""
    try:
        data = json.loads(request.body)
        payment = get_object_or_404(Payment, transaction_id=transaction_id)
        
        # Verify signature
        merchant_id = settings.MCB_JUICE_MERCHANT_ID
        api_key = settings.MCB_JUICE_API_KEY
        signature_string = f"{merchant_id}|{transaction_id}|{data['amount']}|{data['status']}"
        expected_signature = hmac.new(
            api_key.encode(),
            signature_string.encode(),
            hashlib.sha256
        ).hexdigest()
        
        if not hmac.compare_digest(data['signature'], expected_signature):
            return HttpResponseBadRequest('Invalid signature')
        
        with transaction.atomic():
            if data['status'] == 'SUCCESS':
                payment.status = 'completed'
                payment.save()
                
                # Update booking status
                booking = payment.booking
                booking.status = 'confirmed'
                booking.save()
                
                # Update invoice status
                invoice = booking.invoice
                invoice.status = 'paid'
                invoice.save()
                
                # Send WhatsApp notification
                if hasattr(settings, 'TWILIO_ACCOUNT_SID') and settings.TWILIO_ACCOUNT_SID:
                    try:
                        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
                        message = client.messages.create(
                            from_=f'whatsapp:{settings.WHATSAPP_PHONE_NUMBER}',
                            body=f'Payment received for booking {booking.booking_reference}! Your scooter rental is confirmed.',
                            to=f'whatsapp:{booking.user.phone_number}'
                        )
                    except Exception as e:
                        print(f"WhatsApp notification failed: {e}")
            else:
                payment.status = 'failed'
                payment.save()
        
        return JsonResponse({'status': 'success'})
        
    except (json.JSONDecodeError, KeyError):
        return HttpResponseBadRequest('Invalid request')

@login_required
def payment_history(request):
    """View payment history."""
    payments = Payment.objects.filter(
        booking__user=request.user
    ).order_by('-payment_date')
    
    return render(request, 'payments/history.html', {'payments': payments})

@login_required
def refund_request(request, payment_id):
    """Request a refund for a payment."""
    payment = get_object_or_404(Payment, id=payment_id, booking__user=request.user)
    
    if request.method == 'POST':
        reason = request.POST.get('reason')
        if not reason:
            messages.error(request, 'Please provide a reason for the refund.')
            return redirect('payments:refund_request', payment_id=payment.id)
        
        # Create refund record
        refund = Refund.objects.create(
            payment=payment,
            amount=payment.amount,
            reason=reason,
            refund_transaction_id=f"REF-{uuid.uuid4().hex[:8].upper()}",
            status='pending'
        )
        
        messages.success(request, 'Refund request submitted successfully.')
        return redirect('payments:history')
    
    return render(request, 'payments/refund_request.html', {'payment': payment})
