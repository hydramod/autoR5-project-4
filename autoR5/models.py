from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from cloudinary.models import CloudinaryField

class FuelType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class CarType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Car(models.Model):
    make = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    year = models.PositiveIntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    daily_rate = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, default=53.349805)  # Default to Dublin's latitude
    longitude = models.DecimalField(max_digits=9, decimal_places=6, default=-6.26031)  # Default to Dublin's longitude
    location_name = models.CharField(max_length=100)  # Field for location name
    image = CloudinaryField('car_images', blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    car_type = models.ForeignKey(CarType, on_delete=models.SET_NULL, blank=True, null=True)
    fuel_type = models.ForeignKey(FuelType, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.year} {self.make} {self.model}"

    def get_absolute_url(self):
        return reverse('car_detail', args=[str(self.id)])

    @property
    def location(self):
        return f"{self.latitude},{self.longitude}"

    @property
    def address(self):
        return self.location_name  # Return the location name as the address

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    rental_date = models.DateTimeField()
    return_date = models.DateTimeField(blank=True, null=True)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"Booking for {self.car} by {self.user}"

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

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = CloudinaryField('profile_pictures', blank=True, null=True)

    def __str__(self):
        return self.user.username

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    payment_status = models.CharField(max_length=20)

    def __str__(self):
        return f"Payment of {self.amount} for Booking {self.booking}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

class CancellationRequest(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    reason = models.TextField()

    def __str__(self):
        return f"Cancellation request for {self.booking}"

class Location(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

    def __str__(self):
        return self.name

# Add car types
CarType.objects.get_or_create(name='Hatchback')
CarType.objects.get_or_create(name='Saloon')
CarType.objects.get_or_create(name='Estate')
CarType.objects.get_or_create(name='MPV')
CarType.objects.get_or_create(name='SUV')
CarType.objects.get_or_create(name='Sports car')

# Add fuel types
FuelType.objects.get_or_create(name='Petrol')
FuelType.objects.get_or_create(name='Diesel')
FuelType.objects.get_or_create(name='Hybrid')
FuelType.objects.get_or_create(name='Electric')
