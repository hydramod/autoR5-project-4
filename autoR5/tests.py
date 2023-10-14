from django.test import TestCase
from .models import Car, Booking, Review
from django.urls import reverse, resolve
from django.contrib.auth.models import User
from . import views
from .forms import BookingForm, ReviewForm
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone
from decimal import Decimal
import random, string
from django import forms


class CarModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        cls.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2022,
            license_plate="ABC123",
            daily_rate=100.00,
            location_name="Test Location",
            car_type="Hatchback",
            fuel_type="Petrol",
        )

    def test_car_string_representation(self):
        car = self.car
        expected_string = f"{car.year} {car.make} {car.model}"
        self.assertEqual(str(car), expected_string)


class BookingModelTest(TestCase):
    def test_booking_total_cost_calculation(self):
        # Create a test user
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a test car
        car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2022,
            license_plate="ABC123",
            daily_rate=100.00,
            location_name="Test Location",
            car_type="Hatchback",
            fuel_type="Petrol",
        )

        rental_date = datetime(2022, 1, 1, 12, 0, 0)
        return_date = rental_date + timedelta(days=4)  # 4 days later

        booking = Booking.objects.create(
            user=user,
            car=car,
            rental_date=rental_date,
            return_date=return_date,
            total_cost=0.00,  # Initially set to 0
        )

        # Calculate the total cost
        booking.calculate_total_cost()

        # Ensure the total cost is calculated correctly
        self.assertEqual(booking.total_cost, 400.00)


class ReviewModelTest(TestCase):
    def test_review_rating_validator(self):
        # Create a test user
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a test car
        car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2022,
            license_plate="ABC123",
            daily_rate=100.00,
            location="Test Location",
        )

        # Test a valid review rating
        valid_review = Review(
            car=car,
            user=user,
            rating=5,  # Valid rating (5 stars)
            comment="Great car!",
        )
        valid_review.full_clean()  # Should not raise any validation error

        # Test an invalid review rating (less than the minimum)
        invalid_review = Review(
            car=car,
            user=user,
            rating=0,  # Invalid rating (0 stars)
            comment="Poor car!",
        )
        with self.assertRaises(ValidationError):
            invalid_review.full_clean()

    def test_review_string_representation(self):
        # Create a test user
        user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a test car
        car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2022,
            license_plate="ABC123",
            daily_rate=100.00,
            location="Test Location",
        )

        review = Review.objects.create(
            car=car,
            user=user,
            rating=5,
            comment="Great car!",
        )

        expected_string = f"Review for {car.year} {car.make} {car.model} by {user.username}"
        self.assertEqual(str(review), expected_string)


class CarListViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/cars_list/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('cars_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cars_list.html')


