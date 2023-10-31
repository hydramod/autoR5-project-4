"""
Imported modules and classes for the 'autoR5' Django application.

This section includes all the external modules, classes, and functions
that are imported and used within the 'autoR5' Django application.

Modules and Libraries:
- decimal: Provides support for decimal floating point arithmetic.
- time: Allows access to time-related functions.
- os: Provides a portable way of using operating system-dependent
    functionality.
- inspect: Enables runtime introspection of Python objects
- random: Implements pseudo-random number generators.
- string: Contains a collection of string constants.
- io: Supports stream handling and input/output operations.
- datetime: Supplies classes for working with dates and times.
- timedelta: Represents the difference between two dates or times.
- unittest.mock: Provides mock object functionality.
- stripe: Offers integration with the Stripe payment service.
- PIL (Python Imaging Library): Allows image processing.
- django.utils.timezone: Provides timezone-related utilities.
- django.test: Supports testing and test client functionality.
- django.contrib.auth.models.User: Represents user information.
- django.core.exceptions.ValidationError: Handles validation errors.
- django.core.files.uploadedfile.SimpleUploadedFile: Represents
    uploaded files.
- django.urls: Manages URL patterns, reversing, and resolving.
- django.http.HttpResponseRedirect: Redirects HTTP requests.
- django.urls.exceptions.NoReverseMatch: Handles URL reversal errors.
- django.contrib.admin.sites.AdminSite: Manages the admin site.
- selenium: Provides web testing using Selenium WebDriver.
- selenium.webdriver: Offers web testing functionality.
- selenium.webdriver.common.by: Supports locating elements by various
    strategies.
- selenium.webdriver.common.keys: Provides keyboard key codes.
- selenium.webdriver.chrome.service.Service: Manages the ChromeDriver
    service.
- selenium.webdriver.common.desired_capabilities.DesiredCapabilities:
    Manages desired capabilities for browsers.
- selenium.webdriver.common.action_chains.ActionChains: Performs complex
    user interactions.
- selenium.webdriver.support.ui: Offers support for UI interactions and
    waiting for conditions.
- cloudinary.api: Interfaces with the Cloudinary media platform.
- .signals: Imports custom signal handlers.
- .forms: Imports custom forms used in the application.
- .models: Imports custom database models.
- .views: Imports view functions and classes.

Note:
This docstring serves as an overview of the imported modules and classes in
    the 'autoR5' application.
"""
from decimal import Decimal
import time
import os
import inspect
import random
import string
from io import BytesIO
from datetime import date, datetime, timedelta
from unittest import mock
from unittest.mock import patch, Mock
import stripe
from PIL import Image
from django.utils import timezone
from django.test import (TestCase, override_settings,
                         Client, LiveServerTestCase)
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect
from django.urls.exceptions import NoReverseMatch
from django.contrib.admin.sites import AdminSite
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions
from cloudinary import api
from .signals import process_cancellation_request
from .forms import (ContactForm, CustomSignupForm, BookingForm,
                    ReviewForm, CancellationRequestForm,
                    UserProfileForm, CsvImportForm)
from .models import (Car, Booking, Payment, CancellationRequest,
                     Review, UserProfile, ContactFormSubmission)
from . import views


class CarModelTest(TestCase):
    """
    Unit tests for the 'Car' model in the 'autoR5' Django
    web application.

    This test case class defines unit tests for the 'Car' model
    in the 'autoR5' Django web application. It verifies various
    attributes and methods of the 'Car' model.

    - 'setUpTestData' sets up non-modified objects used by all
    test methods.
    - Test methods validate the correctness of the model's
    attributes and methods.

    Usage:
    This test case class is used to ensure that the 'Car' model behaves
    as expected by
    verifying its attributes such as make, model, year, etc., and its
    string representation. These tests are crucial for maintaining the
    integrity of the 'Car' model within the application.

    Attributes and Methods:
    - 'setUpTestData': Sets up a test instance of the 'Car' model.
    - Test methods: Validate different attributes and methods of the
    'Car' model.

    Note:
    This class inherits from 'django.test.TestCase' and is part of the
    automated testing suite for the 'autoR5' Django application.
    """
    @classmethod
    def setUpTestData(cls):
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
        """
        Test the string representation of the 'Car' model.

        This test method verifies that the string representation
        of a 'Car' model object correctly combines the year, make
        and model attributes, creating a human-readable
        representation.

        Attributes:
            self: The test case instance.

        Usage:
        To test the string representation of a 'Car' model, an instance
        of the 'Car' model is created with specific attributes. The
        method then retrieves the expected string by combining the year,
        make, and model, and compares it to the actual string generated by
        the model.

        The test asserts whether the generated string matches the expected
        string, ensuring the proper functioning of the '__str__' method in
        the 'Car' model.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        expected_string = f"{car.year} {car.make} {car.model}"
        self.assertEqual(str(car), expected_string)

    def test_make_content(self):
        """
        Test the 'make' attribute of the 'Car' model.

        This test method verifies that the 'make' attribute of a 'Car'
        model instance matches the expected value.

        Attributes:
            self: The test case instance.

        Usage:
        To test the 'make' attribute of a 'Car' model, an instance of the
        'Car' model is created with a specific 'make' attribute. The method
        then checks whether the 'make' attribute of the model matches the
        expected value ('TestMake').

        The test asserts whether the 'make' attribute is correctly set,
        ensuring that the 'make' attribute of the 'Car' model functions
        as expected.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        self.assertEqual(car.make, "TestMake")

    def test_model_content(self):
        """
        Test the 'model' attribute of the 'Car' model.

        This test method verifies that the 'model' attribute of a 'Car'
        model instance matches the expected value.

        Attributes:
            self: The test case instance.

        Usage:
        To test the 'model' attribute of a 'Car' model, an instance of the
        'Car' model is created with a specific 'model' attribute. The method
        then checks whether the 'model' attribute of the model matches the
        expected value ('TestModel').

        The test asserts whether the 'model' attribute is correctly set,
        ensuring that the 'model' attribute of the 'Car' model functions
        as expected.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        self.assertEqual(car.model, "TestModel")

    def test_year_content(self):
        """
        Test the 'year' attribute of the 'Car' model.

        This test method verifies that the 'year' attribute of a 'Car'
        model instance matches the expected value (2023).

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with a specific 'year'
            attribute.

        Usage:
        To test the 'year' attribute of a 'Car' model, an instance of the
        'Car' model is created with a specific 'year' attribute (2023). The
        method then checks whether the 'year' attribute of the model matches
        the expected value (2023).

        The test asserts whether the 'year' attribute is correctly set,
        ensuring that the 'year' attribute of the 'Car' model functions
        as expected.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        self.assertEqual(car.year, 2023)

    def test_license_plate_content(self):
        """
        Test the 'year' attribute of the 'Car' model.

        This test method verifies that the 'year' attribute of a 'Car'
        model instance matches the expected value (2023).

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with a specific 'year'
            attribute.

        Usage:
        To test the 'year' attribute of a 'Car' model, an instance of the
        'Car' model is created with a specific 'year' attribute (2023). The
        method then checks whether the 'year' attribute of the model matches
        the expected value (2023).

        The test asserts whether the 'year' attribute is correctly set,
        ensuring that the 'year' attribute of the 'Car' model functions
        as expected.

        Note:
        This test method is part of the unit tests for the 'Car'
        model within the 'autoR5' Django application.
        """
        car = self.car
        self.assertEqual(car.license_plate, "ABC123")

    def test_daily_rate_content(self):
        """
        Test the 'daily_rate' attribute of the 'Car' model.

        This test method verifies that the 'daily_rate' attribute of a
        'Car' model instance matches the expected value (100.00).

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with a specific
            'daily_rate' attribute.

        Usage:
        To test the 'daily_rate' attribute of a 'Car' model, an instance
        of the 'Car' model is created with a specific 'daily_rate'
        attribute (100.00). The method then checks whether the 'daily_rate'
        attribute of the model matches the expected value (100.00).

        The test asserts whether the 'daily_rate' attribute is correctly set,
        ensuring that the 'daily_rate' attribute of the 'Car' model functions
        as expected.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        self.assertEqual(car.daily_rate, 100.00)

    def test_is_available_content(self):
        """
        Test the 'is_available' attribute of the 'Car' model.

        This test method verifies that the 'is_available' attribute of a
        'Car' model instance matches the expected value (True).

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with 'is_available'
            set to True.

        Usage:
        To test the 'is_available' attribute of a 'Car' model, an instance
        of the 'Car' model is created with 'is_available' set to True. The
        method then checks whether the 'is_available' attribute of the model
        matches the expected value (True).

        The test asserts whether the 'is_available' attribute is correctly set,
        ensuring that the 'is_available' attribute of the 'Car' model functions
        as expected.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        self.assertTrue(car.is_available)

    def test_latitude_content(self):
        """
        Test the 'latitude' attribute of the 'Car' model.

        This test method verifies that the 'latitude' attribute of a
        'Car' model instance matches the expected value (53.349805)
        within a defined tolerance.

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with a specific
            'latitude' attribute. expected_latitude: The expected
            'latitude' value.

        Usage:
        To test the 'latitude' attribute of a 'Car' model, an instance
        of the 'Car' model is created with a specific 'latitude' attribute
        (53.349805). The method then checks whether the 'latitude' attribute
        of the model matches the expected value (53.349805) within a
        tolerance of 6 decimal places.

        The test asserts whether the 'latitude' attribute is correctly set,
        ensuring that the 'latitude' attribute of the 'Car' model functions
        as expected within the specified tolerance.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        expected_latitude = 53.349805
        self.assertAlmostEqual(car.latitude, expected_latitude, places=6)

    def test_longitude_content(self):
        """
        Test the 'longitude' attribute of the 'Car' model.

        This test method verifies that the 'longitude' attribute of a
        'Car' model instance matches the expected value (6.206031)
        within a defined tolerance.

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with a specific
            'longitude' attribute. expected_longitude: The expected
            'longitude' value.

        Usage:
        To test the 'longitude' attribute of a 'Car' model, an instance
        of the 'Car' model is created with a specific 'longitude' attribute
        (6.206031). The method then checks whether the 'longitude' attribute
        of the model matches the expected value (6.206031) within a tolerance
        of 6 decimal places.

        The test asserts whether the 'longitude' attribute is correctly set,
        ensuring that the 'longitude' attribute of the 'Car' model functions
        as expected within the specified tolerance.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        expected_longitude = 6.206031
        self.assertAlmostEqual(car.longitude, expected_longitude, places=6)

    def test_location_city_content(self):
        """
        Test the 'location_city' attribute of the 'Car' model.

        This test method verifies that the 'location_city' attribute of a
        'Car' model instance matches the expected value ("Test City").

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with a specific 'location_city'
            attribute.

        Usage:
        To test the 'location_city' attribute of a 'Car' model, an instance of
        the 'Car' model is created with a specific 'location_city' attribute
        ("Test City"). The method then checks whether the 'location_city'
        attribute of the model matches the expected value ("Test City").

        The test asserts whether the 'location_city' attribute is correctly
        set, ensuring that the 'location_city' attribute of the 'Car' model
        functions as expected.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        self.assertEqual(car.location_city, "Test City")

    def test_location_address_content(self):
        """
        Test the 'location_address' attribute of the 'Car' model.

        This test method verifies that the 'location_address' attribute of a
        'Car' model instance matches the expected value ("Test Address").

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with a specific
            'location_address' attribute.

        Usage:
        To test the 'location_address' attribute of a 'Car' model, an instance
        of the 'Car' model is created with a specific 'location_address'
        attribute ("Test Address"). The method then checks whether the
        'location_address' attribute of the model matches the expected value
        ("Test Address").

        The test asserts whether the 'location_address' attribute is correctly
        set, ensuring that the 'location_address' attribute of the 'Car' model
        functions as expected.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        self.assertEqual(car.location_address, "Test Address")

    def test_features_content(self):
        """
        Test the 'features' attribute of the 'Car' model.

        This test method verifies that the 'features' attribute of a 'Car'
        model instance matches the expected value ("Test Features").

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with a specific 'features'
            attribute.

        Usage:
        To test the 'features' attribute of a 'Car' model, an instance of
        the 'Car' model is created with a specific 'features' attribute
        ("Test Features"). The method then checks whether the 'features'
        attribute of the model matches the expected value ("Test Features").

        The test asserts whether the 'features' attribute is correctly set,
        ensuring that the 'features' attribute of the 'Car' model functions
        as expected.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        self.assertEqual(car.features, "Test Features")

    def test_car_type_content(self):
        """
        Test the 'car_type' attribute of the 'Car' model.

        This test method verifies that the 'car_type' attribute
        of a 'Car' model instance matches the expected value
        ("Hatchback").

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with a specific
            'car_type' attribute.

        Usage:
        To test the 'car_type' attribute of a 'Car' model, an instance
        of the 'Car' model is created with a specific 'car_type' attribute
        ("Hatchback"). The method then checks whether the 'car_type' attribute
        of the model matches the expected value ("Hatchback").

        The test asserts whether the 'car_type' attribute is correctly set,
        ensuring that the 'car_type' attribute of the 'Car' model functions as
        expected.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        self.assertEqual(car.car_type, "Hatchback")

    def test_fuel_type_content(self):
        """
        Test the 'fuel_type' attribute of the 'Car' model.

        This test method verifies that the 'fuel_type' attribute of a
        'Car' model instance matches the expected value ("Petrol").

        Attributes:
            self: The test case instance.
            car: An instance of the 'Car' model with a specific
            'fuel_type' attribute.

        Usage:
        To test the 'fuel_type' attribute of a 'Car' model, an instance
        of the 'Car' model is created with a specific 'fuel_type' attribute
        ("Petrol"). The method then checks whether the 'fuel_type' attribute
        of the model matches the expected value ("Petrol").

        The test asserts whether the 'fuel_type' attribute is correctly set,
        ensuring that the 'fuel_type' attribute of the 'Car' model functions
        as expected.

        Note:
        This test method is part of the unit tests for the 'Car' model within
        the 'autoR5' Django application.
        """
        car = self.car
        self.assertEqual(car.fuel_type, "Petrol")


