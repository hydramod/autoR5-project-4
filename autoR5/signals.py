from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CancellationRequest, Booking, Payment, Car
import stripe
from django.contrib.auth.models import User


class RefundProcessingError(Exception):
    pass

# Signal receiver to create a user profile when a new user is registered
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Signal receiver to process cancellation requests
@receiver(post_save, sender=CancellationRequest)
def process_cancellation_request(sender, instance, created, **kwargs):
    if instance.approved:
        try:
            booking = Booking.objects.get(id=instance.booking_id)

            # Retrieve the payment intent associated with the payment
            payment = Payment.objects.get(booking=booking)
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
        except (stripe.error.StripeError, Booking.DoesNotExist, Payment.DoesNotExist):
            raise RefundProcessingError('Error processing refund')
