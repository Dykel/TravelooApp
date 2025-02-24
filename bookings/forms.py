from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.ModelForm):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text='When would you like to pick up the scooter?'
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        help_text='When will you return the scooter?'
    )

    class Meta:
        model = Booking
        fields = ['start_date', 'end_date']

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date:
            # Check if start date is in the past
            if start_date < timezone.now():
                raise forms.ValidationError('Start date cannot be in the past.')

            # Check if end date is before start date
            if end_date <= start_date:
                raise forms.ValidationError('End date must be after start date.')

            # Check if booking duration is within allowed limits
            duration = end_date - start_date
            if duration.days > 30:
                raise forms.ValidationError('Maximum booking duration is 30 days.')

        return cleaned_data
