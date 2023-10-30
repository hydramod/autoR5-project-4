"""
This module defines the Django models
and imports necessary for the AutoR5 project.

It includes the following imports and models:

- `Decimal` from the `decimal` module for
    precise decimal arithmetic.
- `User` model from `django.contrib.auth.models`
    for user authentication and management.
- `MinValueValidator` and `MaxValueValidator`
    from `django.core.validators` for value validation.
- `models` from `django.db` for defining custom
    models in the project.
- `reverse` from `django.urls` for generating URLs
    based on view names.
- `timezone` from `django.utils` for working with
    time and time zones.
- `CloudinaryField` from `cloudinary.models`
    for integrating Cloudinary image storage.

These elements are used to create and manage models for the AutoR5 project.
"""

from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from django.utils import timezone
from cloudinary.models import CloudinaryField


class Car(models.Model):
    """
    Represents a car available for rent in the system.

    Attributes:
        make (str): The make or manufacturer of the car (e.g., 'Toyota').
        model (str): The model name of the car (e.g., 'Camry').
        year (int): The manufacturing year of the car (e.g., 2023).
        license_plate (str): The unique license plate of the car.
        daily_rate (Decimal): The daily rental rate of the car.
        is_available (bool): A flag indicating whether
        the car is available for rent.
        latitude (Decimal): The latitude coordinate of the car's location.
        longitude (Decimal): The longitude coordinate of the car's location.
        location_city (str, optional): The city where
        the car is located.
        location_address (str, optional): The specific
        address of the car's location.
        image (CloudinaryField, optional): An image of the car.
        features (str, optional): Description of the
        car's features and specifications.
        car_type (str, optional): The type or category of the car
        (e.g., 'SUV').
        fuel_type (str, optional): The type of fuel the car uses
        (e.g., 'Petrol').

    Methods:
        __str__(): Returns a human-readable string
        representing the car.
        get_absolute_url(): Returns the URL for accessing the car's details.

    Note:
        The `car_type` and `fuel_type` attributes are optional and
        should be selected
        from predefined choices (CAR_TYPES and FUEL_TYPES) using
        the specified format.
    """
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=30, unique=True)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=53.349805)
    longitude = models.DecimalField(
        max_digits=9, decimal_places=6, default=-6.26031)
    location_city = models.CharField(blank=True, null=True, max_length=255)
    location_address = models.CharField(blank=True, null=True, max_length=255)
    image = CloudinaryField("car_images", blank=True, null=True)
    features = models.TextField(blank=True, null=True, max_length=1000)

    CAR_TYPES = [
        ("Hatchback", "Hatchback"),
        ("Saloon", "Saloon"),
        ("Estate", "Estate"),
        ("MPV", "MPV"),
        ("SUV", "SUV"),
        ("Sports_Car", "Sports_Car"),
    ]
    FUEL_TYPES = [
        ("Petrol", "Petrol"),
        ("Diesel", "Diesel"),
        ("Hybrid", "Hybrid"),
        ("Electric", "Electric"),
    ]
    car_type = models.CharField(
        max_length=20, choices=CAR_TYPES, blank=True, null=True)
    fuel_type = models.CharField(
        max_length=20, choices=FUEL_TYPES, blank=True, null=True
    )

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    def get_absolute_url(self):
        """
        Returns the URL for accessing the detailed information page of the car.

        Returns:
            str: The URL for the car's detail page, including the
            car's unique ID.
        """
        return reverse("car_detail", args=[str(self.id)])


class Booking(models.Model):
    """
    This model defines bookings made by users for renting cars
    in the AutoR5 project.

    It includes the following fields and methods:

    Fields:
    - `user`: A foreign key to the `User` model, representing the
    user making the booking.

    - `car`: A foreign key to the `Car` model, representing the rented car.

    - `rental_date`: A date and time when the rental period starts.

    - `return_date`: A date and time when the rental period ends
    (can be blank if the booking is pending).

    - `total_cost`: The total cost of the booking,
    calculated based on the rental period and car's daily rate.

    - `status`: A choice field for booking status, which can be
    'Pending,' 'Confirmed,' 'Completed,' or 'Canceled'.

    Methods:
    - `__str__`: Returns a string representation of the booking in the format
    "Booking for {car} by {user}".

    - `calculate_total_cost`: Calculates the total cost of
    the booking based on the rental period and car's daily rate.

    - `save`: Overrides the default `save` method to automatically
    update the booking and car availability status when the
    booking is complete and calculate the total cost before saving.

    This model represents user bookings in the AutoR5 project.
    """
    BOOKING_STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Canceled", "Canceled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rental_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=BOOKING_STATUS_CHOICES, default="Pending"
    )

    def __str__(self):
        return f"Booking for {self.car} by {self.user}"

    def calculate_total_cost(self):
        """
        Calculate the total cost of the booking based on the rental
        period and car's daily rate.

        This method calculates the total cost of the booking by taking
        into account the rental period and the daily rate of the rented car.

        If the `return_date` is specified:
        - It calculates the number of days between the `rental_date` and
        `return_date` and ensures it's at least 1 day.

        - It converts the car's daily rate to a Decimal and multiplies
        it by the rental period to determine the total cost.

        If `return_date` is not specified (i.e., the booking is pending):
        - The total cost is set to Decimal('0.00').

        The calculated total cost is stored in the `total_cost` field of
        the booking.

        Parameters:
        - None

        Returns:
        - None

        Usage:
        - Call this method on a Booking instance to calculate the total cost.
        """
        if self.return_date:
            rental_period = (self.return_date - self.rental_date).days
            if rental_period < 1:
                rental_period = 1
            car_daily_rate = Decimal(str(self.car.daily_rate))
            self.total_cost = car_daily_rate * Decimal(rental_period)
        else:
            self.total_cost = Decimal("0.00")

    def save(self, *args, **kwargs):
        if (
            self.status == "Confirmed"
            and self.return_date
            and self.return_date < timezone.now()
        ):
            self.status = "Completed"
            self.car.is_available = True
        self.calculate_total_cost()
        super().save(*args, **kwargs)


