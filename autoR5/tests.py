from django.test import TestCase, override_settings
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
from django.urls import reverse
from unittest.mock import patch, Mock
import stripe
from django.http import HttpResponseRedirect
from django.urls.exceptions import NoReverseMatch
from .signals import process_cancellation_request


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


@override_settings(
    STATICFILES_STORAGE='django.contrib.staticfiles.storage.StaticFilesStorage',
    DEFAULT_FILE_STORAGE='django.core.files.storage.FileSystemStorage'
)
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
        # Clean up run after every test method.
        if self.user_profile and self.user_profile.profile_picture:
            os.remove(self.user_profile.profile_picture.path)

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

        # Check if the response status code is as expected (e.g., 200 for a successful booking)
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
