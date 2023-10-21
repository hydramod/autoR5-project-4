from django import forms
from .models import Booking, Review, CancellationRequest, UserProfile
from bootstrap_datepicker_plus.widgets import DatePickerInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout

# BookingForm for booking a car
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

# ReviewForm for submitting a car review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

# ContactForm for contacting support
class ContactForm(forms.Form):
    first_name = forms.CharField(label='FIRST NAME', max_length=100)
    last_name = forms.CharField(label='LAST NAME', max_length=100)
    email = forms.EmailField(label='EMAIL')
    subject = forms.CharField(label='SUBJECT', max_length=100)
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),
    )

# CancellationRequestForm for canceling a booking
class CancellationRequestForm(forms.ModelForm):
    class Meta:
        model = CancellationRequest
        fields = ['reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'required': True}),
        }

# UserProfileForm for updating user profile information
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture']

# CsvImportForm for importing data from a CSV file
class CsvImportForm(forms.Form):
    csv_import = forms.FileField(label='Select CSV File')
