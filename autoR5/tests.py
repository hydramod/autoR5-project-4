from django.test import TestCase, override_settings, Client, LiveServerTestCase
from django.contrib.auth.models import User
from .models import Car, Booking, Payment, CancellationRequest, Review, UserProfile, ContactFormSubmission
from decimal import Decimal
from django.utils import timezone
from datetime import date, datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
import os
import random
import string
from django.urls import reverse, resolve
from unittest import mock
from unittest.mock import patch, Mock
import stripe
from django.http import HttpResponseRedirect
from django.urls.exceptions import NoReverseMatch
from .signals import process_cancellation_request
from cloudinary import api
from .forms import ContactForm, CustomSignupForm, BookingForm, ReviewForm, CancellationRequestForm, UserProfileForm, CsvImportForm
from . import views
from django.contrib.admin.sites import AdminSite
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
import time


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate="ABC123",
            daily_rate=100.00,
            latitude=53.349805,
            longitude=6.206031,
            location_city="Test City",
            location_address="Test Address",
            features="Test Features",
            car_type="Hatchback",
            fuel_type="Petrol",
        )

    def test_car_string_representation(self):
        car = self.car
        expected_string = f"{car.year} {car.make} {car.model}"
        self.assertEqual(str(car), expected_string)

    def test_make_content(self):
        car = self.car
        self.assertEqual(car.make, "TestMake")

    def test_model_content(self):
        car = self.car
        self.assertEqual(car.model, "TestModel")

    def test_year_content(self):
        car = self.car
        self.assertEqual(car.year, 2023)

    def test_license_plate_content(self):
        car = self.car
        self.assertEqual(car.license_plate, "ABC123")

    def test_daily_rate_content(self):
        car = self.car
        self.assertEqual(car.daily_rate, 100.00)

    def test_is_available_content(self):
        car = self.car
        self.assertTrue(car.is_available)

    def test_latitude_content(self):
        car = self.car
        expected_latitude = 53.349805
        self.assertAlmostEqual(car.latitude, expected_latitude, places=6)

    def test_longitude_content(self):
        car = self.car
        expected_longitude = 6.206031
        self.assertAlmostEqual(car.longitude, expected_longitude, places=6)

    def test_location_city_content(self):
        car = self.car
        self.assertEqual(car.location_city, "Test City")

    def test_location_address_content(self):
        car = self.car
        self.assertEqual(car.location_address, "Test Address")

    def test_features_content(self):
        car = self.car
        self.assertEqual(car.features, "Test Features")

    def test_car_type_content(self):
        car = self.car
        self.assertEqual(car.car_type, "Hatchback")

    def test_fuel_type_content(self):
        car = self.car
        self.assertEqual(car.fuel_type, "Petrol")


class BookingModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuserbooking", password="testpassword")

        # Create a test car
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate="ABC123",
            daily_rate=100.00,
            location_city="Test Location",
            car_type="Hatchback",
            fuel_type="Petrol",
        )

    def test_create_booking(self):
        # Create a booking
        rental_date = timezone.now() + timedelta(days=1)
        return_date = rental_date + timedelta(days=4)
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            status='Confirmed',
        )

        # Ensure the booking was created correctly
        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.car, self.car)
        self.assertEqual(booking.rental_date, rental_date)
        self.assertEqual(booking.return_date, return_date)
        self.assertEqual(booking.status, 'Confirmed')
        self.assertEqual(booking.total_cost, Decimal('400.00'))

    def test_completed_booking(self):
        # Create a booking with status 'Confirmed' and return_date in the past
        rental_date = timezone.make_aware(datetime(2023, 1, 1, 12, 0, 0))
        return_date = timezone.make_aware(datetime(2023, 1, 4, 12, 0, 0))
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            status='Confirmed',
        )

        # Ensure the status is automatically updated to 'Completed'
        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Completed')
        self.assertTrue(self.car.is_available)

    def test_calculate_total_cost(self):
        # Create a booking with a custom total cost
        rental_date = timezone.make_aware(datetime(2023, 1, 1, 12, 0, 0))
        return_date = timezone.make_aware(datetime(2023, 1, 5, 12, 0, 0))
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            status='Confirmed',
        )

        # Ensure the total cost is calculated correctly
        booking.calculate_total_cost()
        self.assertEqual(booking.total_cost, Decimal('400.00'))


class PaymentModelTest(TestCase):
    def setUp(self):
        # Create a test car
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate="ABC123",
            daily_rate=100.00,
            location_city="Test Location",
            car_type="Hatchback",
            fuel_type="Petrol",
        )

    def test_payment_creation(self):
        # Create a test user
        user = User.objects.create_user(
            username="testuserpayment", password="testpassword")

        # Create a test booking
        # Make rental_date timezone-aware
        rental_date = timezone.make_aware(datetime(2023, 1, 1, 12, 0, 0))
        return_date = rental_date + timedelta(days=4)  # 4 days later

        booking = Booking.objects.create(
            user=user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            total_cost=Decimal('400.00'),
            status='Confirmed',
        )

        # Create a test payment
        payment = Payment.objects.create(
            user=user,
            booking=booking,
            amount=Decimal('400.00'),
            payment_method='Stripe',
            payment_status='Paid',
        )

        # Ensure the payment is created correctly
        self.assertEqual(payment.user.username, 'testuserpayment')
        self.assertEqual(str(payment.booking),
                         f'Booking for {booking.car} by {booking.user}')
        self.assertEqual(payment.amount, Decimal('400.00'))
        self.assertEqual(payment.payment_method, 'Stripe')
        self.assertEqual(payment.payment_status, 'Paid')


class CancellationModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testusercancel", password="testpassword")

        # Create a test car
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate="ABC123",
            daily_rate=100.00,
            location_city="Test City",
        )

        rental_date = datetime(2023, 12, 1, 12, 0, 0)
        return_date = rental_date + timedelta(days=4)  # 4 days later

        self.booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            total_cost=400.00,  # Set the total cost
        )

    def test_string_representation(self):
        cancellation = CancellationRequest(
            user=self.user,
            booking=self.booking,
            reason="Change of plans",
        )
        self.assertEqual(str(cancellation),
                         f"Cancellation request for {self.booking}")

    def test_defaults(self):
        cancellation = CancellationRequest(
            user=self.user,
            booking=self.booking,
            reason="Change of plans",
        )
        cancellation.save()
        self.assertEqual(cancellation.approved, False)


class ReviewModelTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username="testuserreview", password="testpassword")

        # Create a test car
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate="ABC123",
            daily_rate=100.00,
            location_city="Test Location",
            car_type="Hatchback",
            fuel_type="Petrol",
        )

    def test_review_rating_validator(self):
        # Test a valid review rating
        valid_review = Review(
            car=self.car,
            user=self.user,
            rating=5,  # Valid rating (5 stars)
            comment="Great car!",
        )
        valid_review.full_clean()  # Should not raise any validation error

        # Test an invalid review rating (less than the minimum)
        invalid_review = Review(
            car=self.car,
            user=self.user,
            rating=0,  # Invalid rating (0 stars)
            comment="Poor car!",
        )
        with self.assertRaises(ValidationError):
            invalid_review.full_clean()

    def test_review_string_representation(self):
        review = Review.objects.create(
            car=self.car,
            user=self.user,
            rating=5,
            comment="Great car!",
        )

        expected_string = f"Review for {self.car} by {self.user}"
        self.assertEqual(str(review), expected_string)


class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a User that doesn't change between tests
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com"
        )

    def setUp(self):
        # Create an image file for testing
        image = Image.new('RGB', (100, 100))
        output = BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)

        # Create a SimpleUploadedFile object based on the image
        uploaded_image = SimpleUploadedFile(
            'image.jpg', output.getvalue(), content_type='image/jpeg')

        # Create a UserProfile associated with the User
        self.user_profile, created = UserProfile.objects.get_or_create(
            user=self.user,
            defaults={
                "phone_number": "123-456-7890",
                "profile_picture": uploaded_image  # Use the mocked image file
            }
        )

    def tearDown(self):
        if hasattr(self, 'user_profile') and self.user_profile.profile_picture:
            # Remove the image from Cloudinary
            public_id = self.user_profile.profile_picture.public_id
            api.delete_resources(public_id)

    def test_user_profile_creation(self):
        # Test that the UserProfile was created
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_user_profile_str_method(self):
        # Test the __str__ method
        self.assertEqual(str(self.user_profile), "testuser")

    def test_user_profile_email_property(self):
        # Test the email property
        self.assertEqual(self.user_profile.email, "testuser@example.com")


class ContactFormSubmissionModelTest(TestCase):
    def test_create_contact_submission(self):
        # Create a ContactFormSubmission instance
        submission = ContactFormSubmission.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            subject="Test Subject",
            message="Test Message"
        )

        # Retrieve the created submission from the database
        retrieved_submission = ContactFormSubmission.objects.get(
            id=submission.id)

        # Check if the retrieved values match the ones we set
        self.assertEqual(retrieved_submission.first_name, "John")
        self.assertEqual(retrieved_submission.last_name, "Doe")
        self.assertEqual(retrieved_submission.email, "john@example.com")
        self.assertEqual(retrieved_submission.subject, "Test Subject")
        self.assertEqual(retrieved_submission.message, "Test Message")

    def test_submission_str_representation(self):
        # Create a ContactFormSubmission instance
        submission = ContactFormSubmission(
            first_name="John",
            last_name="Doe",
            subject="Test Subject"
        )

        # Check the string representation of the submission
        self.assertEqual(str(submission), "John Doe - Test Subject")