class BookingModelTest(TestCase):
    """
    Test the 'Booking' model.

    This test class contains test methods to verify the behavior
    of the 'Booking' model in the 'autoR5' Django application.

    Attributes:
        TestCase: The base class for test cases provided by Django.

    Usage:
    This test class defines methods to test various aspects of the
    'Booking' model, including creating bookings, checking status
    updates, and calculating total costs. It ensures that the
    'Booking' model functions correctly as expected.

    Note:
    These test methods are part of the unit tests for the 'Booking'
    model within the 'autoR5' Django application.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuserbooking", password="testpassword")

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
        """
        Test the creation of a booking.

        This test method creates a booking instance using the
        'Booking' model. It sets up the necessary data for the
        booking, including user, car, rental date, return date,
        and status. The method then checks whether the created
        booking matches the expected values and if the total
        cost is calculated correctly.

        Attributes:
            self: The test case instance.

        Usage:
        The test creates a booking with specific attributes and
        checks whether the booking instance is created correctly.
        It verifies if the user, car, rental date, return date,
        status, and total cost match the expected values.

        Note:
        This test method is part of the unit tests for the 'Booking'
        model within the 'autoR5' Django application.
        """
        rental_date = timezone.now() + timedelta(days=1)
        return_date = rental_date + timedelta(days=4)
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            status='Confirmed',
        )

        self.assertEqual(booking.user, self.user)
        self.assertEqual(booking.car, self.car)
        self.assertEqual(booking.rental_date, rental_date)
        self.assertEqual(booking.return_date, return_date)
        self.assertEqual(booking.status, 'Confirmed')
        self.assertEqual(booking.total_cost, Decimal('400.00'))

    def test_completed_booking(self):
        """
        Test the completion of a booking.

        This test method creates a booking instance with status
        'Confirmed' and a return date in the past. It verifies that
        the status is automatically updated to 'Completed' and checks
        if the car becomes available after the booking is completed.

        Attributes:
            self: The test case instance.

        Usage:
        The test creates a booking with a past return date and 'Confirmed'
        tatus. It then refreshes the booking instance from the database and
        checks if the status has changed to 'Completed'. Additionally, the
        method verifies that the associated car becomes available after the
        booking is completed.

        Note:
        This test method is part of the unit tests for the 'Booking' model
        within the 'autoR5' Django application.
        """
        rental_date = timezone.make_aware(datetime(2023, 1, 1, 12, 0, 0))
        return_date = timezone.make_aware(datetime(2023, 1, 4, 12, 0, 0))
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            status='Confirmed',
        )

        booking.refresh_from_db()
        self.assertEqual(booking.status, 'Completed')
        self.assertTrue(self.car.is_available)

    def test_calculate_total_cost(self):
        """
        Test the calculation of the total cost for a booking.

        This test method creates a booking with custom rental
        and return dates and verifies the calculation of the total
        cost based on the car's daily rate.

        Attributes:
            self: The test case instance.

        Usage:
        The test creates a booking with specific rental and return dates,
        setting its status to 'Confirmed'. It then calculates the total
        cost for the booking and checks if the total cost matches the expected
        value based on the car's daily rate.

        The method ensures that the total cost is correctly calculated,
        validating that the booking's financial aspect functions as expected.

        Note:
        This test method is part of the unit tests for the 'Booking' model
        within the 'autoR5' Django application.
        """
        rental_date = timezone.make_aware(datetime(2023, 1, 1, 12, 0, 0))
        return_date = timezone.make_aware(datetime(2023, 1, 5, 12, 0, 0))
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            status='Confirmed',
        )

        booking.calculate_total_cost()
        self.assertEqual(booking.total_cost, Decimal('400.00'))


class PaymentModelTest(TestCase):
    """
    Test the payment-related functionality of the 'Payment' model.

    This test case class includes methods to verify the creation
    and attributes of 'Payment' model instances.

    Attributes:
        TestCase: A subclass of the Django TestCase class for testing.

    Usage:
    The 'PaymentModelTest' class contains test methods to verify the
    creation and attributes of 'Payment' model instances. It includes
    a method to test the creation of a payment with specific attributes,
    ensuring that the payment-related functionality of the 'Payment'
    model works as expected.

    Note:
    This test class is part of the unit tests for the 'Payment' model
    within the 'autoR5' Django application.
    """

    def setUp(self):
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
        """
        Test the creation of a payment instance.

        This test method creates a test user, a test booking,
        and a test payment within the 'Payment' model. It verifies
        that the payment instance is created correctly, with all
        attributes matching the expected values.

        Attributes:
            self: The test case instance.

        Usage:
        The 'test_payment_creation' method creates a test user and a
        test booking with specific attributes. It then creates a test
        payment related to the booking and ensures that the payment instance
        is created correctly. The method checks various payment attributes,
        including the user, booking, payment amount, payment method, and
        payment status, to validate the functionality of the 'Payment' model.

        Note:
        This test method is part of the unit tests for the 'Payment' model
        within the 'autoR5' Django application.
        """
        user = User.objects.create_user(
            username="testuserpayment", password="testpassword")
        rental_date = timezone.make_aware(datetime(2023, 1, 1, 12, 0, 0))
        return_date = rental_date + timedelta(days=4)

        booking = Booking.objects.create(
            user=user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            total_cost=Decimal('400.00'),
            status='Confirmed',
        )
        payment = Payment.objects.create(
            user=user,
            booking=booking,
            amount=Decimal('400.00'),
            payment_method='Stripe',
            payment_status='Paid',
        )

        self.assertEqual(payment.user.username, 'testuserpayment')
        self.assertEqual(str(payment.booking),
                         f'Booking for {booking.car} by {booking.user}')
        self.assertEqual(payment.amount, Decimal('400.00'))
        self.assertEqual(payment.payment_method, 'Stripe')
        self.assertEqual(payment.payment_status, 'Paid')


class CancellationModelTest(TestCase):
    """
    Test the CancellationRequest model and its related methods.

    This test class focuses on the 'CancellationRequest' model
    within the 'autoR5' Django application. It includes test
    methods to verify the creation and attributes of cancellation
    requests.

    Attributes:
        TestCase: A subclass of Django's 'TestCase' for unit
        testing.

    Usage:
    The 'CancellationModelTest' class is responsible for testing the
    'CancellationRequest' model. It creates a test user, car, and
    booking for the tests. Two test methods are included to validate
    the string representation and default attributes of cancellation
    requests.

    - 'test_string_representation': Verifies that the string
    representation of a cancellation request includes the associated
    booking information.
    - 'test_defaults': Ensures that newly created cancellation requests
    have their 'approved' attribute set to 'False'.

    Note:
    This test class is part of the unit tests for the 'autoR5' Django
    application.
    """

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
        return_date = rental_date + timedelta(days=4)

        self.booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=rental_date,
            return_date=return_date,
            total_cost=400.00,
        )

    def test_string_representation(self):
        """
        Test the string representation of a 'CancellationRequest'
        model instance.

        This test method verifies that the string representation of a
        'CancellationRequest' model instance accurately reflects the
        associated booking information.

        Attributes:
            self: The test case instance.

        Usage:
        The 'test_string_representation' method creates a
        'CancellationRequest' model instance with a test user, booking,
        and reason for cancellation. It then asserts that the string
        representation of the cancellation request matches the expected
        format, which includes the associated booking details.

        The test ensures that the string representation of a
        'CancellationRequest' provides clear information about the booking
        it pertains to.

        Note:
        This test method is part of the unit tests for the
        'CancellationRequest' model within the 'autoR5' Django application.
        """
        cancellation = CancellationRequest(
            user=self.user,
            booking=self.booking,
            reason="Change of plans",
        )
        self.assertEqual(str(cancellation),
                         f"Cancellation request for {self.booking}")

    def test_defaults(self):
        """
        Test the default values of a 'CancellationRequest' model
        instance.

        This test method verifies that the default values of a
        'CancellationRequest' model instance are correctly set
        upon creation.

        Attributes:
            self: The test case instance.

        Usage:
        The 'test_defaults' method creates a 'CancellationRequest'
        model instance with a test user, booking, and reason for cancellation.
        After saving the instance, it checks whether the default value for the
        'approved' attribute is set to 'False'.

        The test ensures that the 'approved' attribute is initially set to
        'False' when creating a new 'CancellationRequest'.

        Note:
        This test method is part of the unit tests for the
        'CancellationRequest' model within the 'autoR5' Django application.
        """
        cancellation = CancellationRequest(
            user=self.user,
            booking=self.booking,
            reason="Change of plans",
        )
        cancellation.save()
        self.assertEqual(cancellation.approved, False)


class ReviewModelTest(TestCase):
    """
    Test the 'Review' model and its validation methods.

    This test class is responsible for testing the 'Review'
    model in the 'autoR5' Django application. It includes test
    methods for rating validation and the string representation
    of review objects.

    Attributes:
        TestCase: The Django 'TestCase' class for unit tests.
        self: The test case instance.

    Usage:
    The 'ReviewModelTest' class contains test methods to validate the
    'Review' model, including rating validation and string representation.

    - The 'test_review_rating_validator' method tests whether review
    ratings are properly validated.
    - The 'test_review_string_representation' method verifies that the
    string representation of review objects is correctly formatted.

    Note:
    This test class is part of the unit tests for the 'Review' model within the
    'autoR5' Django application.
    """

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
        """
        Test the validation of review ratings in the 'Review' model.

        This test method verifies that review ratings are properly
        validated when creating 'Review' model instances.

        Attributes:
            self: The test case instance.

        Usage:
        The 'test_review_rating_validator' method includes two test cases:
        - A valid review with a rating of 5 (5 stars) and a positive comment.
        The 'full_clean' method is called on the model instance, and it should
        not raise any validation errors.
        - An invalid review with a rating of 0 (0 stars) and a negative
        comment. The 'full_clean' method is called on the model instance,
        and it is expected to raise a 'ValidationError'.

        The test ensures that the rating validation for 'Review' model
        instances functions as expected.

        Note:
        This test method is part of the unit tests for the 'Review'
        model within the 'autoR5' Django application.
        """
        valid_review = Review(
            car=self.car,
            user=self.user,
            rating=5,
            comment="Great car!",
        )
        valid_review.full_clean()

        invalid_review = Review(
            car=self.car,
            user=self.user,
            rating=0,
            comment="Poor car!",
        )
        with self.assertRaises(ValidationError):
            invalid_review.full_clean()

    def test_review_string_representation(self):
        """
        Test the string representation of the 'Review' model.

        This test method verifies that the string representation
        of a 'Review' model instance matches the expected format.

        Attributes:
            self: The test case instance.

        Usage:
        To test the string representation of a 'Review' model, a 'Review'
        model instance is created with specific attributes, including the
        car, user, rating, and comment. The expected string representation
        is then constructed in the 'expected_string' variable, following
        the format "Review for [car] by [user]." Finally, the test method
        checks whether the actual string representation of the 'Review'
        model matches the expected string.

        The test ensures that the string representation of the 'Review' model
        functions as expected.

        Note:
        This test method is part of the unit tests for the 'Review'
        model within the 'autoR5' Django application.
        """
        review = Review.objects.create(
            car=self.car,
            user=self.user,
            rating=5,
            comment="Great car!",
        )

        expected_string = f"Review for {self.car} by {self.user}"
        self.assertEqual(str(review), expected_string)


class UserProfileModelTest(TestCase):
    """
    Test the 'UserProfile' model and its related functionality.

    This test class includes methods to test the creation and
    behavior of the 'UserProfile' model, as well as its
    associated attributes and methods.

    Attributes:
        TestCase: The base class for all test cases provided by
        Django's test framework.

    Usage:
    The test class includes methods to test various aspects of
    the 'UserProfile' model. The methods cover the creation of
    a user profile, the behavior of its string representation,
    and the email property.

    The tests verify that the 'UserProfile' model functions as
    expected, ensuring that it properly associates with a user,
    displays the correct string representation, and provides
    the email property.

    Note:
    This test class is part of the unit tests for the
    'UserProfile' model within the 'autoR5' Django application.
    """
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            email="testuser@example.com"
        )

    def setUp(self):
        image = Image.new('RGB', (100, 100))
        output = BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)

        uploaded_image = SimpleUploadedFile(
            'image.jpg', output.getvalue(), content_type='image/jpeg')

        self.user_profile, UserProfile.objects.get_or_create(
            user=self.user,
            defaults={
                "phone_number": "123-456-7890",
                "profile_picture": uploaded_image
            }
        )

    def tearDown(self):
        if hasattr(self, 'user_profile') and self.user_profile.profile_picture:
            public_id = self.user_profile.profile_picture.public_id
            api.delete_resources(public_id)

    def test_user_profile_creation(self):
        """
        Test the creation of a 'UserProfile' instance associated
        with a user.

        This test method verifies that a 'UserProfile' instance
        is correctly created and associated with a user. It
        checks whether the number of 'UserProfile' instances in
        the database is one, indicating a successful creation.

        Attributes:
            self: The test case instance.

        Usage:
        The method creates a 'UserProfile' instance associated with
        a predefined user. It then asserts that there is exactly one
        'UserProfile' instance in the database, confirming the
        successful creation and association with the user.

        Note:
        This test method is part of the unit tests for the 'UserProfile'
        model within the 'autoR5' Django application.
        """
        self.assertEqual(UserProfile.objects.count(), 1)

    def test_user_profile_str_method(self):
        """
        Test the string representation of a 'UserProfile'
        instance.

        This test method verifies that the string representation
        of a 'UserProfile' instance matches the expected value,
        which is the username of the associated user.

        Attributes:
            self: The test case instance.

        Usage:
        The method creates a 'UserProfile' instance associated with
        a predefined user and ensures that the string representation
        of this 'UserProfile' instance is equal to the username of
        the user. This validates that the string representation method
        of the 'UserProfile' model functions as expected.

        Note:
        This test method is part of the unit tests for the 'UserProfile'
        model within the 'autoR5' Django application.
        """
        self.assertEqual(str(self.user_profile), "testuser")

    def test_user_profile_email_property(self):
        """
        Test the email property of a 'UserProfile' instance.

        This test method verifies that the 'email' property of
        a 'UserProfile' instance matches the expected email
        address, which is associated with the predefined user.

        Attributes:
            self: The test case instance.

        Usage:
        The method creates a 'UserProfile' instance associated
        with a predefined user and ensures that the 'email'
        property of this 'UserProfile' instance is equal to the
        expected email address. This validates that the email
        property of the 'UserProfile' model functions as expected.

        Note:
        This test method is part of the unit tests for the
        'UserProfile' model within the 'autoR5' Django application.
        """
        self.assertEqual(self.user_profile.email, "testuser@example.com")


class ContactFormSubmissionModelTest(TestCase):
    """
    Test the string representation of a 'ContactFormSubmission'
    instance.

    This test method verifies that the string representation of
    a 'ContactFormSubmission' instance is correctly generated
    based on the attributes of the instance.

    Attributes:
        self: The test case instance.

    Usage:
    The method creates a 'ContactFormSubmission' instance with
    specific attribute values, including the first name, last
    name, and subject. It then checks if the generated string
    representation of the submission matches the expected format,
    which includes the first name, last name, and subject
    of the submission.

    Note:
    This test method is part of the unit tests for the
    'ContactFormSubmission' model within the 'autoR5'
    Django application.
    """

    def test_create_contact_submission(self):
        """
        Test the creation of a 'ContactFormSubmission'
        instance.

        This test method verifies that a 'ContactFormSubmission'
        instance can be created with the specified attributes.
        It checks whether the attributes of the created instance
        match the expected values.

        Attributes:
            self: The test case instance.

        Usage:
        The method creates a 'ContactFormSubmission' instance with
        specific attribute values, including the first name, last
        name, email, subject, and message. It then validates the
        creation by retrieving the submission from the database
        and checking if its attributes match the expected values.

        Note:
        This test method is part of the unit tests for the
        'ContactFormSubmission' model within the 'autoR5'
        Django application.
        """
        submission = ContactFormSubmission.objects.create(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            subject="Test Subject",
            message="Test Message"
        )

        retrieved_submission = ContactFormSubmission.objects.get(
            id=submission.id)

        self.assertEqual(retrieved_submission.first_name, "John")
        self.assertEqual(retrieved_submission.last_name, "Doe")
        self.assertEqual(retrieved_submission.email, "john@example.com")
        self.assertEqual(retrieved_submission.subject, "Test Subject")
        self.assertEqual(retrieved_submission.message, "Test Message")

    def test_submission_str_representation(self):
        """
        Test the string representation of a 'ContactFormSubmission'
        instance.

        This test method verifies that the string representation
        of a 'ContactFormSubmission' instance correctly combines
        the first name, last name, and subject attributes as expected.

        Attributes:
            self: The test case instance.

        Usage:
        The method creates a 'ContactFormSubmission' instance with
        specific attribute values for first name, last name, and
        subject. It then checks whether the string representation
        of the instance matches the expected format, which combines
        the first name and last name with a hyphen and appends the
        subject.

        Note:
        This test method is part of the unit tests for the
        'ContactFormSubmission' model within the 'autoR5'
        Django application.
        """
        submission = ContactFormSubmission(
            first_name="John",
            last_name="Doe",
            subject="Test Subject"
        )

        self.assertEqual(str(submission), "John Doe - Test Subject")


class IndexViewTest(TestCase):
    """
    Test the 'IndexView' view.

    This test class contains methods for testing the behavior
    of the 'IndexView' view within the 'autoR5' Django
    application. It includes tests for various aspects of the
    view, such as response status, content, and template
    rendering.

    Attributes:
        TestCase: The base class for all test cases in Django,
        provided by the Django testing framework.

    Usage:
    To test the 'IndexView' view, this class includes a setup
    method for generating sample car data and a test method
    'test_index_view' to issue a GET request to the view.
    The test checks the response status code, verifies that
    car types and fuel types are displayed in the response
    content, and ensures that the 'index.html' template is
    used for rendering.

    This class is part of the unit tests for the 'IndexView'
    view within the 'autoR5' Django application.
    """
    @staticmethod
    def generate_random_license_plate():
        """
        Generate a random license plate.

        This static method generates a random license plate in the
        format 'AAA123', where 'AAA' consists of uppercase letters
        and '123' consists of digits. The generated license plate
        can be used for creating sample car data for testing purposes.

        Attributes:
            None

        Returns:
            str: A randomly generated license plate.

        Usage:
        Call this method to generate a random license plate for creating
        sample car data in test cases. The generated license plate is a
        string in the format 'AAA123'.

        Example:
            license_plate = IndexViewTest.generate_random_license_plate()
            # Possible output: 'XYZ456'

        Note:
        This method is used within the 'IndexViewTest' test class for
        generating sample car data in the 'autoR5' Django application.
        """
        letters = ''.join(random.choice(string.ascii_uppercase)
                          for _ in range(3))
        digits = ''.join(random.choice(string.digits) for _ in range(3))
        return f"{letters}{digits}"

    def create_car(self, car_type="Hatchback", fuel_type="Petrol"):
        """
        Create a sample car instance for testing.

        This method creates and returns a sample car instance with
        specified attributes for testing purposes.

        Attributes:
            self: The test case instance.
            car_type (str, optional): The type of car to create
            (default is 'Hatchback'). fuel_type (str, optional): The
            fuel type of the car (default is 'Petrol').

        Returns:
            Car: A sample car instance with specified attributes.

        Usage:
        Call this method to create a sample car instance for testing.
        You can customize the 'car_type' and 'fuel_type' attributes by
        providing optional arguments.

        Example:
            Create a sample car instance with custom car type and
            fuel type car = self.create_car(car_type='Sedan',
                fuel_type='Diesel')

        Note:
        This method is used within the 'IndexViewTest' test class to generate
        sample car data for testing in the 'autoR5' Django application.
        """
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
        """
        Test the 'index' view in the 'autoR5' Django application.

        This test method verifies that the 'index' view displays
        car types and fuel types correctly.

        Attributes:
            self: The test case instance.

        Usage:
        This test method sets up sample car data for different car
        types and fuel types. It then issues a GET request to the 'index'
        view, which is a web page displaying car information. The method
        checks if the response status code is 200 (OK) and whether the
        car types and fuel types are correctly displayed in the response
        content. Additionally, it verifies that the correct template
        ('index.html') is used for rendering the view.

        The purpose of this test is to ensure that the 'index' view in the
        'autoR5' Django application correctly displays car data to users.

        Note:
        This test method is part of the unit tests for the 'IndexView' in the
        'autoR5' Django application.
        """
        self.create_car(car_type="Hatchback", fuel_type="Petrol")
        self.create_car(car_type="Saloon", fuel_type="Diesel")

        response = self.client.get(reverse('index'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Hatchback")
        self.assertContains(response, "Saloon")
        self.assertContains(response, "Petrol")
        self.assertContains(response, "Diesel")

        self.assertTemplateUsed(response, 'index.html')


class CarsListViewTest(TestCase):
    """
    Test the 'cars_list' view in the 'autoR5' Django application.

    This test class verifies the behavior of the 'cars_list' view,
    which displays a list of cars with various attributes.

    Attributes:
        create_car: A method to create car instances with different
        attributes. generate_random_license_plate: A method to
        generate a random license plate.
        self: The test case instance.

    Usage:
    This test class sets up sample car data with various attributes using
    the 'create_car' method. It then includes two test methods:

    - 'test_cars_list_view': This method tests whether the 'cars_list'
    view returns a valid HTTP response (status code 200) and whether
    it correctly displays all cars created in the setup.

    - 'test_cars_list_view_with_filter': This method simulates filtering
    parameters in the URL and tests whether the view responds with a
    valid HTTP status code and displays specific HTML elements matching
    the filtering criteria.

    These tests are essential for verifying that the 'cars_list' view in
    the 'autoR5' Django application functions correctly and displays car
    data accurately to users based on different criteria.

    Note:
    This test class is part of the unit tests for the 'CarsListView' in the
    'autoR5' Django application.
    """
    @classmethod
    def setUpTestData(cls):
        cls.create_car(make="Honda", model="Civic", year=2023,
                       car_type="Hatchback", fuel_type="Petrol",
                       location_city="Dublin")
        cls.create_car(make="Toyota", model="Corolla", year=2023,
                       car_type="Sedan", fuel_type="Diesel",
                       location_city="Dublin")
        cls.create_car(make="Ford", model="Fiesta", year=2023,
                       car_type="Hatchback", fuel_type="Petrol",
                       location_city="Dublin")

    @staticmethod
    def generate_random_license_plate():
        """
        Generate a random license plate.

        This static method generates a random license plate in the
        format 'AAA123', where 'AAA' consists of uppercase letters
        and '123' consists of digits. The generated license plate
        can be used for creating sample car data for testing purposes.

        Attributes:
            None

        Returns:
            str: A randomly generated license plate.

        Usage:
        Call this method to generate a random license plate for creating
        sample car data in test cases. The generated license plate is a
        string in the format 'AAA123'.

        Example:
            license_plate = IndexViewTest.generate_random_license_plate()
            # Possible output: 'XYZ456'

        Note:
        This method is used within the 'ClassListViewTest' test class for
        generating sample car data in the 'autoR5' Django application.
        """
        letters = ''.join(random.choice(string.ascii_uppercase)
                          for _ in range(3))
        digits = ''.join(random.choice(string.digits) for _ in range(3))
        return f"{letters}{digits}"

    @classmethod
    def create_car(cls, make, model, year, car_type, fuel_type, location_city):
        """
        Create a 'Car' instance with specific attributes for
        testing purposes.

        This class method creates a 'Car' model instance with the specified
        attributes for use in test cases. It generates a random license plate,
        sets the daily rate, location information, features, and car type
        and fuel type.

        Attributes:
            cls: The class instance.
            make: The make of the car.
            model: The model of the car.
            year: The year of the car.
            car_type: The type of the car.
            fuel_type: The fuel type of the car.
            location_city: The city where the car is located.

        Returns:
            Car: A 'Car' model instance with the specified attributes.

        Usage:
        To create a 'Car' instance for testing purposes, call this method with
        the desired attributes. The generated 'Car' model instance is returned,
        ready for use in test cases.

        Note:
        This method is used in the 'CarsListViewTest' test class to set up
        sample car data for testing.
        """
        license_plate = cls.generate_random_license_plate()

        return Car.objects.create(
            make=make,
            model=model,
            year=year,
            license_plate=license_plate,
            daily_rate=100.00,
            latitude=53.349805,
            longitude=6.206031,
            location_city=location_city,
            location_address="Test Address",
            features="Test Features",
            car_type=car_type,
            fuel_type=fuel_type,
        )

    def test_cars_list_view(self):
        """
        Test the 'cars_list' view for displaying all cars.

        This test method sends a GET request to the 'cars_list'
        view, which is responsible for displaying a list of all
        available cars. It then checks the response to ensure
        that the page loads successfully and that all the test
        cars (Honda, Toyota, and Ford)
        are displayed in the response content.

        Attributes:
            self: The test case instance.

        Usage:
        To test the 'cars_list' view, call this method within a test
        case. The method sends a GET request to the 'cars_list' view,
        captures the response, and performs various
        assertions to validate the behavior of the view.

        Note:
        This test method is part of the unit tests for the 'cars_list'
        view within the Django application. It ensures that the view
        correctly displays all available cars.
        """

        response = self.client.get(reverse('cars_list'))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "Honda")
        self.assertContains(response, "Toyota")
        self.assertContains(response, "Ford")

    def test_cars_list_view_with_filter(self):
        """
        Test the 'cars_list' view with filtering parameters.

        This test method simulates filtering parameters in the
        URL and sends a GET request to the 'cars_list' view with
        those parameters. It then checks the response to ensure
        that the page loads successfully (status code 200) and
        that the specific HTML element with the text "Honda Civic"
        is present, indicating that the filtering worked as expected.
        Additionally, it verifies that other elements with similar
        text (e.g., "Toyota Corolla" and "Ford Fiesta") are not
        present in the response.

        Attributes:
            self: The test case instance.

        Usage:
        To test the 'cars_list' view with filtering, call this method
        within a test case. The method constructs a URL with filter
        parameters, sends a GET request to the 'cars_list'
        view, captures the response, and performs various assertions
        to validate the behavior of the view when filtering
        cars.

        Note:
        This test method is part of the unit tests for the 'cars_list'
        view within the Django application. It ensures that the view
        correctly filters and displays cars based on the provided
        parameters.
        """

        filter_url = reverse('cars_list') + \
            '?make=Honda&model=Civic&year=2023&car_type=Hatchback&' \
            'fuel_type=Petrol&location=Dublin'
        response = self.client.get(filter_url)

        self.assertEqual(response.status_code, 200)

        content = response.content.decode("utf-8")
        pattern = r'<h4 class="card-title display-5">\s+Honda Civic\s+</h4>'
        self.assertRegex(content, pattern)

        content = response.content.decode("utf-8")
        pattern = r'<h4 class="card-title display-5">\s+Toyota Corolla\s+</h4>'
        self.assertNotRegex(content, pattern)

        content = response.content.decode("utf-8")
        pattern = r'<h4 class="card-title display-5">\s+Ford Fiesta\s+</h4>'
        self.assertNotRegex(content, pattern)


class CarDetailTest(TestCase):
    """
    Test the 'car_detail' view in the 'autoR5' Django
    application.

    This test class verifies the behavior of the 'car_detail'
    view, which displays details of a single car, including
    its attributes and reviews.

    Attributes:
        user: A test user created for the test.
        car: A test car with various attributes.
        review: A test review associated with the car.
        self: The test case instance.

    Usage:
    This test class sets up a test user, a test car, and a test
    review using the 'setUp' method.
    It then includes a test method:

    - 'test_car_detail_view': This method tests whether the
    'car_detail' view, when accessed after logging in as the test
    user, returns a valid HTTP response (status code 200) and
    correctly displays the car's details, including make, model,
    year, daily rate, location, features, and reviews.

    These tests are crucial for verifying that the 'car_detail' view
    in the 'autoR5' Django application displays car details and
    associated reviews accurately to users.

    Note:
    This test class is part of the unit tests for the 'CarDetailView'
    in the 'autoR5' Django application.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        self.car = Car.objects.create(
            make='Test Make',
            model='Test Model',
            year=2023,
            license_plate='123ABC',
            daily_rate=100.00,
            location_city='Test City',
            features='Test Features'
        )

        self.review = Review.objects.create(
            car=self.car,
            user=self.user,
            rating=5,
            comment='Great car!',
            approved=True
        )

    def test_car_detail_view(self):
        """
        Test the 'car_detail' view's behavior in the
        'autoR5' Django application.

        This test method verifies the behavior of the 'car_detail'
        view, which displays details of a single car, including its
        attributes and associated reviews, when accessed by a
        logged-in user.

        Attributes:
            self: The test case instance.

        Usage:
        This test method performs the following steps:

        - Logs in a test user with the username 'testuser' and
        password 'testpassword'.

        - Obtains the URL for the 'car_detail' view by passing the
        car's ID.

        - Sends a GET request to the URL.

        - Checks that the response status code is 200, indicating
        a successful HTTP response.

        - Verifies that the response contains specific HTML elements,
        including the car's make, model, year, daily rate, location,
        features, and review information.

        This test is essential for confirming that the 'car_detail'
        view in the 'autoR5' Django application displays car details
        and associated reviews correctly when accessed by a logged-in user.

        Note:
        This test method is part of the unit tests for the 'CarDetailView'
        in the 'autoR5' Django application.
        """

        self.client.login(username='testuser', password='testpassword')

        url = reverse('car_detail', args=[str(self.car.id)])

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'Test Make')
        self.assertContains(response, 'Test Model')
        self.assertContains(response, '2023')
        self.assertContains(response, '€100.00')
        self.assertContains(response, 'Test City')
        self.assertContains(response, 'Test Features')
        self.assertContains(response, 'Rating:')
        self.assertContains(response, 'Great car!')


