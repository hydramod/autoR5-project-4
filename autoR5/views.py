from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Car, Booking, Review, CancellationRequest, Payment
from .forms import BookingForm, ReviewForm, ContactForm, CancellationRequestForm, UserProfileForm
from datetime import date
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.translation import gettext as _
from django.http import JsonResponse
import stripe
from django.conf import settings
from .signals import RefundProcessingError

# View for the home page
def index(request):
    # Retrieve unique car types and fuel types
    car_types = Car.objects.values_list(
        'car_type', flat=True).distinct().exclude(car_type=None)
    fuel_types = Car.objects.values_list(
        'fuel_type', flat=True).distinct().exclude(fuel_type=None)
    return render(request, 'index.html', {'car_types': car_types, 'fuel_types': fuel_types})

# View for the contact page
def contact(request):
    return render(request, 'contact.html')

# View for listing cars
def cars_list(request):
    cars = Car.objects.all()

    # Get filter parameters from the URL
    make = request.GET.get('make')
    model = request.GET.get('model')
    year = request.GET.get('year')
    location = request.GET.get('location')
    car_type = request.GET.get('car_type')
    fuel_type = request.GET.get('fuel_type')

    filters = {}
    if make:
        filters['make'] = make
    if model:
        filters['model'] = model
    if year:
        filters['year'] = year
    if location:
        filters['location_city'] = location
    if car_type:
        filters['car_type'] = car_type
    if fuel_type:
        filters['fuel_type'] = fuel_type

    filtered_cars = Car.objects.filter(**filters)

    all_cars = filtered_cars if make or model or year or location or car_type or fuel_type else cars

    # Retrieve filter options
    makes = Car.objects.values('make').distinct()
    models = Car.objects.values('model').distinct()
    years = Car.objects.values('year').distinct()
    locations = Car.objects.values('location_city').distinct()
    car_types = Car.CAR_TYPES
    fuel_types = Car.FUEL_TYPES

    # Paginate the results
    page_number = request.GET.get('page')
    paginator = Paginator(all_cars, 8)

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return render(request, 'cars_list.html', {
        'cars': page,
        'makes': makes,
        'models': models,
        'years': years,
        'locations': locations,
        'car_types': car_types,
        'fuel_types': fuel_types,
        'make': make,
        'model': model,
        'year': year,
        'location': location,
        'car_type': car_type,
        'fuel_type': fuel_type
    })

# View to get car makes through AJAX
def get_car_makes(request):
    car_makes = Car.objects.values('make').distinct()
    make_options = [{'value': make['make'], 'text': make['make']}
                    for make in car_makes]
    return JsonResponse(make_options, safe=False)

# View to get car models through AJAX
def get_car_models(request):
    selected_make = request.GET.get('make')
    car_models = Car.objects.filter(
        make=selected_make).values('model').distinct()
    model_options = [{'value': model['model'], 'text': model['model']}
                     for model in car_models]
    return JsonResponse(model_options, safe=False)

# View to get car years through AJAX
def get_car_years(request):
    selected_model = request.GET.get('model')
    car_years = Car.objects.filter(
        model=selected_model).values('year').distinct()
    year_options = [{'value': year['year'], 'text': year['year']}
                    for year in car_years]
    return JsonResponse(year_options, safe=False)

# View to get car types through AJAX
def get_car_types(request):
    selected_year = request.GET.get('year')
    car_types = Car.objects.filter(
        year=selected_year).values('car_type').distinct()
    car_type_options = [{'value': car_type['car_type'], 'text': get_display_value(
        Car.CAR_TYPES, car_type['car_type'])} for car_type in car_types]
    return JsonResponse(car_type_options, safe=False)

# View to get fuel types through AJAX
def get_fuel_types(request):
    selected_car_type = request.GET.get('car_type')
    fuel_types = Car.objects.filter(
        car_type=selected_car_type).values('fuel_type').distinct()
    fuel_type_options = [{'value': fuel_type['fuel_type'], 'text': get_display_value(
        Car.FUEL_TYPES, fuel_type['fuel_type'])} for fuel_type in fuel_types]
    return JsonResponse(fuel_type_options, safe=False)

# Function to get the display value for a choice key
def get_display_value(choices, choice_key):
    for choice in choices:
        if choice[0] == choice_key:
            return choice[1]
    return choice_key

# View to get car locations through AJAX
def get_car_locations(request):
    car_locations = Car.objects.values('location_city').distinct()
    location_options = [{'value': location['location_city'],
                         'text': location['location_city']} for location in car_locations]
    return JsonResponse(location_options, safe=False)

