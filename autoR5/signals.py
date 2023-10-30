"""
Imported modules and classes for handling payments and
user-related operations.

This module includes imports for handling payments using Stripe,
as well as signals and models related to user operations.

Modules:
- stripe: Provides functionality for processing payments
through Stripe.
- django.db.models.signals: Contains signals to trigger actions
on specific model events.
- django.dispatch: Enables the creation and handling of
custom signals.
- django.contrib.auth.models.User: Provides the User model
for user management.

Custom Classes:
- CancellationRequest: Model for handling cancellation requests.
- Booking: Model for managing car booking information.
- Payment: Model for recording payment details.
- UserProfile: Model for extending user profiles.

Usage:
The imported modules and classes are used throughout the
project to facilitate payment processing, user-related
operations, and data modeling.

Returns:
None
"""
import stripe
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import CancellationRequest, Booking, Payment, UserProfile


class RefundProcessingError(Exception):
    """
    Custom exception for handling refund processing errors.

    This exception is raised when there is an error during
    the processing of a refund transaction. It allows for more
    specific error handling in scenarios where refunds encounter
    issues.

    Attributes:
    - None

    Usage:
    This exception class is used to raise errors when refund processing
    encounters issues and may be caught and handled to provide more detailed
    feedback to users or log the error for debugging.

    Returns:
    None
    """


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function for creating a user profile upon user creation.

    This function is a signal receiver that is triggered when a new user is
    created.
    Upon user creation, it creates a corresponding user profile.

    Args:
        sender: The sender of the signal.
        instance: The instance of the User model being created.
        created: A boolean indicating whether the User instance is created.
        **kwargs: Additional keyword arguments.

    Returns:
        None

    Usage:
    This function is connected to the post-save signal of the User model
    and is responsible for creating a user profile associated with the newly
    created user. It is automatically called when a new user is registered.
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=CancellationRequest)
def process_cancellation_request(sender, instance, created, **kwargs):
    """
    Signal receiver function for creating a user profile upon user creation.

    This function is a signal receiver that is triggered when a new user
    is created. Upon user creation, it creates a corresponding user profile.

    Args:
        sender: The sender of the signal.
        instance: The instance of the User model being created.
        created: A boolean indicating whether the User instance is created.
        **kwargs: Additional keyword arguments.

    Returns:
        None

    Usage:
    This function is connected to the post-save signal of the User model and
    is responsible for creating a user profile associated with the newly
    created user. It is automatically called when a new user is registered.
    """
    if instance.approved:
        try:
            booking = Booking.objects.get(id=instance.booking_id)
            payment = Payment.objects.get(booking=booking)

            if payment.payment_status != 'Paid':
                booking.status = 'Canceled'
                booking.save()
                payment.payment_status = 'Canceled'
                payment.save()
                car = booking.car
                car.is_available = True
                car.save()
                return

            # Retrieve the payment intent associated with the payment
            payment_intent_id = payment.payment_intent
            car = booking.car

            # Create a refund with Stripe
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id
            )

            # Check the refund status and handle accordingly
            if refund.status == 'succeeded':
                payment.payment_status = 'Refunded'
                payment.save()
                booking.status = 'Canceled'
                booking.save()
                car.is_available = True
                car.save()
            else:
                raise RefundProcessingError('Refund processing failed')
        except (
                stripe.error.StripeError,
                Booking.DoesNotExist,
                Payment.DoesNotExist):
            raise RefundProcessingError('Error processing refund')
