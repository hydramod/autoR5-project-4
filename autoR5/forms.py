from django import forms
from .models import Booking, Review
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout
from bootstrap_datepicker_plus.widgets import DatePickerInput

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['rental_date', 'return_date']
        widgets = {
            'rental_date': DatePickerInput(), 
            'return_date': DatePickerInput(), 
        }

    def clean(self):
        cleaned_data = super().clean()
        rental_date = cleaned_data.get("rental_date")
        return_date = cleaned_data.get("return_date")

        if rental_date and return_date and rental_date >= return_date:
            raise forms.ValidationError("Return date must be after the rental date.")

class ReviewForm(forms.Form):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

from django import forms

class ContactForm(forms.Form):
    first_name = forms.CharField(label='FIRST NAME', max_length=100)
    last_name = forms.CharField(label='LAST NAME', max_length=100)
    email = forms.EmailField(label='EMAIL')
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),
    )