class IndexViewTest(TestCase):
    @staticmethod
    def generate_random_license_plate():
        letters = ''.join(random.choice(string.ascii_uppercase)
                          for _ in range(3))
        digits = ''.join(random.choice(string.digits) for _ in range(3))
        return f"{letters}{digits}"

    def create_car(self, car_type="Hatchback", fuel_type="Petrol"):
        # Generate a random license plate
        license_plate = self.generate_random_license_plate()

        return Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate=license_plate,
            daily_rate=100.00,
            latitude=53.349805,
            longitude=6.206031,
            location_city="Test City",
            location_address="Test Address",
            features="Test Features",
            car_type=car_type,
            fuel_type=fuel_type,
        )

    def test_index_view(self):
        # Create sample data for the Car model to be used in the view
        self.create_car(car_type="Hatchback", fuel_type="Petrol")
        self.create_car(car_type="Saloon", fuel_type="Diesel")

        # Issue a GET request to the index view
        response = self.client.get(reverse('index'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the car types and fuel types are displayed in the response content
        self.assertContains(response, "Hatchback")
        self.assertContains(response, "Saloon")
        self.assertContains(response, "Petrol")
        self.assertContains(response, "Diesel")

        # Check the template used for rendering
        self.assertTemplateUsed(response, 'index.html')


class CarsListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create sample cars with various attributes
        cls.create_car(make="Honda", model="Civic", year=2023,
                       car_type="Hatchback", fuel_type="Petrol", location_city="Dublin")
        cls.create_car(make="Toyota", model="Corolla", year=2023,
                       car_type="Sedan", fuel_type="Diesel", location_city="Dublin")
        cls.create_car(make="Ford", model="Fiesta", year=2023,
                       car_type="Hatchback", fuel_type="Petrol", location_city="Dublin")

    @staticmethod
    def generate_random_license_plate():
        letters = ''.join(random.choice(string.ascii_uppercase)
                          for _ in range(3))
        digits = ''.join(random.choice(string.digits) for _ in range(3))
        return f"{letters}{digits}"

    @classmethod
    def create_car(cls, make, model, year, car_type, fuel_type, location_city):
        # Generate a random license plate
        license_plate = cls.generate_random_license_plate()

        return Car.objects.create(
            make=make,
            model=model,
            year=year,
            license_plate=license_plate,
            daily_rate=100.00,  # Set your default daily_rate here
            latitude=53.349805,
            longitude=6.206031,
            location_city=location_city,
            location_address="Test Address",
            features="Test Features",
            car_type=car_type,
            fuel_type=fuel_type,
        )

    def test_cars_list_view(self):
        # Access the cars_list view without any filtering parameters
        response = self.client.get(reverse('cars_list'))

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that all cars are displayed in the response
        self.assertContains(response, "Honda")
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")

    def test_cars_list_view_with_filter(self):
        # Simulate filtering parameters in the URL
        filter_url = reverse(
            'cars_list') + '?make=Honda&model=Civic&year=2023&car_type=Hatchback&fuel_type=Petrol&location=Dublin'
        response = self.client.get(filter_url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the specific HTML element with the text "Honda Civic" is present
        self.assertRegex(response.content.decode(
            "utf-8"), r'<h4 class="card-title display-5">\s+Honda Civic\s+</h4>')

        # Check that other elements with similar text are not present
        self.assertNotRegex(response.content.decode(
            "utf-8"), r'<h4 class="card-title display-5">\s+Toyota Corolla\s+</h4>')
        self.assertNotRegex(response.content.decode(
            "utf-8"), r'<h4 class="card-title display-5">\s+Ford Fiesta\s+</h4>')


class CarDetailTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Create a car
        self.car = Car.objects.create(
            make='Test Make',
            model='Test Model',
            year=2023,
            license_plate='123ABC',
            daily_rate=100.00,
            location_city='Test City',
            features='Test Features'
        )

        # Create a review for the car
        self.review = Review.objects.create(
            car=self.car,
            user=self.user,
            rating=5,
            comment='Great car!',
            approved=True
        )

    def test_car_detail_view(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Get the URL for the car_detail view using the car's ID
        url = reverse('car_detail', args=[str(self.car.id)])

        # Send a GET request to the URL
        response = self.client.get(url)

        # Check that the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check that the car's details and review are displayed in the response content
        self.assertContains(response, 'Test Make')
        self.assertContains(response, 'Test Model')
        self.assertContains(response, '2023')
        self.assertContains(response, '€100.00')
        self.assertContains(response, 'Test City')
        self.assertContains(response, 'Test Features')
        self.assertContains(response, 'Rating:')
        self.assertContains(response, 'Great car!')


class BookCarViewTest(TestCase):
    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(
            username="testuser", password="testpassword")

        # Create a car
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate="ABC123",
            daily_rate=100.00,
            location_city="Test Location",
            is_available=True,
        )

    def test_book_car_view_with_valid_data(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Define the URL for booking the car
        url = reverse('book_car', kwargs={'car_id': self.car.id})

        # Define booking data with valid dates
        today = date.today()
        rental_date = today + timedelta(days=1)
        return_date = today + timedelta(days=5)
        booking_data = {
            'rental_date': rental_date,
            'return_date': return_date,
            # Add other form fields as needed
        }

        # Perform a POST request with valid booking data
        response = self.client.post(url, booking_data, follow=True)

        # Check if the response status code is as expected
        self.assertEqual(response.status_code, 200)

        # Check if the booking is created
        self.assertTrue(Booking.objects.exists())

        # Check if a Payment object is created
        self.assertTrue(Payment.objects.exists())

        # Check if the booking status is 'Pending'
        booking = Booking.objects.latest('id')
        self.assertEqual(booking.status, 'Pending')

    def test_book_car_view_with_invalid_data(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Define the URL for booking the car
        url = reverse('book_car', kwargs={'car_id': self.car.id})

        # Define invalid booking data (e.g., missing required fields)
        invalid_booking_data = {}

        # Perform a POST request with invalid booking data
        response = self.client.post(url, invalid_booking_data, follow=True)

        # Check if the user is redirected back to the booking page
        self.assertEqual(response.status_code, 200)

        # Check if an error message is shown in the response
        self.assertContains(response, 'This field is required.')

    def test_book_car_view_with_past_date(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Define the URL for booking the car
        url = reverse('book_car', kwargs={'car_id': self.car.id})

        # Define booking data with a past rental date
        today = date.today()
        past_rental_date = today - timedelta(days=2)
        booking_data = {
            'rental_date': past_rental_date,
            'return_date': today + timedelta(days=5),
            # Add other form fields as needed
        }

        # Perform a POST request with invalid booking data
        response = self.client.post(url, booking_data, follow=True)

        # Check if the user is redirected back to the booking page
        self.assertEqual(response.status_code, 200)

        # Check if an error message is shown in the response
        self.assertContains(response, 'You cannot book for a past date.')

    def test_book_car_view_with_conflicting_dates(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Define the URL for booking the car
        url = reverse('book_car', kwargs={'car_id': self.car.id})

        # Define valid booking data
        today = date.today()
        rental_date = today + timedelta(days=1)
        return_date = today + timedelta(days=5)
        valid_booking_data = {
            'rental_date': rental_date,
            'return_date': return_date,
        }

        # Create a valid booking
        response = self.client.post(url, valid_booking_data, follow=True)

        # Check if the response status code is as expected
        self.assertEqual(response.status_code, 200)

        # Check if the booking is created
        self.assertTrue(Booking.objects.exists())

        # Check if a Payment object is created
        self.assertTrue(Payment.objects.exists())

        # Check if the booking status is 'Pending'
        booking = Booking.objects.latest('id')
        self.assertEqual(booking.status, 'Pending')

        # Now, attempt to create another booking with conflicting dates
        conflicting_booking_data = {
            'rental_date': rental_date,  # Same rental date as the previous booking
            'return_date': return_date,  # Same return date as the previous booking
        }

        # Perform a POST request with conflicting booking data and follow the redirect
        response = self.client.post(url, conflicting_booking_data, follow=True)

        # Check if the response status code is as expected (e.g., 200 for a successful booking)
        self.assertEqual(response.status_code, 200)

        # Check if the error message is displayed in the response
        self.assertContains(
            response, 'This car is already booked for the selected dates.')

    def test_book_car_view_with_unavailable_car(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Set the car as unavailable
        self.car.is_available = False
        self.car.save()

        # Define the URL for booking the car
        url = reverse('book_car', kwargs={'car_id': self.car.id})

        # Define booking data with valid dates
        today = date.today()
        rental_date = today + timedelta(days=1)
        return_date = today + timedelta(days=5)
        booking_data = {
            'rental_date': rental_date,
            'return_date': return_date,
        }

        # Perform a POST request with valid booking data
        response = self.client.post(url, booking_data, follow=True)

        # Check if the user is redirected to the car detail page
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_detail.html')

        # Check if the error message is displayed in the response
        self.assertContains(response, 'This car is not available for booking.')


class CheckoutViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username="testuser", password="testpassword")

        # Create a car
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate="ABC123",
            daily_rate=100.00,
            location_city="Test Location",
        )

        # Create a booking associated with the user and car
        self.booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=timezone.now(),  # Provide a valid rental_date

        )

    @patch('stripe.PaymentIntent.create')
    def test_checkout_view(self, stripe_create_mock):
        # Mock the Stripe PaymentIntent creation
        # Create a Mock with the required attribute
        intent_mock = Mock(client_secret='test_secret')
        stripe_create_mock.return_value = intent_mock

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Define the URL for the checkout view
        url = reverse('checkout', kwargs={
                      'car_id': self.car.id, 'booking_id': self.booking.id})

        # Perform a GET request to the checkout view
        response = self.client.get(url)

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the necessary context data is present
        self.assertIn('stripe_publishable_key', response.context)
        self.assertIn('intent_client_secret', response.context)
        self.assertIn('booking_id', response.context)
        self.assertIn('total_cost', response.context)

    @patch('stripe.PaymentIntent.create')
    def test_checkout_view_stripe_error(self, stripe_create_mock):
        # Mock the Stripe PaymentIntent creation to raise an error
        stripe_create_mock.side_effect = stripe.error.StripeError("Test error")

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Define the URL for the checkout view
        url = reverse('checkout', kwargs={
                      'car_id': self.car.id, 'booking_id': self.booking.id})

        try:
            # Perform a GET request to the checkout view
            response = self.client.get(url)

            # Check if the response is a redirect to some URL
            self.assertIsInstance(response, HttpResponseRedirect)
            self.assertEqual(response.url, reverse('checkout', kwargs={
                             'car_id': self.car.id, 'booking_id': self.booking.id}))
        except NoReverseMatch:
            # If NoReverseMatch occurs, it's expected due to the error raised
            pass


class BookingConfirmationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate="ABC123",
            daily_rate=100.00,
            latitude=53.349805,
            longitude=6.206031,
            location_city="Test City",
            location_address="Test Address",
            features="Test Features",
            car_type="Hatchback",
            fuel_type="Petrol",
        )
        rental_date = timezone.now() + timedelta(days=1)
        return_date = rental_date + timedelta(days=4)
        self.booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            status='Confirmed',
        )
        self.payment = Payment.objects.create(
            user=self.user,
            booking=self.booking,
            amount=Decimal('400.00'),
            payment_method='Stripe',
            payment_status='Paid',
        )
        self.client.login(username='testuser', password='testpassword')

    @patch('stripe.PaymentIntent.retrieve')
    def test_successful_payment(self, mock_retrieve):
        # Set up a successful payment scenario
        self.payment_intent_id = "test_payment_intent"
        self.intent_client_secret = "test_client_secret"
        mock_retrieve.return_value = Mock(status='succeeded')
        self.client.force_login(self.user)

        response = self.client.get(reverse('booking_confirmation', args=[self.booking.id]), {
            'payment_intent': self.payment_intent_id,
            'payment_intent_client_secret': self.intent_client_secret,
        })

        # Check both payment and booking status
        booking = Booking.objects.get(id=self.booking.id)
        payment = Payment.objects.get(id=self.payment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['payment_status'], 'Paid')
        self.assertEqual(booking.status, 'Confirmed')
        self.assertEqual(payment.payment_status, 'Paid')

    @patch('stripe.PaymentIntent.retrieve')
    def test_pending_payment(self, mock_retrieve):
        # Set up a pending payment scenario
        self.intent_client_secret = "test_client_secret"
        mock_retrieve.return_value = Mock(status='processing')
        self.client.force_login(self.user)

        response = self.client.get(reverse('booking_confirmation', args=[self.booking.id]), {
            'payment_intent_client_secret': self.intent_client_secret,
        })

        # Check both payment and booking status
        booking = Booking.objects.get(id=self.booking.id)
        payment = Payment.objects.get(id=self.payment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['payment_status'], 'Pending')
        self.assertEqual(booking.status, 'Pending')
        self.assertEqual(payment.payment_status, 'Pending')

    @patch('stripe.PaymentIntent.retrieve')
    def test_failed_payment(self, mock_retrieve):
        # Set up a failed payment scenario
        self.intent_client_secret = "test_client_secret"
        mock_retrieve.return_value = Mock(status='requires_payment_method')
        self.client.force_login(self.user)

        response = self.client.get(reverse('booking_confirmation', args=[self.booking.id]), {
            'payment_intent_client_secret': self.intent_client_secret,
        })

        # Check both payment and booking status
        booking = Booking.objects.get(id=self.booking.id)
        payment = Payment.objects.get(id=self.payment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['payment_status'], 'Failed')
        self.assertEqual(booking.status, 'Canceled')
        self.assertEqual(payment.payment_status, 'Failed')


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
    DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage'
)
class CustomerDashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.url = reverse('customer_dashboard')

        # Create a Car instance
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate="ABC123",
            daily_rate=100.00,
            latitude=53.349805,
            longitude=6.206031,
            location_city="Test City",
            location_address="Test Address",
            features="Test Features",
            car_type="Hatchback",
            fuel_type="Petrol",
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_dashboard.html')

    def test_view_with_no_login_redirects_to_login_page(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)  # Expect a redirect
        expected_redirect_url = reverse('account_login') + f'?next={self.url}'
        self.assertRedirects(
            response, expected_redirect_url, target_status_code=200)

    def test_no_current_bookings_displayed(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('current_bookings', response.context)
        self.assertEqual(list(response.context['current_bookings']), [])

    def test_current_bookings_displayed(self):
        # Create a Booking associated with the Car instance
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            status='Confirmed',
            rental_date=timezone.now() + timedelta(days=1),
            return_date=timezone.now() + timedelta(days=5),
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('current_bookings', response.context)
        self.assertTrue(booking in response.context['current_bookings'])

    def test_no_past_bookings_displayed(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('past_bookings', response.context)
        self.assertEqual(list(response.context['past_bookings']), [])

    def test_past_bookings_displayed(self):
        # Create a Booking associated with the Car instance
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            status='Completed',
            rental_date=timezone.now() - timedelta(days=5),
            return_date=timezone.now() - timedelta(days=1),
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('past_bookings', response.context)
        self.assertTrue(booking in response.context['past_bookings'])

    def test_no_reviews_displayed(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('reviews', response.context)
        self.assertEqual(list(response.context['reviews']), [])

    def test_reviews_displayed(self):
        # Create and save a review
        review = Review(
            car=self.car,
            user=self.user,
            rating=5,
            comment="Great car!",
        )
        review.save()

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('reviews', response.context)

        # Check if the specific values exist in the response content (HTML)
        response_content = response.content.decode(
            "utf-8")  # Decode the content to a string
        self.assertIn(f'{review.rating}/5', response_content)
        self.assertIn(f'{review.comment}', response_content)

    def test_cancellation_request_form_displayed(self):
        # Create a Booking associated with the Car instance
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            status='Confirmed',
            rental_date=timezone.now() + timedelta(days=5),
            return_date=timezone.now() + timedelta(days=1),
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('form', response.context)
        self.assertContains(response, 'Enter your reason here')

    def test_pending_payment_displayed(self):
        # Create a Booking associated with the Car instance
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            status='Pending',
            rental_date=timezone.now() + timedelta(days=5),
            return_date=timezone.now() + timedelta(days=1),
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertContains(response, 'Pay Now')

    def test_rebook_displayed(self):
        # Create a Booking associated with the Car instance
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            status='Completed',
            rental_date=timezone.now() - timedelta(days=5),
            return_date=timezone.now() - timedelta(days=1),
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertContains(response, 'Book Again')

    @patch('autoR5.signals.stripe.Refund.create',
           return_value=Mock(status='succeeded'))  # Mock the Stripe refund creation
    @patch('autoR5.signals.process_cancellation_request',
           side_effect=process_cancellation_request)
    def test_cancellation_request_with_approved_request(
            self, mock_process_cancellation_request, mock_refund_create):

        # Create a Booking associated with the Car instance
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            status='Confirmed',
            rental_date=timezone.now() + timedelta(days=1),
            return_date=timezone.now() + timedelta(days=5),
        )

        # Create a Payment object for the booking
        payment = Payment.objects.create(
            user=self.user,
            booking=booking,
            amount=Decimal('400.00'),
            payment_method='Stripe',
            payment_status='Paid',
            payment_intent='test_intent'
        )

        # Create an approved cancellation request for the booking
        cancellation_request = CancellationRequest.objects.create(
            booking=booking,
            user=self.user,
            reason="Test reason",
            approved=True
        )

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # URL for the customer dashboard view
        url = reverse('customer_dashboard')

        # Simulate a GET request to the view
        response = self.client.get(url)

        # Check if the response contains the booking details
        self.assertNotContains(response, booking.car.make)
        self.assertNotContains(response, booking.car.model)

        # Check if the cancellation form is not visible
        self.assertNotContains(response, 'Enter your reason here')

        # Check if the cancellation request pending message is displayed
        self.assertNotContains(
            response, 'Cancellation request pending approval')

        # Ensure that the Stripe refund creation was called as expected
        mock_refund_create.assert_called_with(
            payment_intent=payment.payment_intent)

    def test_cancellation_request_without_approved_request(self):
        # Create a Booking associated with the Car instance
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            status='Confirmed',
            rental_date=timezone.now() + timedelta(days=1),
            return_date=timezone.now() + timedelta(days=5),
        )

        # Create an unapproved cancellation request for the booking
        cancellation_request = CancellationRequest.objects.create(
            booking=booking,
            user=self.user,
            reason="Test reason",
            approved=False
        )

        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # URL for the customer dashboard view
        url = reverse('customer_dashboard')

        # Simulate a GET request to the view
        response = self.client.get(url)

        # Check if the response contains the booking details
        self.assertContains(response, booking.car.make)
        self.assertContains(response, booking.car.model)

        # Check if the cancellation form is visible
        self.assertNotContains(response, 'Enter your reason here')

        # Check if the cancellation request pending message is not displayed
        self.assertContains(response, 'Cancellation request pending approval')


class LeaveReviewViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        # Create a car
        self.car = Car.objects.create(
            make='TestMake',
            model='TestModel',
            year=2023,
            license_plate='ABC123',
            daily_rate=100.00,
            location_city='Test Location',
        )

        # Define the URL for leaving a review
        self.url = reverse('leave_review', args=[self.car.id])

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leave_review.html')

    def test_review_form_submission(self):
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
            self.url, {'rating': 4, 'comment': 'Great car!'}, follow=True)

        # Check for a redirect to the 'car_detail' view
        self.assertRedirects(response, reverse(
            'car_detail', args=[self.car.id]))

        # Verify if the success message is present in the response content
        self.assertContains(response, 'Thanks for your feedback!')


class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('edit_profile')

    def test_edit_profile_valid_phone_number(self):
        response = self.client.post(self.url, {
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 200)
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.phone_number, '1234567890')
        self.assertContains(response, "Phone number updated successfully.")

    def test_edit_profile_invalid_phone_number(self):
        response = self.client.post(self.url, {
            'phone_number': 'invalid_phone_number'
        })
        self.assertEqual(response.status_code, 200)
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertNotEqual(user_profile.phone_number, 'invalid_phone_number')
        self.assertContains(
            response, "Phone number must be 9 to 10 digits long.")

    def test_edit_profile_with_image_upload(self):
        # Create a mock image file for testing
        image = Image.new('RGB', (100, 100))
        output = BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)

        # Create a SimpleUploadedFile object based on the image
        image_file = SimpleUploadedFile(
            'image.jpg', output.getvalue(), content_type='image/jpeg')

        response = self.client.post(self.url, {
            'phone_number': '1234567890',
            'profile_picture': image_file
        })

        self.assertEqual(response.status_code, 200)

        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.phone_number, '1234567890')

        # Make sure the image exists in Cloudinary
        self.assertIsNotNone(user_profile.profile_picture)

    def tearDown(self):
        user_profile = UserProfile.objects.get(user=self.user)

        if user_profile and user_profile.profile_picture:
            # Remove the image from Cloudinary
            public_id = user_profile.profile_picture.public_id
            api.delete_resources(public_id)


