from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Car, CarType, FuelType, Booking, Review, CancellationRequest
from .forms import BookingForm, ReviewForm
from datetime import date

def index(request):
    #cars = Car.objects.filter(is_available=True)
    return render(request, 'index.html')

def contact(request):
    return render(request, 'contact.html')

def cars_list(request):
    cars = Car.objects.all()
    car_types = CarType.objects.all()
    fuel_types = FuelType.objects.all()
    car_type = request.GET.get('type')
    fuel_type = request.GET.get('fuel')
    if car_type:
        cars = cars.filter(car_type__name=car_type)
    if fuel_type:
        cars = cars.filter(fuel_type__name=fuel_type)
    return render(request, 'cars_list.html', {'cars': cars, 'car_types': car_types, 'fuel_types': fuel_types})

def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    reviews = Review.objects.filter(car=car, approved=True)
    return render(request, 'car_detail.html', {'car': car, 'reviews': reviews})

@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.location = Car.location

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
                messages.error(request, 'This car is already booked for the selected dates.')
                return redirect('book_car', car_id=car_id)

            booking.total_cost = (booking.return_date - booking.rental_date).days * car.daily_rate
            booking.save()
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'book_car.html', {'car': car, 'form': form})

@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking_confirmation.html', {'booking': booking})

@login_required
def leave_review(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.car = car
            review.save()
            return redirect('car_detail', car_id=car.id)
    else:
        form = ReviewForm()
    
    return render(request, 'leave_review.html', {'car': car, 'form': form})

@login_required
def customer_dashboard(request):
    user = request.user
    current_bookings = Booking.objects.filter(user=user, return_date__gte=timezone.now())
    past_bookings = Booking.objects.filter(user=user, return_date__lt=timezone.now())
    reviews = Review.objects.filter(user=user)

    return render(request, 'customer_dashboard.html', {
        'user': user,
        'current_bookings': current_bookings,
        'past_bookings': past_bookings,
        'reviews': reviews,
    })

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)

    if request.method == 'POST':
        if booking.return_date >= timezone.now():
            reason = request.POST.get('reason')
            if not reason:
                messages.error(request, 'Please provide a reason for cancellation.')
            else:
                CancellationRequest.objects.create(booking=booking, user=request.user, reason=reason)
                booking.delete()
                messages.success(request, 'Booking has been canceled.')

        else:
            messages.error(request, 'You cannot cancel a past booking.')

    return redirect('customer_dashboard')