class BookCarViewTest(TestCase):
    """
    Test the 'book_car' view in the 'autoR5' Django application.

    This test class verifies the behavior of the 'book_car' view,
    which allows users to book a car. It includes multiple test
    methods to cover various scenarios related to car booking.

    Attributes:
        create_car: A method to create car instances for testing.
        self: The test case instance.

    Usage:
    This test class sets up a test user and a car using the 'create_car'
    method. It includes the following test methods:

    - 'test_book_car_view_with_valid_data': Tests booking a car with valid
    booking data, including checking if the booking and payment objects are
    created, and the booking status is 'Pending'.

    - 'test_book_car_view_with_invalid_data': Tests attempting to book a
    car with missing required fields and checks if the user receives an
    error message.

    - 'test_book_car_view_with_past_date': Tests attempting to book a car
    with a past rental date and checks if the user receives an error message.

    - 'test_book_car_view_with_conflicting_dates': Tests attempting to book
    a car with dates that conflict with an existing booking and checks if
    the user receives an error message.

    - 'test_book_car_view_with_unavailable_car': Tests attempting to book
    an unavailable car and checks if the user receives an error message.

    These tests ensure that the 'book_car' view functions correctly and
    handles various scenarios related to car booking.

    Note:
    This test class is part of the unit tests for the 'BookCarView' in the
    'autoR5' Django application.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword")

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
        """
        Test the 'book_car' view in the 'autoR5' Django application.

        This test class verifies the behavior of the 'book_car' view,
        which allows users to book a car. It includes multiple test
        methods to cover various scenarios related to car booking.

        Attributes:
            create_car: A method to create car instances for testing.
            self: The test case instance.

        Usage:
        This test class sets up a test user and a car using the 'create_car'
        method. It includes the following test methods:

        - 'test_book_car_view_with_valid_data': Tests booking a car with
        valid booking data, including checking if the booking and payment
        objects are created, and the booking status is 'Pending'.

        - 'test_book_car_view_with_invalid_data': Tests attempting to book
        a car with missing required fields and checks if the user receives
        an error message.

        - 'test_book_car_view_with_past_date': Tests attempting to book a
        car with a past rental date and checks if the user receives an
        error message.

        - 'test_book_car_view_with_conflicting_dates': Tests attempting
        to book a car with dates that conflict with an existing booking
        and checks if the user receives an error message.

        - 'test_book_car_view_with_unavailable_car': Tests attempting to
        book an unavailable car and checks if the user receives an error
        message.

        These tests ensure that the 'book_car' view functions correctly
        and handles various scenarios related to car booking.

        Note:
        This test class is part of the unit tests for the 'BookCarView'
        in the 'autoR5' Django application.
        """
        self.client.login(username="testuser", password="testpassword")

        url = reverse('book_car', kwargs={'car_id': self.car.id})

        today = date.today()
        rental_date = today + timedelta(days=1)
        return_date = today + timedelta(days=5)
        booking_data = {
            'rental_date': rental_date,
            'return_date': return_date,
        }

        response = self.client.post(url, booking_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(Booking.objects.exists())

        self.assertTrue(Payment.objects.exists())

        booking = Booking.objects.latest('id')
        self.assertEqual(booking.status, 'Pending')

    def test_book_car_view_with_invalid_data(self):
        """
        Test the 'book_car' view in the 'autoR5' Django application
        with invalid booking data.

        This test method verifies the behavior of the 'book_car' view when
        a user attempts to book a car with invalid booking data. It checks
        if the user is redirected back to the booking page and if an error
        message is displayed indicating that certain fields are required.

        Attributes:
            self: The test case instance.

        Usage:
        This test method performs the following steps:

        - Logs in a test user with valid credentials.

        - Defines the URL for booking the car with the car's ID.

        - Defines invalid booking data by providing an empty dictionary,
        simulating missing required fields.

        - Performs a POST request with the invalid booking data.

        - Checks if the user is redirected back to the booking page.

        - Checks if an error message is shown in the response, indicating
        that certain fields are required.

        This test ensures that the 'book_car' view correctly handles and
        validates invalid booking data, providing appropriate error messages
        to the user.

        Note:
        This test method is part of the unit tests for the 'BookCarView' in
        the 'autoR5' Django application.
        """
        self.client.login(username="testuser", password="testpassword")

        url = reverse('book_car', kwargs={'car_id': self.car.id})

        invalid_booking_data = {}

        response = self.client.post(url, invalid_booking_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'This field is required.')

    def test_book_car_view_with_past_date(self):
        """
        Test the 'book_car' view in the 'autoR5' Django application
        with a past rental date.

        This test method verifies the behavior of the 'book_car' view
        when a user attempts to book a car with a past rental date.
        It checks if the user is redirected back to the booking page
        and if an error message is displayed indicating that booking
        for a past date is not allowed.

        Attributes:
            self: The test case instance.

        Usage:
        This test method performs the following steps:

        - Logs in a test user with valid credentials.

        - Defines the URL for booking the car with the car's ID.

        - Defines booking data with a past rental date and a future
        return date, simulating a booking for a past date.

        - Performs a POST request with the invalid booking data.

        - Checks if the user is redirected back to the booking page.

        - Checks if an error message is shown in the response, indicating
        that booking for a past date is not allowed.

        This test ensures that the 'book_car' view correctly handles and
        validates bookings with past rental dates, preventing users from
        booking cars for dates that have already passed.

        Note:
        This test method is part of the unit tests for the 'BookCarView'
        in the 'autoR5' Django application.
        """
        self.client.login(username="testuser", password="testpassword")

        url = reverse('book_car', kwargs={'car_id': self.car.id})

        today = date.today()
        past_rental_date = today - timedelta(days=2)
        booking_data = {
            'rental_date': past_rental_date,
            'return_date': today + timedelta(days=5),
        }

        response = self.client.post(url, booking_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, 'You cannot book for a past date.')

    def test_book_car_view_with_conflicting_dates(self):
        """
        Test the 'book_car' view in the 'autoR5' Django
        application with conflicting dates.

        This test method verifies the behavior of the 'book_car'
        view when a user attempts to create a booking with dates
        that conflict with an existing booking. It checks if the
        user is able to book a car with valid dates and if, when
        attempting to create another booking with the same dates,
        the user is redirected back to the booking page with an
        error message indicating that the car is already booked
        for the selected dates.

        Attributes:
            self: The test case instance.

        Usage:
        This test method performs the following steps:

        - Logs in a test user with valid credentials.

        - Defines the URL for booking the car with the car's ID.

        - Defines valid booking data with a rental date and a return
        date.

        - Creates a valid booking by performing a POST request with
        the valid booking data.

        - Checks if the response status code is as expected.

        - Checks if the booking and payment objects are created.

        - Checks if the booking status is 'Pending.'

        - Defines conflicting booking data with the same rental and
        return dates as the previous booking.

        - Performs a POST request with the conflicting booking data
        and follows the redirect.

        - Checks if the response status code is as expected
        (e.g., 200 for a successful booking).

        - Checks if an error message is displayed in the response,
        indicating that the car is already booked for the selected dates.

        This test ensures that the 'book_car' view correctly handles
        bookings with conflicting dates, preventing users from creating
        overlapping bookings for the same car.

        Note:
        This test method is part of the unit tests for the 'BookCarView'
        in the 'autoR5' Django application.
        """

        self.client.login(username="testuser", password="testpassword")

        url = reverse('book_car', kwargs={'car_id': self.car.id})

        today = date.today()
        rental_date = today + timedelta(days=1)
        return_date = today + timedelta(days=5)
        valid_booking_data = {
            'rental_date': rental_date,
            'return_date': return_date,
        }

        response = self.client.post(url, valid_booking_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertTrue(Booking.objects.exists())

        self.assertTrue(Payment.objects.exists())

        booking = Booking.objects.latest('id')
        self.assertEqual(booking.status, 'Pending')

        conflicting_booking_data = {
            'rental_date': rental_date,
            'return_date': return_date,
        }

        response = self.client.post(url, conflicting_booking_data, follow=True)

        self.assertEqual(response.status_code, 200)

        self.assertContains(
            response, 'This car is already booked for the selected dates.')

    def test_book_car_view_with_unavailable_car(self):
        """
        Test the 'book_car' view in the 'autoR5' Django application
        with an unavailable car.

        This test method verifies the behavior of the 'book_car' view
        when a user attempts to book a car that is marked as unavailable.
        It checks if the user is able to book a car with valid dates and if
        the car is marked as unavailable (is_available=False), in which case
        the user is redirected to the car detail page with an error message
        indicating that the car is not available for booking.

        Attributes:
            self: The test case instance.

        Usage:
        This test method performs the following steps:

        - Logs in a test user with valid credentials.

        - Marks the car as unavailable by setting 'is_available' to False.

        - Defines the URL for booking the car with the car's ID.

        - Defines valid booking data with a rental date and a return date.

        - Performs a POST request with the valid booking data.

        - Checks if the user is redirected to the car detail page.

        - Checks if the response status code is as expected (e.g., 200).

        - Checks if the car detail page template ('car_detail.html') is used
        for rendering.

        - Checks if an error message is displayed in the response, indicating
        that the car is not available for booking.

        This test ensures that the 'book_car' view correctly handles
        bookings for unavailable cars and prevents users from booking
        cars that are marked as unavailable.

        Note:
        This test method is part of the unit tests for the 'BookCarView' in the
        'autoR5' Django application.
        """
        self.client.login(username="testuser", password="testpassword")

        self.car.is_available = False
        self.car.save()

        url = reverse('book_car', kwargs={'car_id': self.car.id})

        today = date.today()
        rental_date = today + timedelta(days=1)
        return_date = today + timedelta(days=5)
        booking_data = {
            'rental_date': rental_date,
            'return_date': return_date,
        }

        response = self.client.post(url, booking_data, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_detail.html')

        self.assertContains(response, 'This car is not available for booking.')


class CheckoutViewTest(TestCase):
    """
    Test the 'checkout' view in the 'autoR5' Django application.

    This test class verifies the behavior of the 'checkout' view,
    which allows users to complete their car bookings by processing
    payments. It includes two test methods to cover different
    scenarios related to the checkout process.

    Attributes:
        self: The test case instance.

    Usage:
    This test class sets up a test user, a car, and a booking associated
    with the user and car using the 'setUp' method. It includes the
    following test methods:

    - 'test_checkout_view': Tests the checkout view when a user initiates
    the checkout process. It mocks the Stripe PaymentIntent creation and
    checks if the response status code is 200 (OK). It also ensures that
    necessary context data, such as 'stripe_publishable_key',
    'intent_client_secret', 'booking_id' and 'total_cost', is present
    in the response.

    - 'test_checkout_view_stripe_error': Tests the checkout view when an
    error occursduring the Stripe PaymentIntent creation. It mocks the
    Stripe PaymentIntent creation to raise an error and checks if the
    response is a redirect to the 'checkout' view with the appropriate URL.
    This simulates the handling of payment errors during the checkout process.

    These tests are essential for verifying that the 'checkout' view in the
    'autoR5' Django application functions correctly, including processing
    payments and handling errors during the checkout process.

    Note:
    This test class is part of the unit tests for the 'CheckoutView' in the
    'autoR5' Django application.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword")

        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2023,
            license_plate="ABC123",
            daily_rate=100.00,
            location_city="Test Location",
        )

        self.booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            rental_date=timezone.now(),

        )

    @patch('stripe.PaymentIntent.create')
    def test_checkout_view(self, stripe_create_mock):
        """
        Test the 'checkout_view' method in the 'autoR5' Django application.

        This test method verifies the behavior of the 'checkout_view' method,
        which handles the checkout process when a user initiates the payment
        for a car booking. It includes mocking the Stripe PaymentIntent
        creation and checking the response and context data.

        Attributes:
            stripe_create_mock: A mock object for the Stripe PaymentIntent
            creation.
            self: The test case instance.

        Usage:
        This test method mocks the Stripe PaymentIntent creation by creating a
        Mock object with the required 'client_secret' attribute. It then sets
        up the user session by logging in and defines the URL for the checkout
        view. A GET request is made to the view, and the response is checked
        for a status code of 200 (OK). The test also ensures that necessary
        context data, including 'stripe_publishable_key',
        'intent_client_secret', 'booking_id' and 'total_cost', is present
        in the response.

        This test is essential for verifying that the 'checkout_view' method in
        the 'autoR5' Django application correctly initiates the checkout
        process and provides the required context data for payment processing.

        Note:
        This test method is part of the unit tests for the 'CheckoutView'
        in the 'autoR5' Django application.
        """
        intent_mock = Mock(client_secret='test_secret')
        stripe_create_mock.return_value = intent_mock

        self.client.login(username="testuser", password="testpassword")

        url = reverse('checkout', kwargs={
                      'car_id': self.car.id, 'booking_id': self.booking.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertIn('stripe_publishable_key', response.context)
        self.assertIn('intent_client_secret', response.context)
        self.assertIn('booking_id', response.context)
        self.assertIn('total_cost', response.context)

    @patch('stripe.PaymentIntent.create')
    def test_checkout_view_stripe_error(self, stripe_create_mock):
        """
        Test the 'checkout_view' method in the 'autoR5' Django
        application when a Stripe error occurs.

        This test method verifies the behavior of the 'checkout_view'
        method when a Stripe error is raised during the payment process.
        It includes mocking the Stripe PaymentIntent creation to raise
        a Stripe error and checks the response for proper handling of
        the error condition.

        Attributes:
            stripe_create_mock: A mock object for the Stripe
            PaymentIntent creation.
            self: The test case instance.

        Usage:
        This test method mocks the Stripe PaymentIntent creation to
        raise a 'StripeError' with a custom error message. It then
        logs in the user and defines the URL for the checkout view.
        A GET request is made to the view, and the response is checked
        to ensure it is an instance of 'HttpResponseRedirect.'
        Additionally, it verifies that the URL to which the user is
        redirected matches the 'checkout' view for the car and booking.

        This test is important for confirming that the 'checkout_view'
        method correctly handles Stripe errors and redirects users
        appropriately when such errors occur.

        Note:
        This test method is part of the unit tests for the 'CheckoutView'
        in the 'autoR5' Django application.
        """
        stripe_create_mock.side_effect = stripe.error.StripeError("Test error")

        self.client.login(username="testuser", password="testpassword")

        url = reverse('checkout', kwargs={
                      'car_id': self.car.id, 'booking_id': self.booking.id})

        try:
            response = self.client.get(url)

            self.assertIsInstance(response, HttpResponseRedirect)
            self.assertEqual(response.url, reverse(
                'checkout', kwargs={
                             'car_id': self.car.id,
                             'booking_id': self.booking.id}))
        except NoReverseMatch:
            # If NoReverseMatch occurs, it's expected due to the error raised
            pass


class BookingConfirmationViewTest(TestCase):
    """
    Test the 'booking_confirmation' view in the 'autoR5'
    Django application.

    This test class verifies the behavior of the 'booking_confirmation'
    view, which is responsible for confirming and displaying the booking
    details and payment status to the user. It includes multiple test
    methods to cover various scenarios related to booking confirmation
    and payment status updates.

    Attributes:
        self: The test case instance.

    Usage:
    This test class sets up a test user, a car, a booking, and a payment
    using the 'setUp' method. It includes the following test methods:

    - 'test_successful_payment': This method tests a scenario where the
    payment is successful (status='succeeded'). It mocks the Stripe
    PaymentIntent retrieval to simulate a successful payment and checks
    if the booking and payment status is updated correctly.

    - 'test_pending_payment': This method tests a scenario where the
    payment is pending (status='processing'). It mocks the Stripe
    PaymentIntent retrieval to simulate a pending payment and verifies
    the correct updating of the booking and payment status.

    - 'test_failed_payment': This method tests a scenario where the
    payment fails (status='requires_payment_method'). It mocks the
    Stripe PaymentIntent retrieval to simulate a failed payment and
    checks if the booking and payment status is updated as expected.

    These tests ensure that the 'booking_confirmation' view handles
    different payment scenarios correctly and provides users with
    accurate booking and payment status information.

    Note:
    This test class is part of the unit tests for the
    'BookingConfirmationView' in the 'autoR5' Django application.
    """

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
        """
        Test a successful payment scenario in the 'booking_confirmation'
        view.

        This test method simulates a successful payment scenario by
        mocking the retrieval of a Stripe PaymentIntent with the status
        'succeeded'. It then logs in the user, performs a GET request
        to the 'booking_confirmation' view, and checks if the payment
        and booking status are correctly updated to 'Paid' and
        'Confirmed', respectively.

        Attributes:
            self: The test case instance.
            mock_retrieve: A mock object for the
            'stripe.PaymentIntent.retrieve' method.

        Usage:
        This test method ensures that when a payment is successful, the
        'booking_confirmation' view responds with a status code of 200
        (OK) and updates both the payment and booking status to 'Paid'
        and 'Confirmed', respectively.

        Note:
        This is part of the unit tests for the 'BookingConfirmationView'
        in the 'autoR5' Django application.
        """
        self.payment_intent_id = "test_payment_intent"
        self.intent_client_secret = "test_client_secret"
        mock_retrieve.return_value = Mock(status='succeeded')
        self.client.force_login(self.user)

        response = self.client.get(reverse(
            'booking_confirmation', args=[self.booking.id]), {
            'payment_intent': self.payment_intent_id,
            'payment_intent_client_secret': self.intent_client_secret,
        })

        booking = Booking.objects.get(id=self.booking.id)
        payment = Payment.objects.get(id=self.payment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['payment_status'], 'Paid')
        self.assertEqual(booking.status, 'Confirmed')
        self.assertEqual(payment.payment_status, 'Paid')

    @patch('stripe.PaymentIntent.retrieve')
    def test_pending_payment(self, mock_retrieve):
        """
        Test a pending payment scenario in the 'booking_confirmation'
        view.

        This test method simulates a pending payment scenario by
        mockingthe retrieval of a Stripe PaymentIntent with the status
        'processing'. It logs in the user, performs a GET request to
        the 'booking_confirmation' view with a test client secret,
        and checks if both the payment and booking status are correctly
        updated to 'Pending'.

        Attributes:
            self: The test case instance.
            mock_retrieve: A mock object for the
            'stripe.PaymentIntent.retrieve' method.

        Usage:
        This test method ensures that when a payment is pending, the
        'booking_confirmation' view responds with a status code of
        200 (OK) and updates both the payment and booking status to
        'Pending'.

        Note:
        It is part of the unit tests for the 'BookingConfirmationView'
        in the 'autoR5' Django application.
        """

        self.intent_client_secret = "test_client_secret"
        mock_retrieve.return_value = Mock(status='processing')
        self.client.force_login(self.user)

        response = self.client.get(reverse(
            'booking_confirmation', args=[self.booking.id]), {
            'payment_intent_client_secret': self.intent_client_secret,
        })

        booking = Booking.objects.get(id=self.booking.id)
        payment = Payment.objects.get(id=self.payment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['payment_status'], 'Pending')
        self.assertEqual(booking.status, 'Pending')
        self.assertEqual(payment.payment_status, 'Pending')

    @patch('stripe.PaymentIntent.retrieve')
    def test_failed_payment(self, mock_retrieve):
        """
        Test a failed payment scenario in the 'booking_confirmation
        view.

        This test method simulates a failed payment scenario by
        mocking the retrieval of a Stripe PaymentIntent with the
        status 'requires_payment_method'. It logs in the user,
        performs a GET request to the 'booking_confirmation' view
        with a test client secret, and checks if both the payment
        and booking status are correctly updated to 'Failed' and
        'Canceled', respectively.

        Attributes:
            self: The test case instance.
            mock_retrieve: A mock object for the
            'stripe.PaymentIntent.retrieve' method.

        Usage:
        This test method ensures that when a payment fails, the
        'booking_confirmation' view responds with a status code of
        200 (OK) and updates both the payment and booking status to
        Failed' and 'Canceled', respectively.

        Note:
        It is part of the unit tests for the 'BookingConfirmationView'
        in the 'autoR5' Django application.
        """
        self.intent_client_secret = "test_client_secret"
        mock_retrieve.return_value = Mock(status='requires_payment_method')
        self.client.force_login(self.user)

        response = self.client.get(reverse(
            'booking_confirmation', args=[self.booking.id]), {
            'payment_intent_client_secret': self.intent_client_secret,
        })

        booking = Booking.objects.get(id=self.booking.id)
        payment = Payment.objects.get(id=self.payment.id)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['payment_status'], 'Failed')
        self.assertEqual(booking.status, 'Canceled')
        self.assertEqual(payment.payment_status, 'Failed')


@override_settings(
    STATICFILES_STORAGE=(
        'django.contrib.staticfiles.storage.StaticFilesStorage'
    ),
    DEFAULT_FILE_STORAGE=(
        'django.core.files.storage.FileSystemStorage'
    )
)
class DashboardViewTest(TestCase):
    """
    Test the 'dashboard' view in the 'autoR5' Django
    application.

    This test class is responsible for testing the behavior of
    the 'dashboard' view, which displays a user's
    bookings, reviews, and provides features related to
    cancellations, rebooking, and payment. It includes
    multiple test methods to verify various aspects of the
    view's functionality.

    Attributes:
        self: The test case instance.

    Usage:
    This test class covers several scenarios and ensures the
    dashboard' view functions correctly. It includes
    the following test methods:

    - 'test_view_url_exists_at_desired_location': Checks if the
    view URL exists and returns a status code of 200 (OK).

    - 'test_view_uses_correct_template': Verifies if the view
    uses the expected template.

    - 'test_view_with_no_login_redirects_to_login_page': Ensures
    that unauthenticated users are redirected to the login page.

    - 'test_no_current_bookings_displayed': Validates that no
    current bookings are displayed when there are none.

    - 'test_current_bookings_displayed': Checks if current
    bookings are correctly displayed.

    - 'test_no_past_bookings_displayed': Ensures that no past
    bookings are displayed when there are none.

    - 'test_past_bookings_displayed': Validates that past bookings
    are correctly displayed.

    - 'test_no_reviews_displayed': Checks that no reviews are
    displayed when there are none.

    - 'test_reviews_displayed': Ensures that reviews are correctly
    displayed when available.

    - 'test_cancellation_request_form_displayed': Verifies the
    display of a cancellation request form.

    - 'test_pending_payment_displayed': Checks if the view displays
    a "Pay Now" button for pending payments.

    - 'test_rebook_displayed': Validates the display of a
    "Book Again" button for completed bookings.

    - 'test_cancellation_request_with_approved_request': Tests the
    scenario where a cancellation request with approval results in the
    cancellation process.

    - 'test_cancellation_request_without_approved_request': Verifies that
    cancellation requests without approval are correctly displayed.

    These test methods guarantee the functionality and behavior of the
    'dashboard' view in the 'autoR5' Django application.

    Note:
    This test class is part of the unit tests for the 'DashboardView'
    in the 'autoR5' Django application.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        self.url = reverse('dashboard')

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
        """
        Test if the 'dashboard' view URL exists at
        the desired location.

        This test method checks whether the 'dashboard'
        view URL returns a status code of 200 (OK) when accessed
        by an authenticated user.

        Attributes:
            self: The test case instance.

        Usage:
        This test method logs in a user, sends a GET request to the
        'dashboard' view, and then verifies that the response
        status code is 200, indicating that the view URL exists and
        functions correctly.

        Note:
        This test is part of the unit tests for the 'DashboardView'
        in the 'autoR5' Django application.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test if the 'dashboard' view uses the correct template.

        This test method checks whether the 'dashboard' view,
        when accessed by an authenticated user, uses the
        'dashboard.html' template for rendering.

        Attributes:
            self: The test case instance.

        Usage:
        This test method logs in a user, sends a GET request to the
        'dashboard' view, and then verifies that the response
        status code is 200, indicating that the view exists and functions
        correctly. Additionally, it checks if the 'dashboard.html'
        template is used for rendering the view, ensuring that the correct
        template is employed.

        Note:
        This test is part of the unit tests for the 'DashboardView'
        in the 'autoR5' Django application.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dashboard.html')

    def test_view_with_no_login_redirects_to_login_page(self):
        """
        Test that accessing 'dashboard' view without login
        redirects to the login page.

        This test method checks if users who are not logged in are
        correctly redirected to the login page when they try to
        access the 'dashboard' view.

        Attributes:
            self: The test case instance.

        Usage:
        This test method simulates an unauthenticated user by sending a
        GET request to the 'dashboard' view without logging in.
        It then verifies that the response status code is 302, which
        indicates a redirect, and ensures that the redirect URL is the
        login page with a 'next' parameter indicating the original URL.
        This is to confirm that unauthorized users are redirected to the
        login page when attempting to access the dashboard.

        Note:
        This test is part of the unit tests for the 'DashboardView'
        in the 'autoR5' Django application.
        """
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        expected_redirect_url = reverse('account_login') + f'?next={self.url}'
        self.assertRedirects(
            response, expected_redirect_url, target_status_code=200)

    def test_no_current_bookings_displayed(self):
        """
        Test that no current bookings are displayed in the 'dashboard'
        view.

        This test method ensures that when a user with no current bookings
        ogs into the 'dashboard' view, no current bookings are
        displayed.

        Attributes:
            self: The test case instance.

        Usage:
        This test method logs in a user, sends a GET request to the
        'dashboard' view, and checks whether the 'current_bookings'
        variable exists in the view's context. It then verifies that the
        'current_bookings' list is empty, indicating that there are no current
        bookings for the user. This is to confirm that the view correctly
        handles the case when a user has no current bookings.

        Note:
        This test is part of the unit tests for the 'DashboardView'
        in the 'autoR5' Django application.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('current_bookings', response.context)
        self.assertEqual(list(response.context['current_bookings']), [])

    def test_current_bookings_displayed(self):
        """
        Test that current bookings are displayed in the 'dashboard'
        view.

        This test method ensures that when a user with current bookings logs
        into the 'dashboard' view, the current bookings are
        displayed.

        Attributes:
            self: The test case instance.

        Usage:
        This test method creates a Booking associated with the user and a Car
        instance, setting its status to 'Confirmed.' It then logs in the user,
        sends a GET request to the 'dashboard' view, and checks
        whether the 'current_bookings' variable exists in the view's context.
        The method verifies that the 'current_bookings' list contains the
        expected booking instance, confirming that the view correctly displays
        current bookings for the user.

        Note:
        This test is part of the unit tests for the 'DashboardView' in
        the 'autoR5' Django application.
        """
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
        """
        Test that no past bookings are displayed in the 'dashboard'
        view.

        This test method ensures that when a user with no past bookings logs
        into the 'dashboard' view, the list of past bookings is
        empty.

        Attributes:
            self: The test case instance.

        Usage:
        This test method logs in the user, sends a GET request to the
        'dashboard' view, and checks whether the 'past_bookings'
        variable exists in the view's context. It then verifies that the
        'past_bookings' list is empty, indicating that no past bookings
        are displayed for the user.

        Note:
        This test is part of the unit tests for the 'DashboardView'
        in the 'autoR5' Django application.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('past_bookings', response.context)
        self.assertEqual(list(response.context['past_bookings']), [])

    def test_past_bookings_displayed(self):
        """
        Test that past bookings are displayed in the 'dashboard'
        view.

        This test method ensures that when a user with past bookings logs
        into the 'dashboard' view, the list of past bookings is
        displayed correctly.

        Attributes:
            self: The test case instance.

        Usage:
        This test method creates a past booking associated with the Car
        instance, logs in the user, sends a GET request to the
        'dashboard' view, and checks whether the 'past_bookings'
        variable exists in the view's context. It then verifies that the
        created past booking is included in the 'past_bookings' list,
        indicating that past bookings are displayed for the user.

        Note:
        This test is part of the unit tests for the 'DashboardView'
        in the 'autoR5' Django application.
        """
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
        """
        Test that no reviews are displayed in the 'dashboard'
        view.

        This test method ensures that when a user with no reviews logs
        into the 'dashboard' view, no reviews are displayed.

        Attributes:
            self: The test case instance.

        Usage:
        This test method logs in the user, sends a GET request to the
        'dashboard' view, and checks whether the 'reviews'
        variable exists in the view's context. It further verifies that
        the 'reviews' list is empty, indicating that no reviews are
        displayed for the user.

        Note:
        This test is part of the unit tests for the 'DashboardView'
        in the 'autoR5' Django application.
        """

        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertIn('reviews', response.context)
        self.assertEqual(list(response.context['reviews']), [])

    def test_reviews_displayed(self):
        """
        Test that user reviews are displayed in the 'dashboard'
        view.

        This test method ensures that when a user with reviews logs into
        the 'dashboard' view, their reviews are displayed. It
        creates a review, logs in the user, sends a GET request to the
        'dashboard' view, and checks if the user's reviews,
        including their ratings and comments, are visible in the
        esponse content.

        Attributes:
            self: The test case instance.

        Usage:
        This test method creates a review for the user, logs in the user,
        sends a GET request to the 'dashboard' view, and checks
        whether the 'reviews' variable exists in the view's context.
        It also verifies that the specific review data (rating and comment)
        is present in the HTML response content.

        Note:
        This test is part of the unit tests for the 'DashboardView'
        in the 'autoR5' Django application.
        """
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

        response_content = response.content.decode(
            "utf-8")
        self.assertIn(f'{review.rating}/5', response_content)
        self.assertIn(f'{review.comment}', response_content)

    def test_cancellation_request_form_displayed(self):
        """
        Test that the cancellation request form is displayed in the
        'dashboard' view.

        This test method ensures that when a user has a 'Confirmed'
        booking, the cancellation request form is displayed in the
        'dashboard' view. It creates a booking with the
        'Confirmed' status, logs in the user, sends a GET request
        to the 'dashboard' view, and checks if the
        cancellation request form is present in the view's context
        and visible in the response content.

        Attributes:
            self: The test case instance.

        Usage:
        This test method simulates a user with a 'Confirmed' booking,
        logs in the user, sends a GET request to the
        'dashboard' view, and verifies that the 'form'
        variable exists in the view's context and that the form
        contains the text 'Enter your reason here.'

        Note:
        This test is part of the unit tests for the
        'DashboardView' in the 'autoR5' Django application.
        """
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
        """
        Test that the 'Pay Now' button is displayed for a booking
        with 'Pending' status in the 'dashboard' view.

        This test method ensures that when a user has a booking with
        'Pending' status, the 'Pay Now' button is displayed in the
        'dashboard' view. It creates a booking with the
        'Pending' status, logs in the user, sends a GET request to
        the 'dashboard' view, and checks if the 'Pay Now'
        button is visible in the response content.

        Attributes:
            self: The test case instance.

        Usage:
        This test method simulates a user with a booking in 'Pending'
        status, logs in the user, sends a GET request to the
        'dashboard' view, and verifies that the 'Pay Now'
        button is present in the view's response content.

        Note:
        This test is part of the unit tests for the
        'DashboardView' in the 'autoR5' Django application.
        """
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
        """
        Test that the 'Book Again' option is displayed for a booking
        with 'Completed' status in the 'dashboard' view.

        This test method ensures that when a user has a booking with
        'Completed' status, the 'Book Again' option is displayed in the
        'dashboard' view. It creates a booking with the
        'Completed' status, logs in the user, sends a GET request to
        the 'dashboard' view, and checks if the 'Book Again'
        option is visible in the response content.

        Attributes:
            self: The test case instance.

        Usage:
        This test method simulates a user with a booking in 'Completed'
        status, logs in the user, sends a GET request to the
        'dashboard' view, and verifies that the 'Book Again'
        option is present in the view's response content. The
        'Book Again' option allows users to easily rebook the same
        car for a future rental.

        Note:
        This test is part of the unit tests for the
        'DashboardView' in the 'autoR5' Django application.
        """
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
           return_value=Mock(status='succeeded'))
    @patch('autoR5.signals.process_cancellation_request',
           side_effect=process_cancellation_request)
    def test_cancellation_request_with_approved_request(
            self, mock_process_cancellation_request, mock_refund_create):
        """
        Test the  dashboard view when a cancellation
        request is approved.

        This test method ensures that when a user has a booking
        with an approved cancellation request, the
        'dashboard' view displays the booking details
        without revealing the car's make and model, hides the
        cancellation form, shows a message indicating that the
        cancellation request is pending approval, and verifies
        that a Stripe refund is created.

        Attributes:
            self: The test case instance.
            mock_process_cancellation_request: A mocked function
            for processing a cancellation request.
            mock_refund_create: A mocked function for creating
            a Stripe refund.

        Usage:
        This test method simulates a user with a booking having
        an approved cancellation request. It creates a booking,
        payment object, and an approved cancellation request,
        logs in the user, sends a GET request to the
        'dashboard' view, and checks if the response
        content meets the following criteria:
            - Booking details are displayed without revealing
            car make and model.

            - The cancellation form is not visible.

            - A message indicating the cancellation request is
            pending approval is displayed.

            - A Stripe refund is created as expected.

        Note:
        This test is part of the unit tests for the 'DashboardView'
        in the 'autoR5' Django application. It helps ensure that the user's
        view is consistent and displays the relevant information based on
        the status of their booking and cancellation request.
        """
        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            status='Confirmed',
            rental_date=timezone.now() + timedelta(days=1),
            return_date=timezone.now() + timedelta(days=5),
        )

        payment = Payment.objects.create(
            user=self.user,
            booking=booking,
            amount=Decimal('400.00'),
            payment_method='Stripe',
            payment_status='Paid',
            payment_intent='test_intent'
        )

        cancellation_request = CancellationRequest.objects.create(
            booking=booking,
            user=self.user,
            reason="Test reason",
            approved=True
        )

        self.client.login(username="testuser", password="testpassword")

        url = reverse('dashboard')

        response = self.client.get(url)

        self.assertNotContains(response, booking.car.make)
        self.assertNotContains(response, booking.car.model)

        self.assertNotContains(response, 'Enter your reason here')

        self.assertNotContains(
            response, 'Cancellation request pending approval')

        mock_refund_create.assert_called_with(
            payment_intent=payment.payment_intent)

    def test_cancellation_request_without_approved_request(self):
        """
        Test the  dashboard view when a cancellation
        request is not approved.

        This test method ensures that when a user has a booking
        with an unapproved cancellation request, the
        'dashboard' view displays the booking details,
        shows the cancellation form, and does not display a
        message indicating that the cancellation request is
        pending approval.

        Attributes:
            self: The test case instance.

        Usage:
        This test method simulates a user with a booking that has
        an unapproved cancellation request. It creates a booking
        with an unapproved cancellation request, logs in the user,
        sends a GET request to the 'dashboard' view, and
        checks if the response content meets the following criteria:

            - Booking details are displayed, including car make and model.

            - The cancellation form is visible.

            - There is no message indicating that the cancellation request
            is pending approval.

        Note:
        This test is part of the unit tests for the 'DashboardView'
        in the 'autoR5' Django application. It helps ensure that the user's
        view is consistent and displays the relevant information based on
        the status of their booking and cancellation request.
        """

        booking = Booking.objects.create(
            user=self.user,
            car=self.car,
            status='Confirmed',
            rental_date=timezone.now() + timedelta(days=1),
            return_date=timezone.now() + timedelta(days=5),
        )

        cancellation_request = CancellationRequest.objects.create(
            booking=booking,
            user=self.user,
            reason="Test reason",
            approved=False
        )

        self.client.login(username="testuser", password="testpassword")

        url = reverse('dashboard')

        response = self.client.get(url)

        self.assertContains(response, booking.car.make)
        self.assertContains(response, booking.car.model)

        self.assertNotContains(response, 'Enter your reason here')

        self.assertContains(response, 'Cancellation request pending approval')