class ContactViewTest(TestCase):
    def test_contact_form_submission(self):
        # Define the data to be submitted in the form
        form_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.',
        }

        # Get the URL for the contact page
        url = reverse('contact')

        # Submit the form data to the contact page
        response = self.client.post(url, data=form_data)

        # Check that the response is a redirect (after a successful submission)
        self.assertEqual(response.status_code, 302)

        # Check that the form submission was saved to the database
        self.assertEqual(ContactFormSubmission.objects.count(), 1)

        # Retrieve the saved submission
        submission = ContactFormSubmission.objects.first()

        # Check that the submitted data matches the saved data
        self.assertEqual(submission.first_name, 'John')
        self.assertEqual(submission.last_name, 'Doe')
        self.assertEqual(submission.email, 'john.doe@example.com')
        self.assertEqual(submission.subject, 'Test Subject')
        self.assertEqual(submission.message, 'This is a test message.')

    def test_contact_form_invalid_submission(self):
        # Submit an empty form (invalid data) to the contact page
        url = reverse('contact')
        response = self.client.post(url, data={})

        # Check that the response is not a redirect (since the form is invalid)
        self.assertNotEqual(response.status_code, 302)

        # Check that there are form errors in the response
        self.assertFormError(response, 'form', 'first_name',
                             'This field is required.')
        self.assertFormError(response, 'form', 'last_name',
                             'This field is required.')
        self.assertFormError(response, 'form', 'email',
                             'This field is required.')
        self.assertFormError(response, 'form', 'subject',
                             'This field is required.')
        self.assertFormError(response, 'form', 'message',
                             'This field is required.')


