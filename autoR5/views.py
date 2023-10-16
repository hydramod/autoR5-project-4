from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Car, Booking, Review, CancellationRequest
from .forms import BookingForm, ReviewForm, ContactForm, CancellationRequestForm
from datetime import date
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


def index(request):
    # Get unique car types and fuel types from the Car model
    car_types = Car.objects.values_list('car_type', flat=True).distinct().exclude(car_type=None)
    fuel_types = Car.objects.values_list('fuel_type', flat=True).distinct().exclude(fuel_type=None)

    return render(request, 'index.html', {'car_types': car_types, 'fuel_types': fuel_types})


def contact(request):
    return render(request, 'contact.html')


def cars_list(request):
    cars = Car.objects.all()

    # Get filter values from the request's GET parameters
    car_make = request.GET.get('make')
    car_model = request.GET.get('model')
    car_year = request.GET.get('year')
    car_location = request.GET.get('location')
    car_type = request.GET.get('car_type')
    fuel_type = request.GET.get('fuel_type')

    # Filter the queryset based on the selected filter values
    if car_make:
        cars = cars.filter(make=car_make)
    if car_model:
        cars = cars.filter(model=car_model)
    if car_year:
        cars = cars.filter(year=car_year)
    if car_location:
        cars = cars.filter(location_name=car_location)
    
    if car_type:
        cars = cars.filter(car_type=car_type)
    if fuel_type:
        cars = cars.filter(fuel_type=fuel_type)

    # Add pagination
    page_number = request.GET.get('page')
    paginator = Paginator(cars, 8)  # Show 10 cars per page
    page = paginator.get_page(page_number)

    return render(request, 'cars_list.html', {
        'cars': page,  # Pass the current page instead of all cars
        'car_types': Car.CAR_TYPES,  # Use the choices defined in the Car model
        'fuel_types': Car.FUEL_TYPES,  # Use the choices defined in the Car model
    })


def reset_filter(request):
    return redirect(reverse('cars_list'))


def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    reviews = Review.objects.filter(car=car, approved=True)
    return render(request, 'car_detail.html', {'car': car, 'reviews': reviews})


@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    total_cost = None  # Initialize total_cost as None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.location = car.location_name

            today = date.today()
            rental_date = booking.rental_date.date()
            if rental_date < today:
                messages.error(request, 'You cannot book for a past date.')
                return redirect('book_car', car_id=car_id)

            conflicting_bookings = Booking.objects.filter(
                Q(car=car) &
                (
                    Q(rental_date__range=(booking.rental_date, booking.return_date)) |
                    Q(return_date__range=(booking.rental_date, booking.return_date))
                )
            )
            if conflicting_bookings.exists():
                messages.error(
                    request, 'This car is already booked for the selected dates.')
                return redirect('book_car', car_id=car_id)

            # Calculate the total_cost before saving
            booking.calculate_total_cost()
            booking.save()
            total_cost = booking.total_cost

            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'book_car.html', {'car': car, 'form': form})


@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    car = booking.car
    location_name = car.location_name
    location_lat = car.latitude
    location_long = car.longitude
    total_cost = booking.total_cost
    return render(request, 'booking_confirmation.html', {'booking': booking, 'location_name': location_name, 'location_lat': location_lat, 'location_long': location_long, 'total_cost': total_cost})


@login_required
def leave_review(request, car_id):
    if not request.user.is_authenticated:
        messages.error(request, 'Please log in to leave a review.')
        return redirect('account_login')

    car = get_object_or_404(Car, pk=car_id)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.car = car
            review.save()
            messages.success(request, 'Thanks for your feedback!')
            return redirect('car_detail', car_id=car.id)
        else:
            messages.error(
                request, 'Oops...! There was a problem submitting your feedback.')
    else:
        form = ReviewForm()

    return render(request, 'leave_review.html', {'car': car, 'form': form})


@login_required
def customer_dashboard(request):
    user = request.user
    current_bookings = Booking.objects.filter(
        user=user, return_date__gte=timezone.now())
    past_bookings = Booking.objects.filter(
        user=user, return_date__lt=timezone.now())
    reviews = Review.objects.filter(user=user)
    form = CancellationRequestForm()  # Define the form here

    # Handle booking cancellations
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')  # Retrieve the booking_id from request.POST
        if booking_id is not None:
            booking = Booking.objects.get(id=booking_id)

            # Create a cancellation request
            cancellation_request = form.save(commit=False)
            cancellation_request.booking = booking
            cancellation_request.user = user
            cancellation_request.save()

            # Delete the booking
            booking.delete()

            messages.success(request, 'Cancellation request submitted successfully')
            return redirect('customer_dashboard')

    return render(request, 'customer_dashboard.html', {
        'user': user,
        'current_bookings': current_bookings,
        'past_bookings': past_bookings,
        'reviews': reviews,
        'form': form,
    })


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Form data is valid, you can now process the data
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']

            # Trigger a success message
            messages.success(
                request, 'Thanks for getting touch, One of our representatives will contact you soon')
        else:
            # Form data is not valid, trigger an error message
            messages.error(
                request, 'Oops...! There was a probolem submitting your request.')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})