from django import forms
from .models import Booking


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['visit_date', 'number_of_visitors', 'remarks', 'hotel']
        widgets = {
            'visit_date': forms.DateInput(attrs={'type': 'date'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, destination=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hotel'].required = False
        self.fields['hotel'].empty_label = "No hotel needed (visit only)"
        if destination:
            self.fields['hotel'].queryset = destination.hotels.filter(is_active=True)