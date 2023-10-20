from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from cloudinary.models import CloudinaryField
from geopy.geocoders import Nominatim

# Car model for storing car information
class Car(models.Model):
    # Fields to store car details
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
    image = CloudinaryField('car_images', blank=True, null=True)
    features = models.TextField(blank=True, null=True, max_length=1000)

    # Choices for car types and fuel types
    CAR_TYPES = [
        ('Hatchback', 'Hatchback'),
        ('Saloon', 'Saloon'),
        ('Estate', 'Estate'),
        ('MPV', 'MPV'),
        ('SUV', 'SUV'),
        ('Sports car', 'Sports car'),
    ]
    FUEL_TYPES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Hybrid', 'Hybrid'),
        ('Electric', 'Electric'),
    ]
    car_type = models.CharField(
        max_length=20, choices=CAR_TYPES, blank=True, null=True)
    fuel_type = models.CharField(
        max_length=20, choices=FUEL_TYPES, blank=True, null=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    def get_absolute_url(self):
        return reverse('car_detail', args=[str(self.id)])


# Booking model for managing car bookings
class Booking(models.Model):
    # Choices for booking status
    BOOKING_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rental_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20, choices=BOOKING_STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Booking for {self.car} by {self.user}"

    def calculate_total_cost(self):
        # Calculate the total cost based on the rental period and car's daily rate
        if self.return_date:
            rental_period = (self.return_date - self.rental_date).days
            if rental_period < 1:
                rental_period = 1
            # Convert car.daily_rate to Decimal
            car_daily_rate = Decimal(str(self.car.daily_rate))
            self.total_cost = car_daily_rate * Decimal(rental_period)
        else:
            self.total_cost = Decimal('0.00')

    def save(self, *args, **kwargs):
        # Automatically update the booking status and car availability status when booking is complete
        if self.status == 'Confirmed' and self.return_date and self.return_date < timezone.now():
            self.status = 'Completed'
            self.car.is_available = True
        # Automatically calculate the total cost before saving
        self.calculate_total_cost()
        super().save(*args, **kwargs)

# Payment model for recording user payments
class Payment(models.Model):
    # Choices for payment status
    PAYMENT_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Refunded', 'Refunded')
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey('Booking', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(
        max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Pending')
    payment_intent = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Payment of {self.amount} for Booking {self.booking}"

# CancellationRequest model for recording booking cancellation requests
class CancellationRequest(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Cancellation request for {self.booking}"

# Review model for car reviews
class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review for {self.car} by {self.user}"

# UserProfile model for user profile information
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = CloudinaryField(
        'profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username

    @property
    def email(self):
        return self.user.email

# Notification model for user notifications
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