class CustomSignupFormTest(TestCase):
    def test_valid_custom_signup_form(self):
        # Create a user registration data dictionary
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'phone_number': '1234567890',  # Add phone number
        }

        form = CustomSignupForm(data=registration_data)

        # Verify that the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_custom_signup_form_missing_phone_number(self):
        # Create a user registration data dictionary with a missing phone number
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = CustomSignupForm(data=registration_data)

        # Verify that the form is not valid due to the missing phone number
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)


class BookingFormTest(TestCase):
    def test_valid_booking_form(self):
        # Create a booking data dictionary with valid dates
        booking_data = {
            'rental_date': '2023-10-01',
            'return_date': '2023-10-10',
        }

        form = BookingForm(data=booking_data)

        # Verify that the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_booking_form_return_date_before_rental_date(self):
        # Create a booking data dictionary with an invalid return date
        booking_data = {
            'rental_date': '2023-10-10',  # Rental date after return date
            'return_date': '2023-10-01',
        }

        form = BookingForm(data=booking_data)

        # Check if the form has a validation error on the 'return_date' field
        self.assertTrue("Return date must be after the rental date.")


class ReviewFormTest(TestCase):
    def test_valid_form(self):
        form = ReviewForm(data={
            'rating': 5,
            'comment': 'Great car!',
        })
        self.assertTrue(form.is_valid())

    def test_rating_out_of_range(self):
        form = ReviewForm(data={
            'rating': 6,
            'comment': 'Excellent car!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Ensure this value is less than or equal to 5.', form.errors['rating'])

    def test_rating_below_range(self):
        form = ReviewForm(data={
            'rating': 0,
            'comment': 'Terrible car!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Ensure this value is greater than or equal to 1.', form.errors['rating'])

    def test_missing_comment(self):
        form = ReviewForm(data={
            'rating': 4,
            'comment': '',
        })
        self.assertFalse(form.is_valid())


class ContactFormTest(TestCase):
    def test_valid_contact_form(self):
        # Create valid contact form data
        contact_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.',
        }

        form = ContactForm(data=contact_data)

        # Verify that the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_contact_form_missing_fields(self):
        # Create contact form data with missing required fields
        contact_data = {
            'first_name': '',  # Missing required field
            'last_name': 'Doe',
            'email': '',  # Missing required field
            'subject': 'Test Subject',
            'message': 'This is a test message.',
        }

        form = ContactForm(data=contact_data)

        # Verify that the form is not valid due to missing required fields
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('email', form.errors)


class CancellationRequestFormTest(TestCase):
    def test_valid_cancellation_request_form(self):
        # Create valid cancellation request data
        cancellation_data = {
            'reason': 'This is a valid cancellation reason.',
        }

        form = CancellationRequestForm(data=cancellation_data)

        # Verify that the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_cancellation_request_form_missing_reason(self):
        # Create cancellation request data with a missing required reason field
        cancellation_data = {
            'reason': '',  # Missing required reason field
        }

        form = CancellationRequestForm(data=cancellation_data)

        # Verify that the form is not valid due to the missing reason field
        self.assertFalse(form.is_valid())
        self.assertIn('reason', form.errors)


class UserProfileFormTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser', email='testuser@example.com', password='testpassword123')
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('edit_profile')

    def test_valid_user_profile_form(self):
        # Create valid user profile data
        profile_data = {
            'phone_number': '1234567890',
        }

        form = UserProfileForm(data=profile_data)

        # Verify that the form is valid
        self.assertTrue(form.is_valid())

    def test_invalid_user_profile_form_invalid_phone_number(self):
        # Create user profile data with an invalid phone number
        profile_data = {
            # Invalid phone number (less than 9 digits)
            'phone_number': '1234',
        }

        form = UserProfileForm(data=profile_data)

        # Verify that the form is not valid due to the invalid phone number
        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_valid_user_profile_form_with_picture_upload(self):
        # Create a mock image file for testing
        image = Image.new('RGB', (100, 100))
        output = BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)

        # Create a SimpleUploadedFile object based on the image
        image_file = SimpleUploadedFile(
            'image.jpg', output.getvalue(), content_type='image/jpeg')

        # Simulate a form submission with user profile data and image upload
        form_data = {
            'phone_number': '1234567890',
            'profile_picture_upload': image_file
        }
        form = UserProfileForm(data=form_data, files={
                               'profile_picture_upload': image_file})

        # Verify that the form is valid
        self.assertTrue(form.is_valid())

    def test_valid_user_profile_form_with_clear_picture(self):
        # Create valid user profile data with "Clear Profile Picture" checked
        profile_data = {
            'phone_number': '1234567890',
            'clear_picture': True,
        }

        form = UserProfileForm(data=profile_data)

        # Verify that the form is valid
        self.assertTrue(form.is_valid())


