from django import forms
from .models import Scooter, MaintenanceRecord

class ScooterSearchForm(forms.Form):
    start_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )
    end_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        required=False
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("End date must be after start date")

        return cleaned_data

class ScooterForm(forms.ModelForm):
    class Meta:
        model = Scooter
        fields = [
            'name', 'model', 'year', 'license_plate',
            'hourly_rate', 'daily_rate', 'description',
            'image', 'airtag_id'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'image': forms.FileInput(attrs={'accept': 'image/*'})
        }

class MaintenanceRecordForm(forms.ModelForm):
    under_maintenance = forms.BooleanField(
        required=False,
        help_text="Check this if the scooter should be marked as under maintenance"
    )

    class Meta:
        model = MaintenanceRecord
        fields = ['date', 'description', 'cost', 'performed_by', 'next_maintenance_date']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'next_maintenance_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }
