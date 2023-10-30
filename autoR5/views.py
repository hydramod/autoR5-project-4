"""
Imports necessary modules, libraries, functions, and
classes for the 'autoR5' Django web application.

- 'stripe' for payment processing functionality.
- 'date' and 'timedelta' from 'datetime' for handling
    date and time operations.
- 'render', 'redirect', 'get_object_or_404', 'reverse' from
    'django.shortcuts' for rendering templates, redirection,
    and handling 404 errors.
- 'login_required' from 'django.contrib.auth.decorators'
for requiring authentication to access views.
- 'messages' from 'django.contrib' for displaying
messages to users.
- 'timezone' from 'django.utils' for handling time zones.
- 'Q' from 'django.db.models' for complex database queries.
- 'HttpResponseRedirect', 'HttpResponse' from 'django.http'
for HTTP responses.
- 'Paginator', 'EmptyPage', 'PageNotAnInteger' from
'django.core.paginator' for paginating querysets.
- 'gettext as _' from 'django.utils.translation' for
translation purposes.
- 'JsonResponse' from 'django.http' for handling JSON responses.
- 'settings' from 'django.conf' for accessing project settings.
- 'Car', 'Booking', 'Review', 'CancellationRequest', 'Payment',
'ContactFormSubmission' from '.models' for accessing model classes.
- 'BookingForm', 'ReviewForm', 'ContactForm', 'CancellationRequestForm',
'UserProfileForm' from '.forms' for accessing form classes.
- 'RefundProcessingError' from '.signals' for handling
refund processing errors.
"""
import stripe
from datetime import date, timedelta
from django.shortcuts import (render, redirect,
                              get_object_or_404)
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.paginator import (Paginator, EmptyPage,
                                   PageNotAnInteger)
from django.utils.translation import gettext as _
from django.http import JsonResponse
from django.conf import settings
from .models import (Car, Booking, Review,
                     CancellationRequest, Payment,
                     ContactFormSubmission)
from .forms import (BookingForm, ReviewForm, ContactForm,
                    CancellationRequestForm, UserProfileForm)
from .signals import RefundProcessingError


def index(request):
    """
    View for the home page of the 'autoR5' Django web application.

    Purpose:
    This view is responsible for rendering the home page of the
    application. It retrieves unique car types and fuel types
    from the database and passes them to the 'index.html'
    template for display.

    Args:
    - 'request': The HTTP request object sent by the user's
    browser.

    Returns:
    A rendered HTML response displaying the home page with
    unique car types and fuel types.

    Usage:
    This view is typically associated with the URL pattern for
    the home page and is called when a user accesses the
    application's main landing page.
    """
    car_types = Car.objects.values_list(
        'car_type', flat=True).distinct().exclude(car_type=None)
    fuel_types = Car.objects.values_list(
        'fuel_type', flat=True).distinct().exclude(fuel_type=None)
    return render(request, 'index.html',
                  {'car_types': car_types,
                   'fuel_types': fuel_types})


def cars_list(request):
    """
    View to display a list of cars in the 'autoR5' Django web application.

    Purpose:
    This view is responsible for rendering a list of available cars based
    on various filtering options provided in the query string of the
    request. It allows users to filter cars by make, model, year,
    location, car type, and fuel type, and displays paginated results.

    Args:
    - 'request': The HTTP request object sent by the user's browser,
    including any filter parameters in the query string.

    Returns:
    A rendered HTML response displaying the list of cars with applied
    filters and pagination.

    Usage:
    This view is typically associated with the URL pattern for the cars
    list page. Users can access this page to view and filter the available
    cars, and the results are displayed with pagination for a better user
    experience.
    """
    cars = Car.objects.filter(is_available=True)

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

    all_cars = filtered_cars if any([
        make, model, year, location,
        car_type, fuel_type])else cars

    makes = Car.objects.values('make').distinct()
    models = Car.objects.values('model').distinct()
    years = Car.objects.values('year').distinct()
    locations = Car.objects.values('location_city').distinct()
    car_types = Car.CAR_TYPES
    fuel_types = Car.FUEL_TYPES

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


def get_car_makes(request):
    """
    View to retrieve a list of unique car makes for filtering.

    Purpose:
    This view is used to fetch a list of distinct car makes from
    the database and convert them into JSON format. It is typically
    accessed through an AJAX request and is used to populate the
    available options for car makes in filter dropdowns.

    Args:
    - 'request': The HTTP request object, typically sent via an
    AJAX request.

    Returns:
    A JSON response containing a list of car makes in the form of
    key-value pairs.

    Usage:
    This view is called asynchronously when the user interacts with
    filter dropdowns on the front end. It provides the available
    options for car makes, which can be dynamically updated as
    users select different filter criteria.
    """
    car_makes = Car.objects.values('make').distinct().order_by('make')
    make_options = [{'value': make['make'], 'text': make['make']}
                    for make in car_makes]
    return JsonResponse(make_options, safe=False)


def get_car_models(request):
    """
    View to retrieve a list of unique car models for a selected
    car make.

    Purpose:
    This view is designed to fetch a list of distinct car models
    associated with a specific car make from the database and
    return them in JSON format. It is intended for use in response
    to an AJAX request and serves to populate the available options
    for car models in filter dropdowns based on the selected car make.

    Args:
    - 'request': The HTTP request object, typically sent via an
    AJAX request.

    Returns:
    A JSON response containing a list of car models in the form
    of key-value pairs.

    Usage:
    This view is utilized asynchronously in response to user interactions
    with filter dropdowns on the front end. It provides dynamic updates
    to the available car model options, ensuring that the options are
    relevant to the selected car make.
    """
    selected_make = request.GET.get('make')
    car_models = Car.objects.filter(make=selected_make).values(
        'model').distinct().order_by('model')
    model_options = [{'value': model['model'], 'text': model['model']}
                     for model in car_models]
    return JsonResponse(model_options, safe=False)


def get_car_years(request):
    """
    View to retrieve a list of unique car years for a selected car model.

    Purpose:
    This view is designed to retrieve a list of distinct car years
    associated with a specific car model from the database and return
    them in JSON format. It is intended for use in response to an AJAX
    request and serves to populate the available options for car years
    in filter dropdowns based on the selected car model.

    Args:
    - 'request': The HTTP request object, typically sent via an AJAX
    request.

    Returns:
    A JSON response containing a list of car years in the form of
    key-value pairs.

    Usage:
    This view is employed asynchronously in response to user interactions
    with filter dropdowns on the front end. It provides dynamic updates
    to the available car year options, ensuring that the options are
    relevant to the selected car model.
    """
    selected_model = request.GET.get('model')
    car_years = Car.objects.filter(model=selected_model).values(
        'year').distinct().order_by('year')
    year_options = [{'value': year['year'], 'text': year['year']}
                    for year in car_years]
    return JsonResponse(year_options, safe=False)


def get_car_types(request):
    """
    View to retrieve a list of unique car types through AJAX.

    Purpose:
    This view fetches a list of distinct car types from the database
    for a selected year and returns them in JSON format. It serves
    as an AJAX response to populate the available options for car
    types in filter dropdowns, allowing users to filter cars based
    on their type.

    Args:
    - 'request': The HTTP request object sent via an AJAX request.

    Returns:
    A JSON response containing a list of car types for the selected year.

    Usage:
    This view is used to update the car type options dynamically based on
    the year selected by the user in filter dropdowns on the front end. It
    ensures that users can filter cars by type effectively.
    """
    selected_year = request.GET.get('year')
    car_types = Car.objects.filter(
        year=selected_year).values('car_type').distinct()
    car_type_options = [{'value': car_type['car_type'],
                         'text': get_display_value(
                             Car.CAR_TYPES, car_type[
                                 'car_type'])}for car_type in car_types]
    return JsonResponse(car_type_options, safe=False)


