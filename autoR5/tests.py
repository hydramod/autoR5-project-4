from django.test import TestCase
from django.contrib.auth.models import User
from .models import Car, Booking, Payment, CancellationRequest, Review, UserProfile, ContactFormSubmission
from decimal import Decimal
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
import os
import random
import string
from django.urls import reverse


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
            payment_method='Credit Card',
            payment_status='Paid',
        )

        # Ensure the payment is created correctly
        self.assertEqual(payment.user.username, 'testuserpayment')
        self.assertEqual(str(payment.booking),
                         f'Booking for {booking.car} by {booking.user}')
        self.assertEqual(payment.amount, Decimal('400.00'))
        self.assertEqual(payment.payment_method, 'Credit Card')
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
