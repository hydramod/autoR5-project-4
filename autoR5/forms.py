from django import forms
from .models import Booking, Review, CancellationRequest, UserProfile
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from bootstrap_datepicker_plus.widgets import DatePickerInput
from allauth.account.forms import SignupForm
from django.core.validators import RegexValidator

# custom sign up form


class CustomSignupForm(SignupForm):
    phone_number = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Phone Number'}), required=True)

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        self.fields['phone_number'].required = True

    def save(self, request):
        # Save the phone number to the user's profile.
        user = super(CustomSignupForm, self).save(request)
        phone_number = self.cleaned_data.get('phone_number')
        user.userprofile.phone_number = phone_number
        user.userprofile.save()
        return user


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
            raise forms.ValidationError(
                "Return date must be after the rental date.")

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
    phone_number_validator = RegexValidator(
        regex=r'^\d{9,10}$',
        message='Phone number must be 9 to 10 digits long.',
    )

    phone_number = forms.CharField(
        validators=[phone_number_validator],
        label='Phone Number',
        required=True,
    )

    profile_picture_upload = forms.ImageField(
        label='Profile Picture Upload',
        required=False,
    )

    clear_picture = forms.BooleanField(
        required=False,
        label='Clear Profile Picture',
    )

    class Meta:
        model = UserProfile
        fields = ['phone_number', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('phone_number', css_class='form-control'),
                    css_class='col-md-6'
                ),
                Div(
                    Field('profile_picture_upload'),
                    css_class='col-md-6'
                ),
                css_class='row'
            ),
            Field('clear_picture', css_class='form-check-input'),
        )

# CsvImportForm for importing data from a CSV file


class CsvImportForm(forms.Form):
    csv_import = forms.FileField(label='Select CSV File')
