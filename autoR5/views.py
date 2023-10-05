from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car, Booking, Review
from .forms import BookingForm, ReviewForm

def index(request):
    cars = Car.objects.filter(is_available=True)
    return render(request, 'index.html', {'cars': cars})

def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    reviews = Review.objects.filter(car=car)
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

