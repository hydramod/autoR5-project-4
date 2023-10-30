"""
Imports necessary modules and classes for the 'autoR5' app forms.

- `forms` is imported from Django for form handling.
- `RegexValidator` is imported from Django core validators
    for regex validation.
- `FormHelper`, `Layout`, `Field`, and `Div` are imported from
    Crispy Forms for form layout.
- `DatePickerInput` is imported from the bootstrap_datepicker_plus
    library for date input.
- `SignupForm` is imported from allauth.account.forms for user
    registration.
- `.models` imports data models from the same directory.

These imports are used for defining and configuring forms in the
'autoR5' app.
"""
from django import forms
from django.core.validators import RegexValidator
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Div
from bootstrap_datepicker_plus.widgets import DatePickerInput
from allauth.account.forms import SignupForm
from .models import Booking, Review, CancellationRequest, UserProfile


class CustomSignupForm(SignupForm):
    """
    Custom user registration form extending 'SignupForm' from
    allauth.account.forms.

    This form adds the 'phone_number' field to the user
    registration form and ensures that it is required. When the
    form is saved, it also saves the 'phone_number' to
    the user's profile.

    Attributes:
        phone_number (forms.CharField): A field for the user's
        phone number.

    Methods:
        __init__(self, *args, **kwargs): Initializes the form and
        sets the 'phone_number' field as required.
        save(self, request): Saves the user registration data and
        the 'phone_number' to the user's profile.

    Parameters:
        *args: Additional positional arguments.
        **kwargs: Additional keyword arguments.

    Returns:
        user (User): The user object created or updated during registration.

    """
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


class BookingForm(forms.ModelForm):
    """
    BookingForm for booking a car.

    This form is used to capture booking information, including the
    rental date and return date. It ensures that the return date is
    after the rental date.

    Attributes:
        - Meta: Specifies the model and fields for the form.
        - clean(self): Custom form validation to ensure the return date
        is after the rental date.

    Returns:
        None
    """
    class Meta:
        """
        Inner class and method for custom validation in the BookingForm.

        The 'Meta' inner class defines the model and fields used in the
        form, as well as specifying widget options for date fields.

        The 'clean' method performs custom form validation to ensure that
        the return date is after the rental date. If the validation condition
        is not met, it raises a 'ValidationError' with an appropriate error
        message.

        Attributes:
            - Meta: Specifies the model, fields, and widgets for the form.
            - clean(self): Custom form validation to check the date
            relationship.

        Returns:
            None
        """
        model = Booking
        fields = ['rental_date', 'return_date']
        widgets = {
            'rental_date': DatePickerInput(),
            'return_date': DatePickerInput(),
        }

        def clean(self):
            """
            Custom form validation to ensure that the return date is
            after the rental date.

            This method is called during form validation to check the
            relationship between the rental date and the return date.
            It raises a 'ValidationError' if the rental date is greater
            than or equal to the return date, indicating that the return
            date must be after the rental date.

            Returns:
                None

            Raises:
                ValidationError: If the return date is not after the rental
                date, a 'ValidationError' is raised with an appropriate
                error message.
            """
            cleaned_data = super().clean()
            rental_date = cleaned_data.get("rental_date")
            return_date = cleaned_data.get("return_date")

            if rental_date and return_date and rental_date >= return_date:
                raise forms.ValidationError(
                    "Return date must be after the rental date.")


class ReviewForm(forms.ModelForm):
    """
    ReviewForm for submitting reviews.

    This form is used to capture user reviews, including the
    rating and comments about a car.

    Attributes:
        - Meta: Specifies the model and fields for the form.

    Returns:
        None
    """
    class Meta:
        """
        Inner class for defining the model and fields in ReviewForm.

        The 'Meta' inner class specifies the model and fields used in
        the 'ReviewForm' to determine which fields are displayed and
        captured in the form.

        Attributes:
            - model: The model associated with the form, which is 'Review'
            in this case.
            - fields: A list of fields to include in the form, which consists
            of 'rating' and 'comment' for capturing user reviews.

        Returns:
            None
        """
        model = Review
        fields = ['rating', 'comment']


class ContactForm(forms.Form):
    """
    ContactForm for user inquiries.

    This form is used to capture user inquiries, including their
    first name, last name, email, subject, and message.

    Attributes:
        - first_name: A field for capturing the user's first name.
        - last_name: A field for capturing the user's last name.
        - email: A field for capturing the user's email address.
        - subject: A field for specifying the subject of the inquiry.
        - message: A text area for composing the message.

    Returns:
        None
    """
    first_name = forms.CharField(label='First Name', max_length=100)
    last_name = forms.CharField(label='Last Name', max_length=100)
    email = forms.EmailField(label='Email')
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(
        label='Message',
        widget=forms.Textarea(attrs={'rows': 5, 'cols': 40}),
    )


class CancellationRequestForm(forms.ModelForm):
    """
    CancellationRequestForm for submitting cancellation requests.

    This form is used to capture user cancellation requests, including
    the reason for cancellation.

    Attributes:
        - reason: A text area for specifying the reason for the
        cancellation. This field is required and includes additional
        attributes such as 'rows' and 'cols' for customizing its
        appearance.

    Returns:
        None
    """
    reason = forms.CharField(
        widget=forms.Textarea(
            attrs={'rows': 4,
                   'cols': 40,
                   'required': True,
                   'id': 'unique_reason_id'}),
    )

    class Meta:
        """
        Inner class for defining the model and fields in
        CancellationRequestForm.

        The 'Meta' inner class specifies the model and fields used in the
        'CancellationRequestForm' to determine which fields are
        displayed and captured in the form. In this case, it defines
        the 'CancellationRequest' model and includes the 'reason' field.

        Attributes:
            - model: The model associated with the form, which is
            'CancellationRequest.'
            - fields: A list of fields to include in the form, containing
            only the
            'reason' field for specifying the cancellation reason.

        Returns:
            None
        """
        model = CancellationRequest
        fields = ['reason']


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.

    The 'UserProfileForm' is used for capturing and updating
    user profile information, including the user's phone number,
    profile picture, and the option to clear the profile picture.

    Attributes:
        - phone_number_validator: A regular expression validator
        for the phone number, ensuring it is 9 to 10 digits long.
        - phone_number: A field for entering the user's phone number,
        with validation based on the 'phone_number_validator.'
        - profile_picture_upload: A field for uploading a user's
        profile picture.
        - clear_picture: A checkbox field that allows the user to clear
        their profile picture.

        - Meta: The 'Meta' inner class specifies the model and fields
        used in the form, which includes the 'UserProfile' model and the
        'phone_number' and 'profile_picture' fields.

        - __init__(): The constructor method sets up the form's helper
        and layout, defining the structure of form fields and their appearance.

    Returns:
        None
    """
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
        """
        The 'Meta' inner class for the 'UserProfileForm' class.

        This 'Meta' class provides metadata for the 'UserProfileForm,'
        specifying the model and fields used in the form.

        Attributes:
            - model: The model associated with the form, which is
            'UserProfile' in this case, representing user profile
            information.
            - fields: A list of fields that are included in the form.
            In this instance, it includes 'phone_number' and 'profile_picture,'
            allowing users to update their phone number and profile picture in
            their user profile.

        Returns:
            """
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


class CsvImportForm(forms.Form):
    """
    A form class for importing data from a CSV file.

    This form is used to allow users to upload a CSV file for data import.

    Attributes:
        - csv_import: A FileField for selecting and uploading a CSV file.

    Usage:
        To use this form, instantiate it in a view and provide it to a
        template for user input.

    Returns:
        None
    """
    csv_import = forms.FileField(label='Select CSV File')