# View for displaying car details
def car_detail(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    reviews = Review.objects.filter(car=car, approved=True)
    return render(request, 'car_detail.html', {'car': car, 'reviews': reviews})

# View for booking a car
@login_required
def book_car(request, car_id):
    car = get_object_or_404(Car, pk=car_id)
    total_cost = None

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.location = car.location_city

            today = date.today()
            rental_date = booking.rental_date.date()
            if rental_date < today:
                messages.error(request, 'You cannot book for a past date.')
                return redirect('book_car', car_id=car_id)

            # Check for conflicting bookings with the same car and overlapping date ranges
            conflicting_bookings = Booking.objects.filter(
                Q(car=car) &
                (
                    Q(rental_date__range=(booking.rental_date, booking.return_date)) |
                    Q(return_date__range=(booking.rental_date, booking.return_date))
                )
            )

            # Check if any of the conflicting bookings have a return date in the future and the car is not available
            if conflicting_bookings.filter(return_date__gt=timezone.now()).exclude(car__is_available=True).exists():
                messages.error(
                    request, 'This car is already booked for the selected dates.')
                return redirect('book_car', car_id=car_id)

            booking.calculate_total_cost()
            booking.status = 'Pending'
            booking.save()
            total_cost = booking.total_cost

            payment = Payment(
                user=request.user,
                booking=booking,
                amount=booking.total_cost,
                payment_method='Stripe',
                payment_status='Pending',
            )
            payment.save()
            return redirect('checkout', car_id=booking.car.id, booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'book_car.html', {'car': car, 'form': form, 'total_cost': total_cost})


# Initialize Stripe API key
stripe.api_key = settings.STRIPE_SECRET_KEY

# View for the checkout process
@login_required
def checkout(request, car_id, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY

    try:
        intent = stripe.PaymentIntent.create(
            amount=int(booking.total_cost * 100),
            currency='eur',
            metadata={'booking_id': booking.id},
        )

        return render(request, 'checkout.html', {
            'intent_client_secret': intent.client_secret,
            'stripe_publishable_key': stripe_publishable_key,
            'booking_id': booking_id,
            'total_cost': booking.total_cost
        })

    except stripe.error.StripeError as e:
        print("Stripe Error:", str(e))
        messages.error(request, "Payment processing error. Please try again")
        return redirect('checkout')

# View for booking confirmation
@login_required
def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)

    payment_intent_id = request.GET.get("payment_intent")
    intent_client_secret = request.GET.get("payment_intent_client_secret")

    payment = Payment.objects.get(booking=booking)
    car = booking.car

    if intent_client_secret:
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
        except stripe.error.StripeError as e:
            messages.error(
                request, "Payment processing error. Please try again")
            return redirect('checkout')

        payment_intent_status = intent.status

        if payment_intent_status == 'succeeded':
            payment.payment_status = 'Paid'
            booking.status = 'Confirmed'
            payment.payment_intent = payment_intent_id
            car.is_available = False
            messages.success(request, "Payment successful")
        elif payment_intent_status in ['processing', 'requires_payment_method']:
            payment.payment_status = 'Pending'
            booking.status = 'Pending'
            payment.payment_intent = payment_intent_id
            messages.info(request, "Processing Payment")
        else:
            payment.payment_status = 'Failed'
            booking.status = 'Canceled'
            messages.error(request, "Payment failed")

        car.save()
        payment.save()
        booking.save()

    car = booking.car
    location_address = car.location_address
    location_lat = car.latitude
    location_long = car.longitude
    total_cost = booking.total_cost
    return render(request, 'booking_confirmation.html', {
        'booking': booking,
        'location_address': location_address,
        'location_lat': location_lat,
        'location_long': location_long,
        'total_cost': total_cost,
        'payment_intent_id': payment_intent_id,
        'payment_status': payment.payment_status
    })

# View for leaving a review
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

# View for the customer dashboard
@login_required
def customer_dashboard(request):
    user = request.user
    current_bookings = Booking.objects.filter(
        Q(status='Pending') | Q(status='Confirmed'),
        user=user, 
        return_date__gte=timezone.now()
    )
    past_bookings = Booking.objects.filter(
        Q(status='Completed'),
        user=user, 
        return_date__lt=timezone.now()
    )
    reviews = Review.objects.filter(user=user)
    form = CancellationRequestForm(request.POST or None)
    unapproved_requests = {}

    if request.method == 'POST' and form.is_valid():
        booking_id = request.POST.get('booking_id')
        if booking_id is not None:
            booking = Booking.objects.get(id=booking_id)

            # Check if there is an unapproved cancellation request
            unapproved_request = CancellationRequest.objects.filter(
                booking=booking, approved=False
            ).first()

            if unapproved_request:
                messages.error(request, 'Cannot request cancellation. There is a pending cancellation request.')
            else:
                cancellation_request = form.save(commit=False)
                cancellation_request.booking = booking
                cancellation_request.user = user
                cancellation_request.save()
                messages.success(request, 'Cancellation request submitted successfully')
        return redirect('customer_dashboard')

    return render(request, 'customer_dashboard.html', {
        'user': user,
        'current_bookings': current_bookings,
        'past_bookings': past_bookings,
        'reviews': reviews,
        'form': form,
        'unapproved_requests': unapproved_requests,
    })

# View for editing user profile
@login_required
def edit_profile(request):
    user_profile = request.user.userprofile

    if request.method == 'POST':
        form = UserProfileForm(
            request.POST, request.FILES, instance=user_profile)

        if form.is_valid():
            new_phone_number = form.cleaned_data.get('phone_number')
            new_profile_picture = form.cleaned_data.get('profile_picture')

            if new_phone_number or new_profile_picture:
                if new_phone_number:
                    user_profile.phone_number = new_phone_number
                if new_profile_picture:
                    user_profile.profile_picture = new_profile_picture

                user_profile.save()
            return redirect('customer_dashboard')
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'form': form})

# View for contacting the site administrators
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            messages.success(
                request, 'Thanks for getting in touch. One of our representatives will contact you soon')
        else:
            messages.error(
                request, 'Oops...! There was a problem submitting your request.')

    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