def get_fuel_types(request):
    """
    View to retrieve a list of unique fuel types through AJAX.

    Purpose:
    This view retrieves a list of distinct fuel types from the
    database for a selected car type and returns them in JSON format.
    It serves as an AJAX response to populate the available options for
    fuel types in filter dropdowns, enabling users to filter cars based
    on their fuel type.

    Args:
    - 'request': The HTTP request object sent via an AJAX request.

    Returns:
    A JSON response containing a list of fuel types for the selected car type.

    Usage:
    This view is used to update the fuel type options dynamically based on
    the car type selected by the user in filter dropdowns on the front end.
    It ensures that users can filter cars by fuel type effectively.
    """
    selected_car_type = request.GET.get('car_type')
    fuel_types = Car.objects.filter(
        car_type=selected_car_type).values('fuel_type').distinct()
    fuel_type_options = [{'value': fuel_type['fuel_type'],
                          'text': get_display_value(
                              Car.FUEL_TYPES, fuel_type[
                                  'fuel_type'])} for fuel_type in fuel_types]
    return JsonResponse(fuel_type_options, safe=False)


def get_display_value(choices, choice_key):
    """
    Utility function to retrieve the display value for a given choice key.

    Purpose:
    This function is used to obtain the display value associated with a
    specific choice key from a list of choices. It is commonly used for
    converting choice keys into human-readable labels.

    Args:
    - 'choices': A list of choices, typically a tuple of
    (choice_key,display_value) pairs.

    - 'choice_key': The key for which the corresponding
    display value is required.

    Returns:
    The display value associated with the provided choice_key, or the
    choice_key itself if a matching choice is not found.

    Usage:
    This utility function is employed to translate choice keys into their
    respective display values, enhancing the readability of data in
    various parts of the application.
    """
    for choice in choices:
        if choice[0] == choice_key:
            return choice[1]
    return choice_key


def get_car_locations(request):
    """
    View to retrieve a list of unique car locations through AJAX.

    Purpose:
    This view is designed to fetch a list of distinct car locations
    (cities) from the database and return them in JSON format. It
    serves as an AJAX response to populate the available options for
    car locations in filter dropdowns, enabling users to filter cars
    based on their location.

    Args:
    - 'request': The HTTP request object sent via an AJAX request.

    Returns:
    A JSON response containing a list of car locations (cities) in
    the form of key-value pairs.

    Usage:
    This view is utilized in response to user interactions with filter
    dropdowns on the front end, ensuring that the options are
    dynamically updated based on the available car locations in the
    database.
    """
    car_locations = Car.objects.values(
        'location_city').distinct().order_by('location_city')
    location_options = [{'value': location['location_city'],
                         'text': location[
                             'location_city']} for location in car_locations]
    return JsonResponse(location_options, safe=False)


def car_detail(request, car_id):
    """
    View for displaying the details of a specific car.

    Purpose:
    This view retrieves and displays detailed information about a particular
    car, including its specifications and reviews. It is used to present a
    dedicated page for a single car's details.

    Args:
    - 'request': The HTTP request object sent by the client.
    - 'car_id': The unique identifier (primary key) of the car to be displayed.

    Returns:
    Renders the 'car_detail.html' template, providing the 'car' and 'reviews'
    context variables.

    Usage:
    This view is accessed when a user clicks on a car from the list of
    available cars. It fetches the car's information from the database and
    retrieves approved reviews for that car, allowing users to view the car's
    details and associated reviews.
    """
    car = get_object_or_404(Car, pk=car_id)
    reviews = Review.objects.filter(car=car, approved=True)
    return render(request, 'car_detail.html', {'car': car, 'reviews': reviews})


@login_required
def book_car(request, car_id):
    """
    View for booking a car.

    Purpose:
    This view handles the process of booking a specific car. It allows users
    to fill out a booking form, checks for availability, conflicts with other
    bookings, and calculates the total cost. Users can proceed to checkout
    and make a payment after booking.

    Args:
    - 'request': The HTTP request object sent by the client.
    - 'car_id': The unique identifier (primary key) of the car to be booked.

    Returns:
    Renders the 'book_car.html' template, providing the 'car', 'form',
    'total_cost', and 'bookedDates' context variables.

    Usage:
    1. A user accesses this view to book a car.

    2. The view checks the availability of the car, validates the booking
    form, and calculates the total cost.

    3. It also checks for any conflicting bookings or past booking dates.

    4. If the booking is successful, it proceeds to the checkout process
    for payment.

    Note:
    Only authenticated users can make bookings for cars.
    """
    car = get_object_or_404(Car, pk=car_id)
    total_cost = None

    confirmed_bookings = Booking.objects.filter(car=car, status='Confirmed')

    bookedDates = {}
    for booking in confirmed_bookings:
        current_date = booking.rental_date
        end_date = booking.return_date
        date_range = []
        while current_date <= end_date:
            date_str = current_date.strftime('%d-%m-%Y')
            date_range.append(date_str)
            current_date += timedelta(days=1)
        date_range_str = ' to '.join(date_range)
        bookedDates[booking.id] = date_range_str

    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.car = car
            booking.location = car.location_city

            if not car.is_available:
                messages.error(
                    request, 'This car is not available for booking.')
                return redirect('car_detail', car_id=car_id)

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
                        messages.error(
                            request, 'You cannot book for a past date.')
                        return redirect('book_car', car_id=car_id)

                    conflicting_bookings = Booking.objects.filter(
                        Q(car=car) &
                        (
                            Q(rental_date__range=(booking.rental_date,
                                                  booking.return_date)) |
                            Q(return_date__range=(
                                booking.rental_date, booking.return_date))
                        )
                    )

                    future_conflicting_bookings = conflicting_bookings.filter(
                        return_date__gt=timezone.now())

                    if future_conflicting_bookings.exists():
                        if future_conflicting_bookings.filter(
                                return_date__lt=booking.rental_date).exists():
                            pass
                        else:
                            messages.error(
                                request,
                                'This car is already booked for'
                                'the selected dates.')
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
            return redirect('checkout', car_id=car_id, booking_id=booking.id)
    else:
        form = BookingForm()

    return render(request, 'book_car.html', {'car': car,
                                             'form': form,
                                             'total_cost': total_cost,
                                             'bookedDates': bookedDates})