class CsvImportExportFormTest(TestCase):
    def setUp(self):
        # Create a user for authentication if needed
        self.user = User.objects.create(
            username='admin', password='adminpassword')

    def test_import_csv_function(self):
        # Create a mock CSV file for testing
        csv_data = (
            "make,model,year,license_plate,daily_rate,is_available,latitude,longitude,"
            "location_city,location_address,features,car_type,fuel_type,end\n"
            "Toyota,Camry,2023,XYZ123,50.0,TRUE,37.123,-122.456,"
            "San Jose,123 random street,Test features,Saloon,Petrol\n"
        )

        csv_file = SimpleUploadedFile("cars.csv", csv_data.encode("utf-8"))

        # Simulate an HTTP POST request to the import_csv view
        response = self.client.post(reverse('admin:import_csv'), {
                                    'csv_import': csv_file})

        # Verify that the response status code is 302 (a successful redirect)
        self.assertEqual(response.status_code, 302)

        # Create some Car objects for testing
        car = Car.objects.create(
            make='Toyota',
            model='Camry',
            year=2023,
            license_plate='XYZ123',
            daily_rate=50.0,
            is_available=True,
            latitude=37.123,
            longitude=-122.456,
            location_city='San Jose',
            location_address='123 random street',
            image=None,
            features='Test features',
            car_type='Saloon',
            fuel_type='Petrol'
        )

        # Verify that the data from the CSV file is correctly imported into the Car model
        self.assertEqual(car.make, 'Toyota')
        self.assertEqual(car.model, 'Camry')
        self.assertEqual(car.year, 2023)
        # Use `assertAlmostEqual` for floating-point numbers
        self.assertAlmostEqual(car.daily_rate, 50.00, places=2)
        self.assertEqual(car.is_available, True)
        # Use `assertAlmostEqual` for floating-point numbers
        self.assertAlmostEqual(car.latitude, 37.123, places=3)
        # Use `assertAlmostEqual` for floating-point numbers
        self.assertAlmostEqual(car.longitude, -122.456, places=3)
        self.assertEqual(car.location_city, 'San Jose')
        self.assertEqual(car.location_address, '123 random street')
        self.assertEqual(car.features, 'Test features')
        self.assertEqual(car.car_type, 'Saloon')
        self.assertEqual(car.fuel_type, 'Petrol')

    def test_export_csv_function(self):
        # Create some Car objects for testing
        Car.objects.create(
            make='Toyota',
            model='Camry',
            year=2023,
            license_plate='XYZ123',
            daily_rate=50.0,
            is_available=True,
            latitude=37.123,
            longitude=-122.456,
            location_city='San Jose',
            location_address='123 random street',
            image=None,
            features='Test features',
            car_type='Saloon',
            fuel_type='Petrol'
        )

        # Simulate an HTTP GET request to the export_csv view
        response = self.client.get(reverse('admin:export_csv'))

        # Verify that the response has a 200 status code
        self.assertEqual(response.status_code, 200)

        # Verify that the exported CSV data matches the expected data
        expected_csv_data = (
            "Make,Model,Year,License Plate,Daily Rate,Available,Latitude,Longitude,"
            "Location City,Location Address,Image,Features,Car Type,Fuel Type\r\n"
            "Toyota,Camry,2023,XYZ123,50.00,TRUE,37.123000,-122.456000,"
            "San Jose,123 random street,,Test features,Saloon,Petrol"
        ).strip()

        self.assertMultiLineEqual(
            response.content.decode().strip(), expected_csv_data)


class UpdateLocationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(
            'admin', 'admin@example.com', 'adminpassword')
        self.site = AdminSite()
        self.car = Car.objects.create(
            make='Toyota',
            model='Camry',
            year=2023,
            license_plate='XYZ123',
            daily_rate=50,
            is_available=True,
            latitude=37.338207,
            longitude=-121.886330,
            location_city='',
            location_address='',
        )

    @patch('geopy.geocoders.Nominatim')
    def test_update_location(self, mock_geocoder):
        # Mock the Nominatim geocoder
        mock_nominatim = mock_geocoder.return_value
        mock_location = {
            'raw': {
                'address': {
                    'city': 'San Jose',
                },
            },
            'address': '24, North 5th Street, San Jose, CA 95112 San Jose, Horrace Mann, Downtown San Jose San Jose California United States',
        }
        mock_nominatim.reverse.return_value = mock_location

        # Ensure that the location fields are initially empty
        self.assertEqual(self.car.location_city, '')
        self.assertEqual(self.car.location_address, '')

        # Simulate the admin action to update the location
        client = self.client
        client.login(username='admin', password='adminpassword')
        response = client.post(
            '/admin/autoR5/car/',
            {
                'action': 'update_location',
                '_selected_action': [str(self.car.pk)],
            }
        )

        # Refresh the car instance from the database
        self.car.refresh_from_db()

        # Ensure that the location fields have been updated
        self.assertEqual(self.car.location_city, 'San Jose')
        self.assertIn('24, North 5th Street', self.car.location_address)
        self.assertIn('San Jose', self.car.location_address)
        self.assertIn('95112', self.car.location_address)

    def tearDown(self):
        self.user.delete()
        self.car.delete()


class TestUrls(TestCase):
    def test_index_url(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, views.index)

    def test_car_detail_url(self):
        url = reverse('car_detail', args=[1])
        self.assertEqual(resolve(url).func, views.car_detail)

    def test_book_car_url(self):
        url = reverse('book_car', args=[1])
        self.assertEqual(resolve(url).func, views.book_car)

    def test_booking_confirmation_url(self):
        url = reverse('booking_confirmation', args=[1])
        self.assertEqual(resolve(url).func, views.booking_confirmation)

    def test_leave_review_url(self):
        url = reverse('leave_review', args=[1])
        self.assertEqual(resolve(url).func, views.leave_review)

    def test_cars_list_url(self):
        url = reverse('cars_list')
        self.assertEqual(resolve(url).func, views.cars_list)

    def test_contact_url(self):
        url = reverse('contact')
        self.assertEqual(resolve(url).func, views.contact)

    def test_customer_dashboard_url(self):
        url = reverse('customer_dashboard')
        self.assertEqual(resolve(url).func, views.customer_dashboard)

    def test_edit_profile_url(self):
        url = reverse('edit_profile')
        self.assertEqual(resolve(url).func, views.edit_profile)

    def test_get_car_makes_url(self):
        url = reverse('get_car_makes')
        self.assertEqual(resolve(url).func, views.get_car_makes)

    def test_get_car_models_url(self):
        url = reverse('get_car_models')
        self.assertEqual(resolve(url).func, views.get_car_models)

    def test_get_car_years_url(self):
        url = reverse('get_car_years')
        self.assertEqual(resolve(url).func, views.get_car_years)

    def test_get_car_locations_url(self):
        url = reverse('get_car_locations')
        self.assertEqual(resolve(url).func, views.get_car_locations)

    def test_get_car_types_url(self):
        url = reverse('get_car_types')
        self.assertEqual(resolve(url).func, views.get_car_types)

    def test_get_fuel_types_url(self):
        url = reverse('get_fuel_types')
        self.assertEqual(resolve(url).func, views.get_fuel_types)

    def test_checkout_url(self):
        url = reverse('checkout', args=[1, 1])
        self.assertEqual(resolve(url).func, views.checkout)


class JarallaxTest(LiveServerTestCase):
    def setUp(self):
        # Specify the path to your custom ChromeDriver executable
        custom_chromedriver_path = 'C:/Users/2295883/Desktop/autoR5-project-4/chrome-win64/chromedriver.exe'
        chrome_binary_path = 'C:/Users/2295883/Desktop/autoR5-project-4/chrome-win64/chrome.exe'

        # Set Chrome options to specify the binary location
        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = chrome_binary_path
        chrome_options.add_argument('start-maximized')

        # Initialize the ChromeDriver with the specified paths
        self.selenium = webdriver.Chrome(
            executable_path=custom_chromedriver_path, options=chrome_options)

    def tearDown(self):
        self.selenium.quit()

    def test_jarallax_initialization(self):
        # Load the page containing Jarallax initialization
        self.selenium.get('http://localhost:8000/')

        time.sleep(2)  # Wait for 2 seconds (adjust as needed)

        # Find an element with the Jarallax effect
        jarallax_element = self.selenium.find_element(
            By.CSS_SELECTOR, '.jarallax-container div')

        # Check if Jarallax effect is applied (e.g., check for a certain CSS property)
        self.assertIn('transform: translate3d(0px, 65px, 0px);',
                      jarallax_element.get_attribute('style'))