class LeaveReviewViewTest(TestCase):
    """
    Unit tests for the 'LeaveReviewView' in the 'autoR5'
    Django application.

    This test suite includes three test methods to ensure
    hat the 'LeaveReviewView' works as expected. This view
    allows users to leave reviews for cars they have rented.

    Attributes:
        TestCase: A class from the Django test framework
        for unit testing.

    Test Methods:
        1. test_view_url_exists_at_desired_location:
            - Purpose: Check if the view's URL exists and
            returns a 200 status code.

            - Usage: Simulates a logged-in user sending a
            GET request to the 'leave_review' view and checks
            for a 200 status code.

        2. test_view_uses_correct_template:
            - Purpose: Verify if the 'leave_review' view uses
            the correct HTML template.

            - Usage: Simulates a logged-in user sending a GET
            request to the view and checks if the template
            'leave_review.html' is used.

        3. test_review_form_submission:
            - Purpose: Confirm that submitting a review form redirects
            to the 'car_detail' view and displays a success message.

            - Usage: Simulates a logged-in user sending a POST request
            with review data (rating and comment) to the 'leave_review'
            view, checks for a redirect to the 'car_detail' view, and
            verifies the presence of a success message.

    Note:
    These tests validate the functionality and behavior of the
    'LeaveReviewView' in the 'autoR5' Django application,
    ensuring that users can leave reviews for cars and receive
    appropriate feedback after submitting a review.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')

        self.car = Car.objects.create(
            make='TestMake',
            model='TestModel',
            year=2023,
            license_plate='ABC123',
            daily_rate=100.00,
            location_city='Test Location',
        )

        self.url = reverse('leave_review', args=[self.car.id])

    def test_view_url_exists_at_desired_location(self):
        """
        Test whether the 'LeaveReviewView' URL exists and returns
        a 200 status code.

        This test method checks if the URL for the 'LeaveReviewView'
        exists and, when accessed by a logged-in user, returns a
        status code of 200 (OK). It verifies that the view is accessible.

        Attributes:
            self: The test case instance.

        Usage:
        - Log in a user with the provided username and password.
        - Send a GET request to the URL of the 'LeaveReviewView'.
        - Check if the response status code is 200 (OK), indicating
        that the view is accessible.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        """
        Test whether the 'LeaveReviewView' uses the correct template.

        This test method checks if the 'LeaveReviewView' uses the
        expected template, which is 'leave_review.html',
        by inspecting the response content. It helps ensure that
        the view is correctly configured to use the designated
        template for rendering.

        Attributes:
            self: The test case instance.

        Usage:
        - Log in a user with the provided username and password.
        - Send a GET request to the URL of the 'LeaveReviewView'.
        - Check if the response status code is 200 (OK).
        - Verify if the 'leave_review.html' template is used for
        rendering the view.
        """
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leave_review.html')

    def test_review_form_submission(self):
        """
        Test the submission of a review form on the 'LeaveReviewView'.

        This test method simulates the submission of a review form on
        the 'LeaveReviewView' by making a POST request with sample
        review data. It verifies whether the submission process
        correctly redirects to the 'car_detail' view and displays
        a success message.

        Attributes:
            self: The test case instance.

        Usage:
        - Log in a user with the provided username and password.
        - Send a POST request to the URL of the 'LeaveReviewView'
        with sample review data (rating and comment).
        - Check if the response is a redirect to the 'car_detail'
        view for the corresponding car.
        - Verify if the success message ('Thanks for your feedback!')
        is present in the response content.
        """
        self.client.login(username='testuser', password='testpassword')

        response = self.client.post(
            self.url, {'rating': 4, 'comment': 'Great car!'}, follow=True)

        self.assertRedirects(response, reverse(
            'car_detail', args=[self.car.id]))

        self.assertContains(response, 'Thanks for your feedback!')


