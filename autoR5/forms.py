from django import forms
from .models import Booking, Review, CancellationRequest
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
            raise forms.ValidationError(
                "Return date must be after the rental date.")


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']


class ContactForm(forms.Form):
    first_name = forms.CharField(label='FIRST NAME', max_length=100)
    last_name = forms.CharField(label='LAST NAME', max_length=100)
    email = forms.EmailField(label='EMAIL')
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),
    )


class CancellationRequestForm(forms.ModelForm):
    class Meta:
        model = CancellationRequest
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'required': True}),
        }

class CsvImportForm(forms.Form):
    csv_import = forms.FileField(label='Select CSV File')