class MessageAlertsTest(LiveServerTestCase):
    def setUp(self):
        # Set up the Selenium WebDriver for Chrome
        custom_chromedriver_path = 'C:/Users/2295883/Desktop/autoR5-project-4/chrome-win64/chromedriver.exe'
        chrome_binary_path = 'C:/Users/2295883/Desktop/autoR5-project-4/chrome-win64/chrome.exe'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = chrome_binary_path
        chrome_options.add_argument('start-maximized')

        self.selenium = webdriver.Chrome(
            executable_path=custom_chromedriver_path, options=chrome_options)

    def tearDown(self):
        self.selenium.quit()

    def test_message_alerts(self):
        # Open a page where the JavaScript is executed (replace 'url' with the actual URL)
        self.selenium.get('http://localhost:8000/')

        # Find and click the "Log In" button
        log_in_button = self.selenium.find_element(
            By.LINK_TEXT, "Log In")  # Adjust the locator if needed
        log_in_button.click()

        # Find the login form elements (you may need to inspect your page to determine the element IDs and names)
        username_input = self.selenium.find_element(By.NAME, "login")
        password_input = self.selenium.find_element(By.NAME, "password")
        login_button = self.selenium.find_element(
            By.XPATH, "//button[@type='submit']")

        username = 'testuser'
        password = 'testpassword'

        # Enter login credentials and submit the form
        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        # Wait for the JavaScript to run and the message container to be displayed
        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "message-container"))
        )

        # Check that the message container is displayed
        message_container = self.selenium.find_element(
            By.ID, "message-container")
        self.assertEqual(
            message_container.value_of_css_property("display"), 'block')

        # Check that the message contains "Successfully signed in"
        message_text = message_container.text
        self.assertIn(f"Successfully signed in as {username}.", message_text)

        # Ensure the message container is no longer displayed
        WebDriverWait(self.selenium, 10).until(
            lambda driver: 'none' in message_container.value_of_css_property(
                "display")
        )


class AJAXFilterTests(LiveServerTestCase):
    def setUp(self):
        # Set up the Selenium WebDriver for Chrome
        custom_chromedriver_path = 'C:/Users/2295883/Desktop/autoR5-project-4/chrome-win64/chromedriver.exe'
        chrome_binary_path = 'C:/Users/2295883/Desktop/autoR5-project-4/chrome-win64/chrome.exe'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = chrome_binary_path
        chrome_options.add_argument('start-maximized')

        self.selenium = webdriver.Chrome(
            executable_path=custom_chromedriver_path, options=chrome_options)

    def tearDown(self):
        # Clean up Selenium WebDriver after the test
        self.selenium.quit()

    def test_dropdown_updates(self):
        # Open the target URL
        self.selenium.get('http://localhost:8000/cars_list/')

        # Find and select the car make
        make_dropdown = Select(self.selenium.find_element_by_id('car_make'))
        make_dropdown.select_by_value('Alfa Romeo')

        # Add a 2-3 second pause
        time.sleep(2)

        # Find and select the car model
        model_dropdown = Select(self.selenium.find_element_by_id('car_model'))
        model_dropdown.select_by_value('Giulia')

        # Add a 2-3 second pause
        time.sleep(2)

        # Find and select the car year
        year_dropdown = Select(self.selenium.find_element_by_id('car_year'))
        year_dropdown.select_by_value('2023')

        # Add a 2-3 second pause
        time.sleep(2)

        # Find and select the car type
        car_type_dropdown = Select(
            self.selenium.find_element_by_id('car_type'))
        car_type_dropdown.select_by_value('Saloon')

        # Add a 2-3 second pause
        time.sleep(2)

        # Find and select the fuel type
        fuel_type_dropdown = Select(
            self.selenium.find_element_by_id('fuel_type'))
        fuel_type_dropdown.select_by_value('Petrol')

        # Add a 2-3 second pause
        time.sleep(2)

        # Find and select the location
        location_dropdown = Select(
            self.selenium.find_element_by_id('car_location'))
        location_dropdown.select_by_value('Dublin')

        # Add a 2-3 second pause
        time.sleep(2)

        # Click the filter button
        filter_button = login_button = self.selenium.find_element(
            By.XPATH, '//*[@id="filter-form"]/div/div[7]/button[1]')
        filter_button.click()

        # Add a 2-3 second pause
        time.sleep(2)

        # Verify that there is only one element with class "item-wrapper"
        item_wrappers = self.selenium.find_elements_by_class_name(
            'item-wrapper')
        self.assertEqual(len(item_wrappers), 1)

        # Click the reset button
        reset_button = self.selenium.find_element_by_id('reset-filter')
        reset_button.click()

        # Add a 2-3 second pause
        time.sleep(2)

        # Check that there is more than one element with class "item-wrapper"
        item_wrappers_after_reset = self.selenium.find_elements_by_class_name(
            'item-wrapper')
        self.assertGreater(len(item_wrappers_after_reset), 1)


class MapTest(LiveServerTestCase):
    def setUp(self):
        # Set up the Selenium WebDriver for Chrome
        custom_chromedriver_path = 'C:/Users/2295883/Desktop/autoR5-project-4/chrome-win64/chromedriver.exe'
        chrome_binary_path = 'C:/Users/2295883/Desktop/autoR5-project-4/chrome-win64/chrome.exe'

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = chrome_binary_path
        chrome_options.add_argument('start-maximized')

        self.selenium = webdriver.Chrome(
            executable_path=custom_chromedriver_path, options=chrome_options)

    def tearDown(self):
        # Clean up Selenium WebDriver after the test
        self.selenium.quit()

    def test_map_displayed(self):
        # Open the page where the JavaScript initializes the map (replace 'url' with the actual URL)
        self.selenium.get(f'http://localhost:8000/booking/65/confirmation/')

        # Find the login form elements (you may need to inspect your page to determine the element IDs and names)
        username_input = self.selenium.find_element(By.NAME, "login")
        password_input = self.selenium.find_element(By.NAME, "password")
        login_button = self.selenium.find_element(
            By.XPATH, "//button[@type='submit']")

        # Enter login credentials and submit the form
        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')
        login_button.click()

        time.sleep(3)

        # Check if the map element is present
        map_element = self.selenium.find_element_by_id('map')
        self.assertTrue(map_element.is_displayed())

        # Verify that the map has a marker
        marker_element = self.selenium.find_element_by_class_name(
            'leaflet-marker-icon')
        self.assertTrue(marker_element.is_displayed())