class CarDetailViewTest(TestCase):
    def test_view_url_exists_at_desired_location(self):
        car = Car.objects.create(make='TestMake', model='TestModel', year=2022, license_plate='ABC123',
                                 daily_rate=100.00, location='Test Location')
        response = self.client.get(f'/car/{car.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        car = Car.objects.create(make='TestMake', model='TestModel', year=2022, license_plate='ABC123',
                                 daily_rate=100.00, location='Test Location')
        response = self.client.get(reverse('car_detail', args=[car.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'car_detail.html')


class BookingViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a car
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2022,
            license_plate="ABC123",
            daily_rate=100.00,
            location_name="Test Location",
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse('book_car', kwargs={'car_id': self.car.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="testuser", password="testpassword")

        url = reverse('book_car', kwargs={'car_id': self.car.id})

        response = self.client.get(url)

        self.assertTemplateUsed(response, 'book_car.html')

    def test_booking_total_cost_calculation(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Define the URL
        url = reverse('book_car', kwargs={'car_id': self.car.id})

        # Define booking data
        booking_data = {
            'rental_date': timezone.now(),
            'return_date': timezone.now() + timezone.timedelta(days=4),  # 4 days later
        }

        # Perform a POST request with booking data
        response = self.client.post(url, booking_data)

        # Check if the total_cost is correctly calculated and passed to the template
        self.assertEqual(response.status_code, 302)  # Check for a redirect
        self.assertRedirects(response, reverse('booking_confirmation', args=[1]))  # Adjust the URL as needed

        # Follow the redirect to the booking_confirmation view
        response = self.client.get(response.url)

        # Check if the total_cost is in the context of the booking_confirmation view
        self.assertEqual(response.context['total_cost'], Decimal('400.00'))


class BookingConfirmationViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a car
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2022,
            license_plate="ABC123",
            daily_rate=100.00,
            location_name="Test Location",
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username="testuser", password="testpassword")
        url = reverse('book_car', kwargs={'car_id': self.car.id})

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username="testuser", password="testpassword")

        url = reverse('book_car', kwargs={'car_id': self.car.id})

        booking_data = {
            'rental_date': timezone.now(),
            'return_date': timezone.now() + timezone.timedelta(days=4),  # 4 days later
        }

        response = self.client.post(url, booking_data)

        # Check if the total_cost is correctly calculated and passed to the template
        self.assertEqual(response.status_code, 302)  # Check for a redirect

        # Follow the redirect to the booking_confirmation view
        response = self.client.get(response.url, follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'booking_confirmation.html')


class LeaveReviewViewTest(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a car
        self.car = Car.objects.create(
            make='TestMake',
            model='TestModel',
            year=2022,
            license_plate='ABC123',
            daily_rate=100.00,
            location_name='Test Location',
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

        response = self.client.post(self.url, {'rating': 4, 'comment': 'Great car!'}, follow=True)

        # Check for a redirect to the 'car_detail' view
        self.assertRedirects(response, reverse('car_detail', args=[self.car.id]))

        # Verify if the success message is present in the response content
        self.assertContains(response, 'Thanks for your feedback!')

    def test_approve_review(self):
        # Create a review
        review = Review.objects.create(
            car=self.car,
            user=self.user,
            rating=4,
            comment='Great car!',
        )

        # Set the review as approved
        review.approved = True
        review.save()

        # Get the URL of the car_detail page
        car_detail_url = reverse('car_detail', args=[self.car.id])

        # Fetch the car detail page
        response = self.client.get(car_detail_url)

        # Verify if the approved review comment is present in the 'car_detail' template
        self.assertContains(response, 'Great car!')


class CustomerDashboardViewTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('customer_dashboard')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_dashboard.html')


class CancelBookingTest(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="testpassword")

        # Create a test car
        self.car = Car.objects.create(
            make="TestMake",
            model="TestModel",
            year=2022,
            license_plate="ABC123",
            daily_rate=100.00,
            location_name="Test Location",
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

    def test_cancel_booking_from_customer_dashboard(self):
        # Log in the user
        self.client.login(username="testuser", password="testpassword")

        # Access the customer_dashboard page
        response = self.client.get(reverse('customer_dashboard'))

        # Check if the customer_dashboard page loads successfully
        self.assertEqual(response.status_code, 200)

        # Ensure that there is a cancel booking form in the response
        self.assertContains(response, 'form method="POST"')

        # Submit the cancellation form
        response = self.client.post(reverse('customer_dashboard'), {"booking_id": self.booking.id, "reason": "Change of plans"}, follow=True)
        
        # Check if the booking has been canceled
        self.assertEqual(response.status_code, 200)

        # Verify if the message is present in the response content
        self.assertContains(response, "Cancellation request submitted successfully")


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


class BookingFormTest(TestCase):
    def test_valid_form(self):
        form = BookingForm(data={
            'rental_date': '2023-10-15',
            'return_date': '2023-10-20',
        })
        self.assertTrue(form.is_valid())

    def test_rental_date_after_return_date(self):
        form = BookingForm(data={
            'rental_date': '2023-10-20',
            'return_date': '2023-10-15',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Return date must be after the rental date.', form.non_field_errors())

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
        self.assertIn('Ensure this value is less than or equal to 5.', form.errors['rating'])

    def test_rating_below_range(self):
        form = ReviewForm(data={
            'rating': 0,
            'comment': 'Terrible car!',
        })
        self.assertFalse(form.is_valid())
        self.assertIn('Ensure this value is greater than or equal to 1.', form.errors['rating'])

    def test_missing_comment(self):
        form = ReviewForm(data={
            'rating': 4,
            'comment': '',
        })
        self.assertFalse(form.is_valid())