@login_required
def checkout(request, car_id, booking_id):
    """
    View for processing payments and checkout.

    Purpose:
    This view handles the payment processing and checkout for a specific
    booking. It uses the Stripe API to create a PaymentIntent, which allows
    users to make payments. If the payment is successful, the view displays
    the checkout page with payment details.

    Args:
    - 'request': The HTTP request object sent by the client.

    - 'car_id': The unique identifier (primary key) of the car being booked.

    - 'booking_id': The unique identifier (primary key) of the booking being
    checked out.

    Returns:
    Renders the 'checkout.html' template, providing context variables such as
    'intent_client_secret', 'stripe_publishable_key', 'booking_id', and
    'total_cost'.

    Usage:
    1. A user initiates the checkout process after booking a car.

    2. The view uses the Stripe API to create a PaymentIntent, allowing the
    user to make a payment.

    3. If the payment is successful, the checkout page is displayed with
    relevant payment details.

    4. In case of a Stripe error or payment processing issue, an error message
    is shown, and the user is redirected back to the checkout page.

    Note:
    Only authenticated users can make payments for cars.
    """
    booking = get_object_or_404(Booking, pk=booking_id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
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
        return redirect('checkout', car_id=car_id, booking_id=booking.id)


@login_required
def booking_confirmation(request, booking_id):
    """
    View for confirming a booking and displaying booking details.

    Purpose:
    This view handles the confirmation of a booking and displays
    relevant booking details to the user. It also processes the payment
    status based on the Stripe payment intent.

    Args:
    - 'request': The HTTP request object sent by the client.

    - 'booking_id': The unique identifier (primary key) of the booking
    to be confirmed.

    Returns:
    Renders the 'booking_confirmation.html' template, providing context
    variables such as 'booking', 'location_address', 'location_lat',
    'location_long', 'total_cost', 'payment_intent_id', and
    'payment_status'.

    Usage:
    1. A user proceeds to confirm their booking.

    2. The view retrieves booking and payment information.

    3. If a valid payment intent is provided, the payment status is updated
    based on the intent status ('succeeded', 'processing', or
    'requires_payment_method').

    4. Appropriate messages are displayed to the user regarding the payment
    status.

    5. Booking details, location information, and payment status are presented
    on the booking confirmation page.

    Note:
    Only authenticated users view bookings for cars.
    """
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
            return redirect('checkout',
                            car_id=booking.car.id,
                            booking_id=booking_id)

        payment_intent_status = intent.status

        if payment_intent_status == 'succeeded':
            payment.payment_status = 'Paid'
            booking.status = 'Confirmed'
            payment.payment_intent = payment_intent_id
            messages.success(request, "Payment successful")
        elif payment_intent_status == 'processing':
            payment.payment_status = 'Pending'
            booking.status = 'Pending'
            payment.payment_intent = payment_intent_id
            messages.info(request, "Processing Payment")
        else:
            payment_intent_status == 'requires_payment_method'
            payment.payment_status = 'Failed'
            booking.status = 'Canceled'
            messages.error(request, "Payment failed")

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


@login_required
def leave_review(request, car_id):
    """
    View for leaving a review for a car.

    Purpose:
    This view allows authenticated users to leave a review for a specific car.
    It handles both the submission of new reviews and the rendering of the
    review submission form.

    Args:
    - 'request': The HTTP request object sent by the client.

    - 'car_id': The unique identifier (primary key) of the car for which the
    review is being submitted.

    Returns:
    Renders the 'leave_review.html' template, providing context variables
    such as 'car' and 'form'. The template includes a review submission form.

    Usage:
    1. A user, who is logged in, navigates to the page for leaving a review
    for a particular car.

    2. The view checks if the user is authenticated. If not, they are prompted
    to log in.

    3. If the request method is POST, it processes the form data and saves the
    review, associating it with the logged-in user and the selected car.

    4. Appropriate messages are displayed based on the outcome of the review
    submission (success or error).

    5. The review submission form is displayed, ready for user input.

    Note:
    Only authenticated users can leave reviews for cars.
    """
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
                request,
                'Oops...! There was a problem submitting your feedback.')
    else:
        form = ReviewForm()

    return render(request, 'leave_review.html', {'car': car, 'form': form})


@login_required
def customer_dashboard(request):
    """
    View for the customer dashboard.

    Purpose:
    This view provides a dashboard for authenticated users, particularly
    customers, to view and manage their bookings, reviews, and cancellation
    requests. It displays information on current bookings, past bookings,
    reviews, and any unapproved cancellation requests.

    Args:
    - 'request': The HTTP request object sent by the client.

    Returns:
    Renders the 'customer_dashboard.html' template, providing context
    variables including 'user', 'current_bookings', 'past_bookings',
    'reviews', 'form', and 'unapproved_requests'. The template displays
    relevant user data and booking-related information.

    Usage:
    1. An authenticated user (customer) accesses their customer dashboard.

    2. The view retrieves and organizes data related to the user's bookings,
    reviews, and cancellation requests.

    3. It checks for current and past bookings and filters unapproved
    cancellation requests associated with current bookings.

    4. If the request method is POST and a valid cancellation request is
    submitted, it processes the request and displays a success message.

    5. The dashboard template displays the user's information and relevant
    data, allowing them to manage their bookings, reviews, and cancellation
    requests.

    Note:
    - Only authenticated users can access the customer dashboard.
    - Users can submit cancellation requests for their bookings.
    """
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

    for booking in current_bookings:
        unapproved_request = CancellationRequest.objects.filter(
            booking=booking, approved=False
        ).first()
        if unapproved_request:
            unapproved_requests[booking.id] = unapproved_request

    if request.method == 'POST' and form.is_valid():
        booking_id = request.POST.get('booking_id')
        if booking_id is not None:
            booking = Booking.objects.get(id=booking_id)

            cancellation_request = form.save(commit=False)
            cancellation_request.booking = booking
            cancellation_request.user = user
            cancellation_request.save()
            messages.success(
                request, 'Cancellation request submitted successfully')
        return redirect('customer_dashboard')

    return render(request, 'customer_dashboard.html', {
        'user': user,
        'current_bookings': current_bookings,
        'past_bookings': past_bookings,
        'reviews': reviews,
        'form': form,
        'unapproved_requests': unapproved_requests,
    })