class Payment(models.Model):
    """
    Represents a payment made for a booking.

    This model stores information about a payment made by a user for
    a specific booking.It includes details such as the user who made
    the payment, the booking it corresponds to, the payment amount,
    payment date, payment method, and payment status.

    Payment Status Choices:
    - 'Pending': The payment is pending and has not been processed.
    - 'Paid': The payment has been successfully processed.
    - 'Failed': The payment processing has failed.
    - 'Refunded': The payment has been refunded.
    - 'Canceled': The payment has been canceled.

    Fields:
    - user (ForeignKey): The user who made the payment.

    - booking (ForeignKey): The booking for which the payment was made.

    - amount (DecimalField): The total amount of the payment.

    - payment_date (DateTimeField): The date and time when the payment
    was made (auto-generated).

    - payment_method (CharField): The method used for the payment.

    - payment_status (CharField): The status of the payment
    (default is 'Pending').

    - payment_intent (CharField, optional): A unique identifier for
    the payment, if available.

    Methods:
    - __str__: Returns a string representation of the payment.

    Usage:
    - Create instances of this model to record payments made for
    bookings.
    """
    PAYMENT_STATUS_CHOICES = (
        ("Pending", "Pending"),
        ("Paid", "Paid"),
        ("Failed", "Failed"),
        ("Refunded", "Refunded"),
        ("Canceled", "Canceled"),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey("Booking", on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default="Pending"
    )
    payment_intent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.amount} for Booking {self.booking}"


class CancellationRequest(models.Model):
    """
    Represents a user's request to cancel a booking.

    This model stores information about a cancellation request made
    by a user for a specific booking. It includes details such as the
    booking for which the cancellation is requested, the user making
    the request, the date and time of the request, the reason for
    the request, and whether the request has been approved.

    Fields:
    - booking (ForeignKey): The booking for which the cancellation
    is requested.

    - user (ForeignKey): The user making the cancellation request.

    - request_date (DateTimeField): The date and time when the
    cancellation request was created (auto-generated).

    - reason (TextField): The reason provided by the user for the
    cancellation request.

    - approved (BooleanField): Indicates whether the request has been
    approved (default is 'False').

    Methods:
    - __str__: Returns a string representation of the cancellation
    request.

    Usage:
    - Create instances of this model to record user requests to cancel
    bookings and track their status (approved or pending).
    """
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Cancellation request for {self.booking}"


class Review(models.Model):
    """
    Represents a user review for a specific car.

    This model stores information about user reviews for cars,
    including details such as the reviewed car,
    the user who wrote the review, the rating provided
    (between 1 and 5), the user's comments,
    and whether the review has been approved.

    Fields:
    - car (ForeignKey): The car for which the review is written.

    - user (ForeignKey): The user who wrote the review.

    - rating (PositiveIntegerField): The numeric rating given
    by the user (validated between 1 and 5).

    - comment (TextField): The user's comments or feedback about
    the car.

    - approved (BooleanField): Indicates whether the review has
    been approved (default is 'False').

    Methods:
    - __str__: Returns a string representation of the review.

    Usage:
    - Create instances of this model to collect and manage user
    reviews and ratings for cars.
    """
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for {self.car} by {self.user}"


class UserProfile(models.Model):
    """
    Represents user profile information associated with a Django
    User.

    This model extends the built-in Django User model to include
    additional user profile information, such as the user's phone
    number and profile picture.

    Fields:
    - user (OneToOneField): A reference to the associated Django
    User.

    - phone_number (CharField): The user's phone number
    (optional, blank and null are allowed).

    - profile_picture (CloudinaryField): The user's profile
    picture stored in Cloudinary
    (optional, blank and null are allowed).

    Properties:
    - email (property): Provides access to the email address of
    the associated User.

    Methods:
    - __str__: Returns a string representation of the user's
    profile.

    Usage:
    - Create instances of this model to associate additional

    information with a Django User, such as phone numbers or
    profile pictures.

    - Access the associated User's email through the 'email' property.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = CloudinaryField(
        "profile_pictures", blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def email(self):
        """
        Property to access the email address associated with the user.

        This property provides read-only access to the email address of the
        user associated with the UserProfile.

        Returns:
        str: The email address of the user.

        Usage:
        Access the email address of the user associated with the UserProfile
        using this property.
        For example:
        user_profile = UserProfile.objects.get(user=user)
        user_email = user_profile.email
        """

        return self.user.email


class ContactFormSubmission(models.Model):
    """
    Model to store contact form submissions.

    This model represents submissions made through a contact form on a
    website. It stores information about the submitter, including their
    first name, last name, email, subject, message, and the submission
    date.

    Attributes:
    - first_name (str): The first name of the submitter.
    - last_name (str): The last name of the submitter.
    - email (str): The email address of the submitter.
    - subject (str): The subject of the submission.
    - message (str): The message or content of the submission.
    - submission_date (datetime): The date and time when the submission
    was made.

    Methods:
    - __str__(): Returns a string representation of the submission in
    the format "First Name Last Name - Subject".

    Usage:
    You can create instances of this model to store contact form submissions
    made on your website.

    Example:
    submission = ContactFormSubmission(
        first_name="John",
        last_name="Doe",
        email="johndoe@example.com",
        subject="Question",
        message="I have a question about your services."
    )
    submission.save()
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    submission_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.subject}"