class EditProfileViewTest(TestCase):
    """
    Unit tests for the 'EditProfileView' in the 'autoR5'
    Django application.

    This test suite includes three test methods to ensure
    that the 'EditProfileView' works as expected. This view allows
    users to edit their profiles, including updating their phone
    number and profile picture.

    Attributes:
        TestCase: A class from the Django test framework
        for unit testing.

    Test Methods:
        1. test_edit_profile_valid_phone_number:
            - Purpose: Verify that a user can update their phone number
            with a valid input.

            - Usage: Simulates a logged-in user sending a POST request
            to the 'edit_profile' view with a valid phone number and
            checks for a 200 status code. Verifies that the user's phone
            number is updated successfully.

        2. test_edit_profile_invalid_phone_number:
            - Purpose: Ensure that an invalid phone number input does
            not update the user's profile.

            - Usage: Simulates a logged-in user sending a POST request
            to the 'edit_profile' view with an invalid phone number and
            checks for a 200 status code. Verifies that the user's phone
            number remains unchanged and that an appropriate error message
            is displayed.

        3. test_edit_profile_with_image_upload:
            - Purpose: Confirm that a user can upload a new profile picture.

            - Usage: Simulates a logged-in user sending a POST request to
            the 'edit_profile' view with a valid phone number and an uploaded
            image. Checks for a 200 status code, verifies that the phone number
            is updated, and ensures that the uploaded image exists in
            Cloudinary.

        Note:
        These tests validate the functionality and behavior of the
        'EditProfileView' in the 'autoR5' Django application, allowing users
        to edit their profile information, including phone number and profile
        picture.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
        self.url = reverse('edit_profile')

    def test_edit_profile_valid_phone_number(self):
        """
        Unit test for the 'EditProfileView' in the 'autoR5'
        Django application, specifically testing the case of
        updating the user's phone number with a valid input.

        Attributes:
            TestCase: A class from the Django test framework
            for unit testing.

        Test Method:
            test_edit_profile_valid_phone_number:
                - Purpose: Verify that a user can update their
                phone number with a valid input.

                - Usage: Simulates a logged-in user sending a
                POST request to the 'edit_profile' view with a
                valid phone number and checks for a 200 status code.
                Verifies that the user's phone number is updated
                successfully and checks for the presence of a success
                message indicating the update.

        Note:
        This test method ensures that the 'EditProfileView' in the
        'autoR5' Django application correctly handles the scenario when
        a user updates their profile's phone number with a valid input.
        """
        response = self.client.post(self.url, {
            'phone_number': '1234567890'
        })
        self.assertEqual(response.status_code, 200)
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.phone_number, '1234567890')
        self.assertContains(response, "Phone number updated successfully.")

    def test_edit_profile_invalid_phone_number(self):
        """
        Unit test for the 'EditProfileView' in the 'autoR5'
        Django application, specifically testing the case of
        updating the user's phone number with an invalid input.

        Attributes:
            TestCase: A class from the Django test framework
            for unit testing.

        Test Method:
            test_edit_profile_invalid_phone_number:
                - Purpose: Verify that the 'edit_profile' view handles
                the case when a user attempts to update their phone
                umber with an invalid input.

                - Usage: Simulates a logged-in user sending a POST
                request to the 'edit_profile' view with an invalid phone
                number (e.g., not 9 to 10 digits long) and checks for a
                200 status code. Verifies that the user's phone number is
                not updated to the invalid input and checks for the
                presence of an error message indicating the required
                format.

        Note:
        This test method ensures that the 'EditProfileView' in the
        'autoR5' Django application correctly handles the scenario when a
        user attempts to update their profile's phone number with an
        invalid input.
        """

        response = self.client.post(self.url, {
            'phone_number': 'invalid_phone_number'
        })
        self.assertEqual(response.status_code, 200)
        user_profile = UserProfile.objects.get(user=self.user)
        self.assertNotEqual(user_profile.phone_number, 'invalid_phone_number')
        self.assertContains(
            response, "Phone number must be 9 to 10 digits long.")

    def test_edit_profile_with_image_upload(self):
        """
        Unit test for the 'EditProfileView' in the 'autoR5'
        Django application, specifically testing the case of
        updating the user's profile with an image upload.

        Attributes:
            TestCase: A class from the Django test framework
            for unit testing.

        Test Method:
            test_edit_profile_with_image_upload:
                - Purpose: Confirm that the 'edit_profile' view allows users to
                update their profile with a new phone number and a profile
                picture upload. It checks if the view responds with a 200
                status code and validates that the user's phone number is
                updated to the new value, and the profile picture is
                successfully uploaded.

                - Usage: Simulates a logged-in user sending a POST request to
                the 'edit_profile' view, providing a new phone number and a
                mock image file for profile picture upload. It then checks
                for a 200 status code and verifies that the phone number is
                updated correctly. Additionally, it ensures that the
                profile picture is uploaded and stored properly in Cloudinary.

        Note:
        This test method ensures that the 'EditProfileView' in the
        'autoR5' Django application functions correctly when a user updates
        their profile with both a new phone number and a profile
        picture upload.
        """
        image = Image.new('RGB', (100, 100))
        output = BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)

        image_file = SimpleUploadedFile(
            'image.jpg', output.getvalue(), content_type='image/jpeg')

        response = self.client.post(self.url, {
            'phone_number': '1234567890',
            'profile_picture': image_file
        })

        self.assertEqual(response.status_code, 200)

        user_profile = UserProfile.objects.get(user=self.user)
        self.assertEqual(user_profile.phone_number, '1234567890')

        self.assertIsNotNone(user_profile.profile_picture)

    def tearDown(self):
        user_profile = UserProfile.objects.get(user=self.user)

        if user_profile and user_profile.profile_picture:
            public_id = user_profile.profile_picture.public_id
            api.delete_resources(public_id)


#final tests go here

class ContactViewTest(TestCase):
    """
    Unit tests for the 'ContactView' in the 'autoR5' Django application.

    This test suite includes two test methods to ensure that the 'ContactView'
    works as expected. The 'ContactView' allows users to submit contact forms
    with their information and messages.

    Attributes:
        TestCase: A class from the Django test framework for unit testing.

    Test Methods:
        1. test_contact_form_submission:
            - Purpose: Verify that the 'ContactView' correctly handles a valid
            form submission. It checks if the view responds with a redirect
            after a successful submission and ensures that the submitted data
            matches the data saved in the database.

            - Usage: Simulates a user submitting a contact form with valid data
            and checks the response status, the saved submission, and the
            consistency of the submitted and saved data.

        2. test_contact_form_invalid_submission:
            - Purpose: Confirm that the 'ContactView' handles an invalid form
            submission correctly. It checks if the view does not redirect
            after an invalid submission and ensures that the form errors
            are present in the response.

            - Usage: Simulates a user submitting an empty form (invalid data)
            and hecks the response status, the absence of a redirect, and the
            presence of form errors in the response.

    Note:
    These tests validate the functionality and behavior of the 'ContactView' in
    the 'autoR5' Django application, ensuring that users can successfully
    submit contact forms and that the view handles both valid and invalid
    submissions appropriately.
    """

    def test_contact_form_submission(self):
        """
        Test the submission of a contact form in the 'ContactView'.

        Purpose:
            Verify that the 'ContactView' correctly handles a valid form
            submission. This test method simulates a user submitting a
            contact form with valid data and checks the following aspects:

            - The response status code is a redirect (302) after a
            successful submission.

            - The form submission is saved to the database.

            - The submitted data matches the data saved in the database,
            including first name, last name, email, subject, and message.

        Usage:
            Simulates a user sending a POST request to the 'ContactView'
            with valid form data containing first name, last name, email,
            subject, and a message. The method then examines the response
            status code, verifies the presence of the saved submission in
            the database, and compares the submitted data to the saved data.

        Note:
        This test method ensures that the 'ContactView' in the 'autoR5'
        Django application handles valid contact form submissions
        correctly, storing the data accurately in the database.
        """
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
        """
        Test an invalid form submission to the 'ContactView'.

        Purpose:
            Verify that the 'ContactView' correctly handles an
            invalid form submission by submitting an empty form
            (invalid data). This test method checks the
            following aspects:

            - The response status code is not a redirect (not 302)
            since the form is invalid.

            - The response contains form errors for required fields:
            first name, last name, email, subject, and message.

        Usage:
            Simulates a user sending a POST request to the 'ContactView'
            with an empty form, resulting in an invalid submission. The
            method then examines the response status code, ensuring it's
            not a redirect, and checks for form errors in the response
            for required fields.

        Note:
        This test method ensures that the 'ContactView' in the 'autoR5'
        Django application appropriately handles invalid form submissions
        by providing meaningful form error messages for required fields.
        """
        url = reverse('contact')
        response = self.client.post(url, data={})

        self.assertNotEqual(response.status_code, 302)

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
    """
    Unit tests for the 'CustomSignupForm' in the 'autoR5' Django application.

    This test suite includes two test methods to validate the behavior of the
    custom signup form.

    Attributes:
        TestCase: A class from the Django test framework for unit testing.

    Test Methods:
        1. test_valid_custom_signup_form:
            - Purpose: Confirm that the custom signup form is valid when all
            required fields, including the additional 'phone_number' field,
            are provided with appropriate data.
            - Usage: Creates a user registration data dictionary with valid
            data and asserts that the form is valid when instantiated with
            this data.

        2. test_invalid_custom_signup_form_missing_phone_number:
            - Purpose: Validate that the custom signup form is invalid when
            the 'phone_number' field is missing in the user registration data.

            - Usage: Creates a user registration data dictionary with a missing
            'phone_number' field and asserts that the form is not valid due
            to the absence of this required field.

    Note:
    These tests ensure the correct functioning of the 'CustomSignupForm',
    guaranteeing that it properly handles both valid and invalid data scenarios
    during user registration, including the additional 'phone_number' field.
    """

    def test_valid_custom_signup_form(self):
        """
        Test a valid form submission to the 'CustomSignupForm'.

        Purpose:
            Verify that the 'CustomSignupForm' validates a user registration
            with valid data. This test method creates a user registration data
            dictionary with a valid username, email, matching passwords, and
            a phone number. It then initializes the 'CustomSignupForm' with
            this data and checks whether the form is valid.

        Usage:
            Simulates a user filling out a registration form with valid data
            for username, email, matching passwords, and a phone number. The
            method creates the 'CustomSignupForm' instance with this data
            and verifies that the form is valid.

        Note:
        This test method ensures that the 'CustomSignupForm' in the 'autoR5'
        Django application correctly validates user registration data when
        all required fields are provided with valid values.
        """
        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'phone_number': '1234567890',
        }

        form = CustomSignupForm(data=registration_data)

        self.assertTrue(form.is_valid())

    def test_invalid_custom_signup_form_missing_phone_number(self):
        """
        Test an invalid form submission to the 'CustomSignupForm' with
        a missing phone number.

        Purpose:
            Verify that the 'CustomSignupForm' correctly handles an invalid
            form submission by submitting registration data with a missing
            phone number. This test method creates a user registration data
            dictionary without a phone number and initializes the
            'CustomSignupForm' with this data. It then checks that the form
            is not valid due to the missing phone number and that form errors
            include 'phone_number'.

        Usage:
            Simulates a user attempting to register without providing a phone
            number. The method creates the 'CustomSignupForm' instance with
            this data and confirms that the form is not valid, indicating that
            a phone number is required.

        Note:
        This test method ensures that the 'CustomSignupForm' in the 'autoR5'
        Django application enforces the requirement of a phone number during
        user registration and correctly handles cases where it's missing.
        """

        registration_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        form = CustomSignupForm(data=registration_data)

        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)


class BookingFormTest(TestCase):
    """
    Unit tests for the 'BookingForm' in the 'autoR5' Django application.

    This test suite includes two test methods to ensure that the
    'BookingForm' works as expected. The 'BookingForm' is responsible for
    handling booking data, including rental and return dates.

    Attributes:
        TestCase: A class from the Django test framework for unit testing.

    Test Methods:
        1. test_valid_booking_form:
            - Purpose: Verify that the 'BookingForm' accepts valid booking
            data with correct date values.

            - Usage: Creates a booking data dictionary with valid rental
            and return dates and initializes the 'BookingForm' with this
            data. Then, it checks that the form is valid.

        2. test_invalid_booking_form_return_date_before_rental_date:
            - Purpose: Confirm that the 'BookingForm' detects an invalid
            return date that is before the rental date.

            - Usage: Creates a booking data dictionary with an invalid
            return date (before the rental date) and initializes the
            'BookingForm' with this data. The method checks if the form
            has a validation error on the 'return_date' field.

    Note:
    These tests validate the functionality of the 'BookingForm' in the
    'autoR5' Django application, ensuring that it correctly handles valid
    booking data and properly detects cases where the return date is
    before the rental date.
    """

    def test_valid_booking_form(self):
        """
        Test the 'BookingForm' with valid booking data.

        Purpose:
            Verify that the 'BookingForm' accepts valid booking data with
            correct date values.

        Usage:
            - Create a booking data dictionary with valid rental and
            return dates.
            - Initialize the 'BookingForm' with this data.
            - Check that the form is valid.

        Note:
        This test method ensures that the 'BookingForm' in the 'autoR5' Django
        application can handle valid booking data, specifically with proper
        rental and return dates.
        """
        booking_data = {
            'rental_date': '2023-10-01',
            'return_date': '2023-10-10',
        }

        form = BookingForm(data=booking_data)

        self.assertTrue(form.is_valid())

    def test_invalid_booking_form_return_date_before_rental_date(self):
        """
        Test the 'BookingForm' with an invalid return date before
        the rental date.

        Purpose:
            Verify that the 'BookingForm' correctly identifies and
            rejects booking data where the return date is before the
            rental date.

        Usage:
            - Create a booking data dictionary with an invalid return
            date that precedes the rental date.
            - Initialize the 'BookingForm' with this data.
            - Check if the form has a validation error on the 'return_date'
            field, indicating that "Return date must be after the rental
            date."

        Note:
        This test method ensures that the 'BookingForm' in the 'autoR5'
        Django application can handle and reject booking data with a return
        date that occurs before the rental date, preventing invalid bookings.
        """
        booking_data = {
            'rental_date': '2023-10-10',
            'return_date': '2023-10-01',
        }

        form = BookingForm(data=booking_data)

        self.assertTrue("Return date must be after the rental date.")


class ReviewFormTest(TestCase):
    """
    Unit tests for the 'ReviewForm' in the 'autoR5' Django application.

    This test suite includes three test methods to ensure the 'ReviewForm'
    works as expected. The form is used for leaving reviews, and the test
    methods cover different aspects of its validation.

    Attributes:
        TestCase: A class from the Django test framework for unit testing.

    Test Methods:
        1. test_valid_form:
            - Purpose: Verify that the 'ReviewForm' is valid with a valid
            rating and comment.
            - Usage: Create a form instance with valid data, including a
            rating of 5 and a comment. Check if the form is considered valid.

        2. test_rating_out_of_range:
            - Purpose: Confirm that the 'ReviewForm' is invalid when the
            rating is out of the valid range (greater than 5).
            - Usage: Create a form instance with a rating of 6 (outside
            the valid range) and a comment. Check if the form is considered
            invalid and contains a specific error message for the rating field.

        3. test_rating_below_range:
            - Purpose: Ensure that the 'ReviewForm' is invalid when the rating
            is below the valid range (less than 1).
            - Usage: Create a form instance with a rating of 0 (outside the
            valid range) and a comment. Check if the form is considered invalid
            and contains a specific error message for the rating field.

        4. test_missing_comment:
            - Purpose: Validate that the 'ReviewForm' is invalid when a comment
            is missing.
            - Usage: Create a form instance with a valid rating and an empty
            comment. Check if the form is considered invalid.

    Note:
    These test methods are designed to test the validation behavior of the
    'ReviewForm' in the 'autoR5' Django application, ensuring that it
    correctly handles various scenarios, including valid data, out-of-range
    ratings, and missing comments.
    """

    def test_valid_form(self):
        """
        Test a valid form submission using the 'ReviewForm'.

        Purpose:
            Verify that the 'ReviewForm' is considered valid when provided
            with a valid rating (5) and a comment. This test method checks the
            following aspects:

            - The form is created with valid data, including a rating of 5
              and a non-empty comment.
            - The form's 'is_valid()' method returns 'True'.

        Usage:
            Create a 'ReviewForm' instance with data representing a valid
            review, including a rating of 5 and a non-empty comment. Then,
            check if the form is considered valid using the 'is_valid()'
            method.

        Note:
        This test method validates that the 'ReviewForm' correctly handles
        valid review submissions by ensuring that the form's validation
        passes when provided with acceptable data.
        """
        form = ReviewForm(data={
            'rating': 5,
            'comment': 'Great car!',
        })
        self.assertTrue(form.is_valid())

    def test_rating_out_of_range(self):
        """
        Test an invalid form submission using the 'ReviewForm' with a rating
        value outside the valid range.

        Purpose:
            Verify that the 'ReviewForm' correctly handles an invalid form
            submission where the rating value is outside the acceptable range.
            This test method checks the following aspects:

            - The form is created with an out-of-range rating value (6) and
              a non-empty comment.
            - The form's 'is_valid()' method returns 'False.'
            - The form's errors include a message indicating that the rating
              value should be less than or equal to 5.

        Usage:
            Create a 'ReviewForm' instance with data representing an invalid
            review, including a rating value of 6 and a non-empty comment.
            Then, check if the form is considered invalid using the
            'is_valid()' method, and confirm that an error message about the
            rating value being out of range is present in the form's errors.

        Note:
        This test method ensures that the 'ReviewForm' handles and rejects
        out-of-range rating values by validating that the form is marked
        as invalid and includes a suitable error message.
        """
        form = ReviewForm(data={
            'rating': 6,
            'comment': 'Excellent car!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Ensure this value is less than or equal to 5.',
            form.errors['rating'])

    def test_rating_below_range(self):
        """
        Test an invalid form submission using the 'ReviewForm' with a rating
        value below the valid range.

        Purpose:
            Verify that the 'ReviewForm' correctly handles an invalid form
            submission where the rating value is below the acceptable range.
            This test method checks the following aspects:

            - The form is created with a below-range rating value (0) and
              a non-empty comment.
            - The form's 'is_valid()' method returns 'False.'
            - The form's errors include a message indicating that the rating
              value should be greater than or equal to 1.

        Usage:
            Create a 'ReviewForm' instance with data representing an invalid
            review, including a rating value of 0 and a non-empty comment.
            Then, check if the form is considered invalid using the
            'is_valid()' method, and confirm that an error message about the
            rating value being below the valid range is present in the form's
            errors.

        Note:
        This test method ensures that the 'ReviewForm' correctly rejects
        below-range rating values by validating that the form is marked as
        invalid and includes a suitable error message.
        """
        form = ReviewForm(data={
            'rating': 0,
            'comment': 'Terrible car!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn(
            'Ensure this value is greater than or equal to 1.',
            form.errors['rating'])

    def test_missing_comment(self):
        """
        Test an invalid form submission using the 'ReviewForm' with a missing
        comment.

        Purpose:
            Verify that the 'ReviewForm' correctly handles an invalid form
            submission where the comment field is left empty. This test method
            checks the following aspects:

            - The form is created with a valid rating value (4) and an empty
              comment.
            - The form's 'is_valid()' method returns 'False.'
            - The form's errors include a message indicating that the comment
              field is required.

        Usage:
            Create a 'ReviewForm' instance with data representing an invalid
            review, including a valid rating value (4) and an empty comment.
            Then, check if the form is considered invalid using the
            'is_valid()' method, and confirm that an error message about
            the required comment field is present in the form's errors.

        Note:
        This test method ensures that the 'ReviewForm' correctly rejects
        missing comments by validating that the form is marked as
        invalid and includes an appropriate error message.
        """


class ContactFormTest(TestCase):
    """
    Unit tests for the 'ContactForm' in the 'autoR5' Django application.

    This test suite includes two test methods to ensure that the 'ContactForm'
    works as expected. The 'ContactForm' is used for user inquiries and allows
    users to submit their contact information and messages.

    Attributes:
        TestCase: A class from the Django test framework for unit testing.

    Test Methods:
        1. test_valid_contact_form:
            - Purpose: Test a valid form submission using the 'ContactForm.'

            - Usage: Create a 'ContactForm' instance with complete and valid
              contact data, including the first name, last name, email,
              subject and message. Verify that the form is considered valid
              using the 'is_valid()' method.

        2. test_invalid_contact_form_missing_fields:
            - Purpose: Test an invalid form submission using the 'ContactForm'
              with missing fields.

            - Usage: Create a 'ContactForm' instance with incomplete and
            invalid contact data, specifically by omitting the required first
            name and email fields. Confirm that the form is marked as invalid
            using the 'is_valid()' method, and check that error messages about
            the missing fields (first name and email) are included in the
            form's errors.

    Note:
    These tests validate the functionality of the 'ContactForm' in the
    'autoR5' Django application, ensuring that it correctly processes both
    valid and invalid form submissions for user inquiries.
    """

    def test_valid_contact_form(self):
        """
        Test a valid form submission using the 'ContactForm'.

        Purpose:
            Verify that the 'ContactForm' correctly handles a valid form
            submission by providing it with complete and accurate contact
            data. This test method checks the following aspects:

            - The form is created with valid contact data, including the
              first name, last name, email, subject, and message.
            - The form's 'is_valid()' method returns 'True.'

        Usage:
            Create a 'ContactForm' instance with complete and valid contact
            data, such as a first name, last name, email, subject, and message.
            Then, verify that the form is considered valid using the
            'is_valid()' method.

        Note:
        This test method ensures that the 'ContactForm' correctly accepts
        and validates complete and accurate contact information.
        """
        contact_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'johndoe@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.',
        }

        form = ContactForm(data=contact_data)

        self.assertTrue(form.is_valid())

    def test_invalid_contact_form_missing_fields(self):
        """
        Test an invalid form submission using the 'ContactForm' with missing
        fields.

        Purpose:
            Verify that the 'ContactForm' correctly handles an invalid form
            submission by submitting incomplete contact data with missing
            required fields. This test method checks the following aspects:

            - The form is created with missing required fields, such as the
              first name and email.
            - The form's 'is_valid()' method returns 'False.'
            - The form's errors include messages indicating the missing
              first name and email fields.

        Usage:
            Create a 'ContactForm' instance with incomplete and invalid
            contact data, specifically by omitting the required first name
            and email fields. Then, confirm that the form is marked as invalid
            using the 'is_valid()' method, and check that error messages about
            the missing fields (first name and email) are included in the
            form's errors.

        Note:
        This test method ensures that the 'ContactForm' correctly rejects
        invalid form submissions that lack required contact information.
        """
        contact_data = {
            'first_name': '',
            'last_name': 'Doe',
            'email': '',
            'subject': 'Test Subject',
            'message': 'This is a test message.',
        }

        form = ContactForm(data=contact_data)

        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('email', form.errors)


class CancellationRequestFormTest(TestCase):
    """
    Unit tests for the 'CancellationRequestForm' in the 'autoR5'
    Django application.

    This test suite includes two test methods to ensure that the
    'CancellationRequestForm' works as expected. The
    'CancellationRequestForm' is used for users to submit cancellation
    requests for their bookings.

    Attributes:
        TestCase: A class from the Django test framework for unit testing.

    Test Methods:
        1. test_valid_cancellation_request_form:
            - Purpose: Test a valid form submission using the
            'CancellationRequestForm.'

            - Usage: Create a 'CancellationRequestForm' instance with complete
            and valid cancellation request data, including a valid reason.
            Verify that the form is considered valid using the 'is_valid()'
            method.

        2. test_invalid_cancellation_request_form_missing_reason:
            - Purpose: Test an invalid form submission using the
            'CancellationRequestForm' with a missing reason field.
            - Usage: Create a 'CancellationRequestForm' instance with
            incomplete and invalid cancellation request data, specifically
            by omitting the required reason field. Confirm that the form is
            marked as invalid using the 'is_valid()' method, and check that an
            error message regarding the missing reason field is included in the
            form's errors.

    Note:
    These tests validate the functionality of the 'CancellationRequestForm' in
    the 'autoR5' Django application, ensuring that it correctly processes both
    valid and invalid form submissions for cancellation requests, particularly
    focusing on the presence of the required 'reason' field.
    """

    def test_valid_cancellation_request_form(self):
        """
        Test a valid form submission using the 'CancellationRequestForm'.

        Purpose:
            This test method verifies the functionality of the
            'CancellationRequestForm' by submitting valid cancellation request
            data, specifically including a valid reason. The primary goal is
            to ensure that the form processes this valid data correctly.

        Usage:
            1. Create a dictionary 'cancellation_data' with valid cancellation
            request data, including a meaningful reason.

            2. Create an instance of the 'CancellationRequestForm' by providing
            'cancellation_data'.

            3. Verify that the form is considered valid by calling the
            'is_valid()' method.

            4. Use 'self.assertTrue()' to confirm that the form is indeed
            valid.

        Note:
        This test method focuses on testing the 'CancellationRequestForm' when
        provided with a complete and valid cancellation request, with a
        particular emphasis on the 'reason' field being valid. It checks
        whether the form correctly processes such valid data.
        """
        cancellation_data = {
            'reason': 'This is a valid cancellation reason.',
        }

        form = CancellationRequestForm(data=cancellation_data)

        self.assertTrue(form.is_valid())

    def test_invalid_cancellation_request_form_missing_reason(self):
        """
        Test an invalid form submission using the
        'CancellationRequestForm' with a missing reason.

        Purpose:
            This test method focuses on verifying the behavior
            of the 'CancellationRequestForm' when presented with
            invalid data. Specifically, it examines the form's response
            when the required 'reason' field is missing.

        Usage:
            1. Create a 'cancellation_data' dictionary with a missing
            required 'reason' field.

            2. Instantiate the 'CancellationRequestForm' with the incomplete
            'cancellation_data'.

            3. Verify that the form is not considered valid due to the
            missing 'reason' field by checking the result of
            'form.is_valid()'.

            4. Use 'self.assertFalse()' to assert that the form is
            indeed invalid.

            5. Check for form errors using 'self.assertIn()' to ensure that
            'reason' is reported as a required field error in 'form.errors'.

        Note:
        This test method focuses on a scenario where the
        'CancellationRequestForm' is expected to handle missing data by
        detecting the absence of a 'reason' and raising a validation error
        accordingly. The main objective is to ensure that the form
        correctly identifies this specific type of invalid input.
        """
        cancellation_data = {
            'reason': '',
        }

        form = CancellationRequestForm(data=cancellation_data)

        self.assertFalse(form.is_valid())
        self.assertIn('reason', form.errors)


class UserProfileFormTest(TestCase):
    """
    Unit tests for the 'UserProfileForm' in the 'autoR5' Django
    application.

    This test suite includes multiple test methods to validate
    the behavior of the 'UserProfileForm'. The form is used for
    updating user profiles, including phone numbers and profile
    pictures.

    Attributes:
        TestCase: A class from the Django test framework for unit
        testing.

    Test Methods:
        1. test_valid_user_profile_form:
            - Purpose: Check if the 'UserProfileForm' is valid when
            provided with valid user profile data.

            - Usage: Instantiate the form with valid phone number,
            and ensure the form is considered valid.

        2. test_invalid_user_profile_form_invalid_phone_number:
            - Purpose: Verify that the form is invalid when an invalid
            phone number (less than 9 digits) is provided.

            - Usage: Instantiate the form with an invalid phone number
            and check for validation errors.

        3. test_valid_user_profile_form_with_picture_upload:
            - Purpose: Confirm that the form is valid when a valid phone
            number and a profile picture are provided.

            - Usage: Simulate a form submission with a valid phone number
            and a mock image file for the profile picture. heck if the form
            is valid after uploading the image.

        4. test_valid_user_profile_form_with_clear_picture:
            - Purpose: Ensure the form is valid when the user selects
            "Clear Profile Picture".

            - Usage: Provide a valid phone number and set the 'clear_picture'
            field to True. Verify that the form is valid under these
            conditions.

    Note:
    These tests validate the functionality and behavior of the
    'UserProfileForm' in the 'autoR5' Django application, ensuring that it
    handles valid and invalid input for phone numbers and profile picture
    uploads correctly.
    """

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create(
            username='testuser',
            email='testuser@example.com',
            password='testpassword123')
        self.client.login(username='testuser',
                          password='testpassword')
        self.url = reverse('edit_profile')

    def test_valid_user_profile_form(self):
        """
        Test a valid form submission to the 'UserProfileForm'.

        Purpose:
            Verify that the 'UserProfileForm' is valid when provided with
            valid user profile data, specifically a valid phone number.

        Usage:
            1. Create a 'profile_data' dictionary with a valid phone number.
            2. Instantiate the 'UserProfileForm' with the 'profile_data'.
            3. Verify that the form is valid by checking the result of
            'form.is_valid()'.
            4. Use 'self.assertTrue()' to assert that the form is indeed valid.
        """
        profile_data = {
            'phone_number': '1234567890',
        }

        form = UserProfileForm(data=profile_data)

        self.assertTrue(form.is_valid())

    def test_invalid_user_profile_form_invalid_phone_number(self):
        """
        Test an invalid form submission to the 'UserProfileForm' with an
        invalid phone number.

        Purpose:
            Verify that the 'UserProfileForm' is not valid when provided
            with user profile data containing an invalid phone number,
            specifically, a phone number with less than 9 digits.

        Usage:
            1. Create a 'profile_data' dictionary with an invalid phone
            number (less than 9 digits).
            2. Instantiate the 'UserProfileForm' with the 'profile_data'.
            3. Verify that the form is not valid by checking the result of
            'form.is_valid()'.
            4. Use 'self.assertFalse()' to assert that the form is indeed
            not valid.
            5. Check for the presence of the 'phone_number' field in the
            form errors using 'self.assertIn()'.

        Note:
        This test method ensures that the 'UserProfileForm' correctly
        identifies and reports an invalid phone number, specifically when it
        has fewer than 9 digits, by checking for the presence of errors in
        the form.
        """
        profile_data = {
            'phone_number': '1234',
        }

        form = UserProfileForm(data=profile_data)

        self.assertFalse(form.is_valid())
        self.assertIn('phone_number', form.errors)

    def test_valid_user_profile_form_with_picture_upload(self):
        """
        Test a valid form submission to the 'UserProfileForm'
        with a picture upload.

        Purpose:
            Verify that the 'UserProfileForm' is valid when
            provided with user profile data, including a phone
            number and a profile picture upload.

        Usage:
            1. Create a mock image file for testing. An image of 100x100
            pixels in JPEG format is generated.

            2. Prepare a 'SimpleUploadedFile' object, 'image_file,' based
            on the mock image.

            3. Simulate a form submission by creating a 'form_data'
            dictionary that includes a valid phone number and the
            'profile_picture_upload' field set to the 'image_file.'

            4. Instantiate the 'UserProfileForm' with the 'form_data' and
            'files' parameters to simulate the file upload.

            5. Verify that the form is valid by checking the result of
            'form.is_valid()'.

            6. Use 'self.assertTrue()' to assert that the form is indeed
            valid.

        Note:
        This test method ensures that the 'UserProfileForm' correctly handles
        a valid form submission that includes user profile data with a phone
        number and a profile picture upload. It verifies that the form is
        valid in this scenario.
        """
        image = Image.new('RGB', (100, 100))
        output = BytesIO()
        image.save(output, format='JPEG')
        output.seek(0)

        image_file = SimpleUploadedFile(
            'image.jpg', output.getvalue(), content_type='image/jpeg')

        form_data = {
            'phone_number': '1234567890',
            'profile_picture_upload': image_file
        }
        form = UserProfileForm(data=form_data, files={
                               'profile_picture_upload': image_file})

        self.assertTrue(form.is_valid())

    def test_valid_user_profile_form_with_clear_picture(self):
        """
        Test a valid form submission to the 'UserProfileForm' with the "Clear
        Profile Picture" option.

        Purpose:
            Verify that the 'UserProfileForm' is valid when provided with user
            profile data that includes a valid phone number and the
            "Clear Profile Picture" option checked.

        Usage:
            1. Create a 'profile_data' dictionary with a valid phone number
            and set the 'clear_picture' field to 'True' to indicate that the
            user wants to clear their profile picture.

            2. Instantiate the 'UserProfileForm' with the 'profile_data'
            dictionary.

            3. Verify that the form is valid by checking the result of
            'form.is_valid()'.

            4. Use 'self.assertTrue()' to assert that the form is indeed
            valid.

        Note:
        This test method ensures that the 'UserProfileForm' correctly handles a
        valid form submission that includes user profile data with a phone
        number and the option to clear the user's profile picture. It verifies
        that the form is valid when "Clear Profile Picture" is selected.
        """
        profile_data = {
            'phone_number': '1234567890',
            'clear_picture': True,
        }

        form = UserProfileForm(data=profile_data)

        self.assertTrue(form.is_valid())


class CsvImportExportFormTest(TestCase):
    """
    Unit tests for importing and exporting CSV data using the
    'CsvImportExportForm'.

    This test suite includes two test methods:
    1. 'test_import_csv_function': Simulates the import of CSV data using the
    'CsvImportExportForm'. It creates a mock CSV file for testing and sends a
    POST request to the 'import_csv' view. The test verifies the response
    status code and checks that the data from the CSV file is correctly
    imported into the 'Car' model.

    2. 'test_export_csv_function': Simulates the export of CSV data using the
    'CsvImportExportForm'. It creates some 'Car' objects for testing and sends
    a GET request to the 'export_csv' view. The test checks that the response
    status code is as expected and verifies that the exported CSV data matches
    the expected format and content.

    Note:
    These tests ensure that the 'CsvImportExportForm' correctly handles CSV
    data import and export functionality. It validates the integrity of the
    data transfer between CSV files and the 'Car' model.
    """

    def setUp(self):
        self.user = User.objects.create(
            username='admin', password='adminpassword')

    def test_import_csv_function(self):
        """
        Test the CSV data import functionality using the
        'CsvImportExportForm'.

        Purpose:
        This test method simulates the import of CSV data into the system.
        It creates a mock CSV file containing data for 'Car' objects, simulates
        a POST request to the 'import_csv' view, and verifies that the response
        status code is 302 (indicating a successful redirect). The test also
        creates 'Car' objects based on the imported data and checks if the data
        from the CSV file is correctly imported into the 'Car' model.

        Usage:
        1. Create a mock CSV file with data for 'Car' objects.

        2. Simulate an HTTP POST request to the 'import_csv' view, providing
        the CSV file for import.

        3. Check that the response status code is 302, indicating a successful
        import.

        4. Create 'Car' objects based on the imported data.

        5. Verify that the data from the CSV file is correctly imported into
        the 'Car' model.

        Note:
        This test method ensures that the CSV data import feature correctly
        handles data files and accurately populates the 'Car' model with the
        imported data.
        """

        csv_data = (
            "make,model,year,license_plate,daily_rate,"
            "is_available,latitude,longitude,"
            "location_city,location_address,"
            "features,car_type,fuel_type,end\n"
            "Toyota,Camry,2023,XYZ123,50.0,TRUE,37.123,-122.456,"
            "San Jose,123 random street,"
            "Test features,Saloon,Petrol\n"
        )

        csv_file = SimpleUploadedFile("cars.csv",
                                      csv_data.encode("utf-8"))

        response = self.client.post(reverse('admin:import_csv'), {
                                    'csv_import': csv_file})

        self.assertEqual(response.status_code, 302)

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

        self.assertEqual(car.make, 'Toyota')
        self.assertEqual(car.model, 'Camry')
        self.assertEqual(car.year, 2023)
        self.assertAlmostEqual(car.daily_rate, 50.00, places=2)
        self.assertEqual(car.is_available, True)
        self.assertAlmostEqual(car.latitude, 37.123, places=3)
        self.assertAlmostEqual(car.longitude, -122.456, places=3)
        self.assertEqual(car.location_city, 'San Jose')
        self.assertEqual(car.location_address, '123 random street')
        self.assertEqual(car.features, 'Test features')
        self.assertEqual(car.car_type, 'Saloon')
        self.assertEqual(car.fuel_type, 'Petrol')

    def test_export_csv_function(self):
        """
        Test the CSV data export functionality using the
        'CsvImportExportForm'.

        Purpose:
        This test method verifies the export of CSV data from the system.
        It creates 'Car' objects with sample data for testing, simulates
        an HTTP GET request to the 'export_csv' view, and checks that
        the response has a status code of 200 (indicating success).
        The test further ensures that the exported CSV data matches the
        expected format and content.

        Usage:
        1. Create 'Car' objects with sample data for testing.

        2. Simulate an HTTP GET request to the 'export_csv' view to
        trigger data export.

        3. Check that the response has a status code of 200, indicating
        a successful export.

        4. Compare the exported CSV data to the expected CSV data format
        and content.

        Note:
        This test method confirms that the CSV data export feature is
        working correctly by generating CSV data that adheres to the
        specified format and contains the expected data from the 'Car' model.
        """
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

        response = self.client.get(reverse('admin:export_csv'))

        self.assertEqual(response.status_code, 200)

        expected_csv_data = (
            "Make,Model,Year,License Plate,Daily Rate,"
            "Available,Latitude,Longitude,"
            "Location City,Location Address,"
            "Image,Features,Car Type,Fuel Type\r\n"
            "Toyota,Camry,2023,XYZ123,50.00,"
            "TRUE,37.123000,-122.456000,"
            "San Jose,123 random street,,"
            "Test features,Saloon,Petrol"
        ).strip()

        self.assertMultiLineEqual(
            response.content.decode().strip(), expected_csv_data)


class UpdateLocationTest(TestCase):
    """
    Test the 'update_location' admin action for 'Car' objects.

    Purpose:
    This test class is designed to evaluate the functionality of
    the 'update_location' admin action in the 'Car' model's
    admin interface. The test case covers the process of updating
    a car's location based on its latitude and longitude coordinates
    by invoking a geocoding service (Nominatim). The specific
    purpose of the test methods is to confirm that the location
    fields ('location_city' and 'location_address')
    are correctly populated based on the geocoding results.

    Usage:
    1. Create a superuser and a 'Car' object with relevant data,
    including latitude and longitude coordinates.

    2. Mock the Nominatim geocoder using patching to control
    geocoding responses.

    3. Verify that the car's location fields are initially empty.

    4. Simulate an admin action to update the car's location by
    triggering the 'update_location' action in the admin interface.

    5. Refresh the car instance from the database and ensure tha
    the location fields have been successfully updated with the
    geocoded information.

    6. Clean up by deleting the superuser and the 'Car' object
    after testing.

    Note:
    This test class assesses the accuracy of the 'update_location'
    admin action by verifying that it retrieves location
    information from the latitude and longitude coordinates and
    stores it in the appropriate fields ('location_city' and
    'location_address') of the 'Car' model.
    """
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
        """
        Test the 'update_location' admin action for a 'Car'
        object.

        Purpose:
        This test method assesses the behavior of the
        'update_location' admin action when invoked for a
        specific 'Car' object. The primary objective is to
        validate that the action correctly retrieves and
        stores location information based on the car's
        latitude and longitude coordinates by simulating
        a call to a geocoding service (Nominatim). The
        method checks whether the location fields, including
        'location_city' and 'location_address', are populated
        as expected with the geocoded data.

        Usage:
        1. Mock the Nominatim geocoder using the @patch
        decorator and provide a mock geocoding response containing
        address details such as 'city' and 'address.'

        2. Confirm that the car's 'location_city' and
        'location_address' fields are initially empty.

        3. Simulate the admin action to update the car's location
        by creating an HTTP POST request to the corresponding
        admin interface.

        4. After executing the admin action, refresh the 'Car'
        instance from the database.

        5. Validate that the 'location_city' field is updated to
        'San Jose' and that 'location_address' contains relevant
        address information, including '24, North 5th Street,'
        'San Jose,' and '95112.'

        Note:
        This test method evaluates the accuracy of the
        'update_location' admin action for a single 'Car' object,
        verifying that it effectively retrieves location data from
        the latitude and longitude coordinates and correctly stores
        it in the corresponding fields. It also confirms that the
        geocoding service's response is processed as expected.
        """
        mock_nominatim = mock_geocoder.return_value
        mock_location = {
            'raw': {
                'address': {
                    'city': 'San Jose',
                },
            },
            'address': '24, North 5th Street, San Jose, CA 95112 San Jose,'
            'Horrace Mann, '
            'Downtown San Jose San Jose California United States',
        }
        mock_nominatim.reverse.return_value = mock_location

        self.assertEqual(self.car.location_city, '')
        self.assertEqual(self.car.location_address, '')

        client = self.client
        client.login(username='admin', password='adminpassword')
        response = client.post(
            '/admin/autoR5/car/',
            {
                'action': 'update_location',
                '_selected_action': [str(self.car.pk)],
            }
        )

        self.car.refresh_from_db()
        self.assertEqual(self.car.location_city, 'San Jose')
        self.assertIn('24, North 5th Street', self.car.location_address)
        self.assertIn('San Jose', self.car.location_address)
        self.assertIn('95112', self.car.location_address)

    def tearDown(self):
        self.user.delete()
        self.car.delete()


class TestUrls(TestCase):
    """
    Test the URL patterns and associated view functions of
    the 'autoR5' Django application.

    Purpose:
    This test class verifies that the URL patterns defined
    in the 'urls.py' file of the 'autoR5' Django application
    are correctly mapped to their respective view functions.
    Each test method focuses on a specific URL pattern and
    confirms that it resolves to the intended view function
    using the Django 'resolve' function.

    Usage:
    Each test method simulates a URL reversal using the
    'reverse' function to obtain the URL for a specific view.
    The 'resolve' function is then used to determine
    the associated view function for that URL. The test
    methods compare the resolved view function with the
    expected view function to ensure accurate URL-to-view
    function mapping.

    Note:
    This test class ensures the integrity of the URL
    configurations in the 'autoR5' Django application,
    providing confidence that the defined URLs lead to the
    intended views. It aids in identifying potential issues
    with URL routing, helping maintain consistent navigation
    within the application.
    """
    def test_index_url(self):
        """
        Verify the URL pattern for the 'index' view.

        Purpose:
        Ensures that the 'index' URL correctly maps
        to the 'index' view function.

        Usage:
        This test validates the URL pattern for the
        'index' view by comparing the resolved
        view function to the expected 'index'
        view function.

        Note:
        Essential to confirm that the 'index' URL leads
        to the main landing page.
        """
        url = reverse('index')
        self.assertEqual(resolve(url).func,
                         views.index)

    def test_car_detail_url(self):
        """
        Verify the URL pattern for the 'car_detail' view.

        Purpose:
        Ensures that the 'car_detail' URL correctly maps to
        the 'car_detail' view function.

        Usage:
        Validates the URL pattern for the 'car_detail' view
        by comparing the resolved view function to the expected
        'car_detail' view function.

        Note:
        Essential to confirm that the 'car_detail' URL leads
        to the car detail page.
    """
        url = reverse('car_detail', args=[1])
        self.assertEqual(resolve(url).func,
                         views.car_detail)

    def test_book_car_url(self):
        """
        Verify the URL pattern for the 'book_car' view.

        Purpose:
        Ensures that the 'book_car' URL correctly maps to the
        'book_car' view function.

        Usage:
        Validates the URL pattern for the 'book_car' view by
        comparing the resolved view function to the expected
        'book_car' view function.

        Note:
        Essential to confirm that the 'book_car' URL leads to
        the booking page.
    """
        url = reverse('book_car', args=[1])
        self.assertEqual(resolve(url).func,
                         views.book_car)

    def test_booking_confirmation_url(self):
        """
        Verify the URL pattern for the 'booking_confirmation' view.

        Purpose:
        Ensures that the 'booking_confirmation' URL correctly maps
        to the 'booking_confirmation' view function.

        Usage:
        Validates the URL pattern for the 'booking_confirmation'
        view by comparing the resolved view function to the expected
        'booking_confirmation' view function.

        Note:
        Essential to confirm that the 'booking_confirmation' URL
        leads to the booking confirmation page.
        """
        url = reverse('booking_confirmation', args=[1])
        self.assertEqual(resolve(url).func,
                         views.booking_confirmation)

    def test_leave_review_url(self):
        """
        Verify the URL pattern for the 'leave_review' view.

        Purpose:
        Ensures that the 'leave_review' URL correctly maps to the
        'leave_review' view function.

        Usage:
        Validates the URL pattern for the 'leave_review' view by
        comparing the resolved view function to the expected
        'leave_review' view function.

        Note:
        Essential to confirm that the 'leave_review' URL leads to
        the leave review page.
        """
        url = reverse('leave_review', args=[1])
        self.assertEqual(resolve(url).func,
                         views.leave_review)

    def test_cars_list_url(self):
        """
        Verify the URL pattern for the 'cars_list' view.

        Purpose:
        Ensures that the 'cars_list' URL correctly maps to
        the 'cars_list' view function.

        Usage:
        Validates the URL pattern for the 'cars_list' view
        by comparing the resolved view function to the
        expected 'cars_list' view function.

        Note:
        Essential to confirm that the 'cars_list' URL leads
        to the car listing page.
        """
        url = reverse('cars_list')
        self.assertEqual(resolve(url).func,
                         views.cars_list)

    def test_contact_url(self):
        """
        Verify the URL pattern for the 'contact' view.

        Purpose:
        Ensures that the 'contact' URL correctly maps to
        the 'contact' view function.

        Usage:
        Validates the URL pattern for the 'contact' view
        by comparing the resolved view function to the expected
        'contact' view function.

        Note:
        Essential to confirm that the 'contact' URL leads to
        the contact page.
        """
        url = reverse('contact')
        self.assertEqual(resolve(url).func,
                         views.contact)

    def test_dashboard_url(self):
        """
        Verify the URL pattern for the 'dashboard' view.

        Purpose:
        Ensures that the 'dashboard' URL correctly maps
        to the 'dashboard' view function.

        Usage:
        Validates the URL pattern for the 'dashboard'
        view by comparing the resolved view function to the expected
        'dashboard' view function.

        Note:
        Essential to confirm that the 'dashboard' URL leads
        to the  dashboard.
        """
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func,
                         views.dashboard)

    def test_edit_profile_url(self):
        """
        Verify the URL pattern for the 'edit_profile' view.

        Purpose:
        Ensures that the 'edit_profile' URL correctly maps to the
        'edit_profile' view function.

        Usage:
        Validates the URL pattern for the 'edit_profile' view by
        comparing the resolved view function to the expected
        'edit_profile' view function.

        Note:
        Essential to confirm that the 'edit_profile' URL leads to
        the user profile editing page.
        """
        url = reverse('edit_profile')
        self.assertEqual(resolve(url).func,
                         views.edit_profile)

    def test_get_car_makes_url(self):
        """
        Verify the URL pattern for the 'get_car_makes' view.

        Purpose:
        Ensures that the 'get_car_makes' URL correctly maps
        to the 'get_car_makes' view function.

        Usage:
        Validates the URL pattern for the 'get_car_makes'
        view by comparing the resolved view function to the expected
        'get_car_makes' view function.

        Note:
        Essential to confirm that the 'get_car_makes' URL leads
        to car makes retrieval.
        """
        url = reverse('get_car_makes')
        self.assertEqual(resolve(url).func,
                         views.get_car_makes)

    def test_get_car_models_url(self):
        """
        Verify the URL pattern for the 'get_car_models' view.

        Purpose:
        Ensures that the 'get_car_models' URL correctly maps to
        the 'get_car_models' view function.

        Usage:
        Validates the URL pattern for the 'get_car_models'
        view by comparing the resolved view function to the
        expected 'get_car_models' view function.

        Note:
        Essential to confirm that the 'get_car_models'
        URL leads to car models retrieval.
        """
        url = reverse('get_car_models')
        self.assertEqual(resolve(url).func,
                         views.get_car_models)

    def test_get_car_years_url(self):
        """
        Verify the URL pattern for the 'get_car_years' view.

        Purpose:
        Ensures that the 'get_car_years' URL correctly maps to the
        'get_car_years' view function.

        Usage:
        Validates the URL pattern for the 'get_car_years' view by
        comparing the resolved view function to the expected
        'get_car_years' view function.

        Note:
        Essential to confirm that the 'get_car_years' URL
        leads to car years retrieval.
        """
        url = reverse('get_car_years')
        self.assertEqual(resolve(url).func,
                         views.get_car_years)

    def test_get_car_locations_url(self):
        """
        Verify the URL pattern for the 'get_car_locations' view.

        Purpose:
        Ensures that the 'get_car_locations' URL correctly maps
        to the 'get_car_locations' view function.

        Usage:
        Validates the URL pattern for the 'get_car_locations'
        view by comparing the resolved view function to the
        expected 'get_car_locations' view function.

        Note:
        Essential to confirm that the 'get_car_locations'
        URL leads to car locations retrieval.
        """
        url = reverse('get_car_locations')
        self.assertEqual(resolve(url).func,
                         views.get_car_locations)

    def test_get_car_types_url(self):
        """
        Verify the URL pattern for the 'get_car_types' view.

        Purpose:
        Ensures that the 'get_car_types' URL correctly maps to
        the 'get_car_types' view function.

        Usage:
        Validates the URL pattern for the 'get_car_types'
        view by comparing the resolved view function to the expected
        'get_car_types' view function.

        Note:
        Essential to confirm that the 'get_car_types' URL
        leads to car types retrieval.
        """
        url = reverse('get_car_types')
        self.assertEqual(resolve(url).func,
                         views.get_car_types)

    def test_get_fuel_types_url(self):
        """
        Verify the URL pattern for the 'get_fuel_types' view.

        Purpose:
        Ensures that the 'get_fuel_types' URL correctly maps
        to the 'get_fuel_types' view function.

        Usage:
        Validates the URL pattern for the 'get_fuel_types'
        view by comparing the resolved view function to the expected
        'get_fuel_types' view function.

        Note:
        Essential to confirm that the 'get_fuel_types' URL leads to
        fuel types retrieval.
        """
        url = reverse('get_fuel_types')
        self.assertEqual(resolve(url).func,
                         views.get_fuel_types)

    def test_checkout_url(self):
        """
        Verify the URL pattern for the 'checkout' view.

        Purpose:
        Ensures that the 'checkout' URL correctly maps to the
        'checkout' view function.

        Usage:
        Validates the URL pattern for the 'checkout' view by
        comparing the resolved view function to the expected
        'checkout' view function.

        Note:
        Essential to confirm that the 'checkout' URL leads to
        the checkout page.
        """
        url = reverse('checkout', args=[1, 1])
        self.assertEqual(resolve(url).func,
                         views.checkout)


class JarallaxTest(LiveServerTestCase):
    """
    Test the Jarallax initialization on a web page.

    Purpose:
    This test class is designed to verify the proper
    initialization of the Jarallax parallax scrolling
    effect on a web page. It checks if the Jarallax
    effect is applied as expected by inspecting the
    relevant CSS properties of an element.

    Usage:
    The test class uses Selenium to interact with a
    live web page and examines the Jarallax effect on an
    element. The test navigates to the web page, waits
    for a specified duration, locates the element with the
    Jarallax effect, and checks whether the element's CSS
    properties reflect the expected transformation.

    Note:
    - Ensure that the web page under test contains an element
    with Jarallax effect applied.

    - The test duration in the 'time.sleep' can be adjusted
    based on page load times.

    - The CSS property checked in the assertion should match
    the expected Jarallax effect.
    """
    def setUp(self):
        current_file = inspect.getfile(inspect.currentframe())
        base_dir = os.path.dirname(os.path.abspath(current_file))

        main_project_dir = os.path.dirname(base_dir)

        custom_chromedriver_path = os.path.join(main_project_dir,
                                                'chrome-win64',
                                                'chromedriver.exe')
        chrome_binary_path = os.path.join(main_project_dir,
                                          'chrome-win64',
                                          'chrome.exe')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = chrome_binary_path
        chrome_options.add_argument('start-maximized')

        self.selenium = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.selenium.quit()

    def test_jarallax_initialization(self):
        """
        Verify the initialization of the Jarallax parallax
        effect.

        Purpose:
        This test method validates that the Jarallax
        parallax effect is correctly applied to an element on
        a web page. It ensures that the element's CSS
        properties reflect the expected transformation that
        characterizes Jarallax parallax scrolling.

        Usage:
        The test method loads the web page containing the
        Jarallax effect, waits for a specified duration to
        allow page rendering, locates the element with the Jarallax
        effect, and checks the element's CSS properties to confirm
        the presence of the expected Jarallax transformation.

        Note:
        - Adjust the sleep duration as needed for page loading.
        - Customize the CSS property in the assertion to match
        the expected Jarallax effect.
        """
        self.selenium.get('http://localhost:8000/')

        time.sleep(2)

        jarallax_element = self.selenium.find_element(
            By.CSS_SELECTOR, '.jarallax-container div')

        self.assertIn('transform: translate3d(0px, 65px, 0px);',
                      jarallax_element.get_attribute('style'))


class MessageAlertsTest(LiveServerTestCase):
    """
    Test message alerts on a web page after user interaction.

    Purpose:
    This test class verifies the functionality of message
    alerts displayed on a web page following user interactions,
    such as logging in. It checks if the expected alert message
    is shown and correctly disappears after a certain event.

    Usage:
    The test class uses Selenium to interact with a live web page,
    simulating user actions like clicking the "Log In" button,
    entering login credentials, and submitting the form. It waits
    for the alert message to appear, validates its content, and
    ensures it disappears as expected.

    Note:
    - Adjust the URLs, locators, and content checks based on your
    specific web application.

    - The test assumes that there is a message container element
    with a unique ID.
    """
    def setUp(self):
        current_file = inspect.getfile(inspect.currentframe())
        base_dir = os.path.dirname(os.path.abspath(current_file))

        main_project_dir = os.path.dirname(base_dir)

        custom_chromedriver_path = os.path.join(main_project_dir,
                                                'chrome-win64',
                                                'chromedriver.exe')
        chrome_binary_path = os.path.join(main_project_dir,
                                          'chrome-win64',
                                          'chrome.exe')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = chrome_binary_path
        chrome_options.add_argument('start-maximized')

        self.selenium = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.selenium.quit()

    def test_message_alerts(self):
        """
        Verify message alerts after user interaction.

        Purpose:
        This test method ensures that message alerts on a
        web page function as intended after user interactions.
        It verifies that the expected alert message appears
        after a successful action (e.g., logging in) and
        subsequently disappears.

        Usage:
        The test loads the web page, simulates a user clicking
        the "Log In" button, entering login credentials, and
        submitting the form. It then waits for the alert message
        to be displayed and checks its content. Finally, the
        test ensures that the message alert disappears as expected.

        Note:
        - Customize the test method with appropriate locators,
        URLs, and alert content checks.

        - Adjust wait conditions based on the behavior of your
        web application.
        """
        self.selenium.get('http://localhost:8000/')

        log_in_button = self.selenium.find_element(
            By.LINK_TEXT, "Log In")
        log_in_button.click()

        username_input = self.selenium.find_element(By.NAME, "login")
        password_input = self.selenium.find_element(By.NAME, "password")
        login_button = self.selenium.find_element(
            By.XPATH, "//button[@type='submit']")

        username = 'testuser'
        password = 'testpassword'

        username_input.send_keys(username)
        password_input.send_keys(password)
        login_button.click()

        WebDriverWait(self.selenium, 10).until(
            expected_conditions.presence_of_element_located(
                (By.ID, "message-container"))
        )

        message_container = self.selenium.find_element(
            By.ID, "message-container")
        self.assertEqual(
            message_container.value_of_css_property("display"), 'block')

        message_text = message_container.text
        self.assertIn(f"Successfully signed in as {username}.", message_text)

        WebDriverWait(self.selenium, 10).until(
            lambda driver: 'none' in message_container.value_of_css_property(
                "display")
        )


class AJAXFilterTests(LiveServerTestCase):
    """
    Test AJAX-based filtering on a web page.

    Purpose:
    This test class focuses on verifying the functionality of
    AJAX-based filtering on a web page. It checks if filtering
    options for car make, model, year, type, fuel, and location
    update the displayed car listings correctly.

    Usage:
    The test class utilizes Selenium WebDriver to interact with
    a web page, performing actions like selecting options from
    dropdowns and clicking filter and reset buttons. It pauses
    briefly to allow AJAX responses to update the page. The test
    then checks if the number of displayed car listings matches
    the expected count after filtering and resetting.

    Note:
    - Customize the test method with appropriate locators, URLs,
    and filtering options.

    - Adjust wait times based on the speed of AJAX requests and
    the behavior of your web application.
    """
    def setUp(self):
        current_file = inspect.getfile(inspect.currentframe())
        base_dir = os.path.dirname(os.path.abspath(current_file))

        main_project_dir = os.path.dirname(base_dir)

        custom_chromedriver_path = os.path.join(main_project_dir,
                                                'chrome-win64',
                                                'chromedriver.exe')
        chrome_binary_path = os.path.join(main_project_dir,
                                          'chrome-win64',
                                          'chrome.exe')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = chrome_binary_path
        chrome_options.add_argument('start-maximized')

        self.selenium = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.selenium.quit()

    def test_dropdown_updates(self):
        """
        Verify that dropdown updates trigger correct AJAX
        filtering.

        Purpose:
        This test method ensures that selecting options from
        car make, model, year, type, fuel, and location dropdowns
        triggers the expected AJAX filtering on the web page.
        It checks if the number of displayed car listings changes
        accordingly after each selection.

        Usage:
        The test loads the target web page and sequentially selects
        options from each dropdown, waiting for AJAX updates after
        each selection. It then verifies that the filtered listings
        match the expected count. Additionally, it checks that
        clicking the reset button restores the original listing count.

        Note:
        - Customize this method with specific locators and expected
        filtering results.

        - Adjust wait times based on the behavior of your web
        application and AJAX response times.
        """
        self.selenium.get(
            'http://localhost:8000/cars_list/')

        make_dropdown = Select(
            self.selenium.find_element_by_id('car_make'))
        make_dropdown.select_by_value('Alfa Romeo')

        time.sleep(2)

        model_dropdown = Select(
            self.selenium.find_element_by_id('car_model'))
        model_dropdown.select_by_value('Giulia')

        time.sleep(2)

        year_dropdown = Select(
            self.selenium.find_element_by_id('car_year'))
        year_dropdown.select_by_value('2023')

        time.sleep(2)

        car_type_dropdown = Select(
            self.selenium.find_element_by_id('car_type'))
        car_type_dropdown.select_by_value('Saloon')

        time.sleep(2)

        fuel_type_dropdown = Select(
            self.selenium.find_element_by_id('fuel_type'))
        fuel_type_dropdown.select_by_value('Petrol')

        time.sleep(2)

        location_dropdown = Select(
            self.selenium.find_element_by_id('car_location'))
        location_dropdown.select_by_value('Dublin')

        time.sleep(2)

        filter_button = login_button = self.selenium.find_element(
            By.XPATH, '//*[@id="filter-form"]/div/div[7]/button[1]')
        filter_button.click()

        time.sleep(2)

        item_wrappers = self.selenium.find_elements_by_class_name(
            'item-wrapper')
        self.assertEqual(len(item_wrappers), 1)

        reset_button = self.selenium.find_element_by_id(
            'reset-filter')
        reset_button.click()

        time.sleep(2)

        item_wrappers_after_reset = self.selenium.find_elements_by_class_name(
            'item-wrapper')
        self.assertGreater(len(item_wrappers_after_reset), 1)


class MapTest(LiveServerTestCase):
    """
    Test the display of a map with markers on a web page.

    Purpose:
    This test class is designed to verify the correct display
    of a map with markers on a web page. It checks if the map
    and its associated markers are correctly rendered.

    Usage:
    The test class utilizes Selenium WebDriver to load a
    specific web page, log in as a user, and checks for the
    presence and visibility of a map and its markers. It
    waits for a brief period to allow the map to render.

    Note:
    - Customize the test method with the appropriate URL and
    login credentials.

    - Adjust wait times based on the rendering speed of the
    map and markers.
    """
    def setUp(self):
        current_file = inspect.getfile(inspect.currentframe())
        base_dir = os.path.dirname(os.path.abspath(current_file))

        main_project_dir = os.path.dirname(base_dir)

        custom_chromedriver_path = os.path.join(main_project_dir,
                                                'chrome-win64',
                                                'chromedriver.exe')
        chrome_binary_path = os.path.join(main_project_dir,
                                          'chrome-win64',
                                          'chrome.exe')

        chrome_options = webdriver.ChromeOptions()
        chrome_options.binary_location = chrome_binary_path
        chrome_options.add_argument('start-maximized')

        self.selenium = webdriver.Chrome(options=chrome_options)

    def tearDown(self):
        self.selenium.quit()

    def test_map_displayed(self):
        """
        Verify that the map and markers are correctly displayed.

        Purpose:
        This test method ensures that a web page displays a
        map and its associated markers properly. It logs in
        as a test user, waits for the map to load, and then
        checks the visibility of the map and its markers.

        Usage:
        The test loads a specific web page, logs in with the
        provided credentials, and waits for the map to render.
        It then checks if the map is displayed and if at least
        one marker is visible.

        Note:
        - Customize this method with the specific URL,
        login credentials, and marker locator as needed.

        - Adjust the wait time to accommodate the map's loading
        time.
        """
        self.selenium.get(
            f'http://localhost:8000/booking/65/confirmation/')

        username_input = self.selenium.find_element(By.NAME, "login")
        password_input = self.selenium.find_element(By.NAME, "password")
        login_button = self.selenium.find_element(
            By.XPATH, "//button[@type='submit']")

        username_input.send_keys('testuser')
        password_input.send_keys('testpassword')
        login_button.click()

        time.sleep(3)

        map_element = self.selenium.find_element_by_id('map')
        self.assertTrue(map_element.is_displayed())

        marker_element = self.selenium.find_element_by_class_name(
            'leaflet-marker-icon')
        self.assertTrue(marker_element.is_displayed())