@login_required
def edit_profile(request):
    """
    View for editing the user profile.

    Purpose:
    This view allows authenticated users to edit their user profiles,
    including updating their phone number and profile picture. Users
    can choose to clear their profile picture as well.

    Args:
    - 'request': The HTTP request object sent by the client.

    Returns:
    Renders the 'edit_profile.html' template with context variables
    including 'form'. The template provides a form for editing the
    user's profile, allowing them to update their phone number and
    profile picture.

    Usage:
    1. An authenticated user accesses the edit profile page.

    2. The view retrieves the user's profile information and
    displays it in the edit profile form.

    3. If the request method is POST and the form is valid, the view
    processes any updates to the phone number and profile picture.

    4. Users can choose to clear their profile picture.

    5. Appropriate success, info, or error messages are displayed based
    on the outcomes of the updates.

    Note:
    - Only authenticated users can edit their profiles.
    - Users can update their phone number and profile picture.
    - Users can clear their profile picture.
    """
    user_profile = request.user.userprofile
    form = UserProfileForm(request.POST or None,
                           request.FILES, instance=user_profile)

    phone_updated = False
    picture_updated = False

    if request.method == 'POST':
        if form.is_valid():
            new_phone_number = form.cleaned_data['phone_number']
            new_profile_picture = form.cleaned_data['profile_picture_upload']

            if new_phone_number.strip() != "":
                if new_phone_number.isdigit():
                    user_profile.phone_number = new_phone_number
                    phone_updated = True

            if new_profile_picture:
                user_profile.profile_picture = new_profile_picture
                picture_updated = True

            if 'clear_picture' in request.POST and request.POST[
                    'clear_picture'] == 'on':
                if user_profile.profile_picture:
                    user_profile.profile_picture = None
                    picture_updated = True
                    messages.success(
                        request, 'Profile picture removed successfully.')

            if phone_updated:
                user_profile.save()
                messages.success(request, 'Phone number updated successfully.')
            if picture_updated:
                user_profile.save()
                messages.success(
                    request, 'Profile picture updated successfully.')
            elif not picture_updated and not phone_updated:
                messages.info(
                    request,
                    'No changes made to phone number or profile picture.')

        else:
            messages.error(
                request, 'Form contains errors. Please correct them.')

    return render(request, 'edit_profile.html', {'form': form})


def contact(request):
    """
    View for the contact page.

    Purpose:
    This view handles user submissions from the contact page, allowing users
    to send inquiries or messages to the website administrators.

    Args:
    - 'request': The HTTP request object sent by the client.

    Returns:
    Renders the 'contact.html' template with context variable 'form', which
    provides a form for users to submit their inquiries or messages.

    Usage:
    1. A user accesses the contact page to submit an inquiry or message.

    2. If the request method is POST and the form is valid, the view processes
    the form submission.

    3. The submitted data, including the first name, last name, email, subject,
    and message, are saved to the database as a 'ContactFormSubmission' object.

    4. A success message is displayed, indicating that the submission was
    successful, and the user is informed that a representative will contact
    them.

    5. Users are redirected back to the contact page after submission.

    6. If the request method is not POST (e.g., a GET request), the view
    renders the contact page with an empty form for submission.

    Note:
    - This view is used for submitting inquiries or messages to the website
    administrators.

    - It handles both POST requests (form submissions) and GET requests for
    rendering the contact page.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']

            # Save the submission to the database
            submission = ContactFormSubmission(
                first_name=first_name,
                last_name=last_name,
                email=email,
                subject=subject,
                message=message
            )
            submission.save()

            messages.success(
                request,
                'Thanks for getting in touch. One of our'
                'representatives will contact you soon.')

            # Redirect back to the contact page after submission
            return redirect('contact')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})
