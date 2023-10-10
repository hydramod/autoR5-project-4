from django import forms
from .models import Booking, Review
from bootstrap_datepicker_plus.widgets import DatePickerInput

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['rental_date', 'return_date']
        widgets = {
            'rental_date': DatePickerInput(format='%d-%m-%Y'), 
            'return_date': DatePickerInput(format='%d-%m-%Y'), 
        }

    def clean(self):
        cleaned_data = super().clean()
        rental_date = cleaned_data.get("rental_date")
        return_date = cleaned_data.get("return_date")

        if rental_date and return_date and rental_date >= return_date:
            raise forms.ValidationError("Return date must be after the rental date.")

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
