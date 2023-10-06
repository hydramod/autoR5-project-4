from django.contrib import admin
from .models import Car, Booking, Review, UserProfile, Payment, Notification, CancellationRequest, Location

class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'license_plate', 'daily_rate', 'is_available', 'location')
    list_filter = ('make', 'model', 'year', 'is_available', 'location')
    search_fields = ('make', 'model', 'year', 'location')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'rental_date', 'return_date', 'total_cost')
    list_filter = ('user', 'car', 'rental_date', 'return_date')
    search_fields = ('user__username', 'car__make', 'car__model', 'car__year')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'comment')
    list_filter = ('car', 'user', 'rating')
    search_fields = ('car__make', 'car__model', 'user__username')

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'amount', 'payment_date', 'payment_method', 'payment_status')
    list_filter = ('user', 'payment_date', 'payment_method', 'payment_status')
    search_fields = ('user__username', 'booking__id')

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'is_read', 'created_at')
    list_filter = ('user', 'is_read', 'created_at')
    search_fields = ('user__username', 'message')

class CancellationRequestAdmin(admin.ModelAdmin):
    list_display = ('booking', 'user', 'request_date', 'reason')
    list_filter = ('user', 'request_date')
    search_fields = ('user__username', 'booking__id', 'reason')

class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'latitude', 'longitude')
    search_fields = ('name', 'address')

admin.site.register(Car, CarAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Notification, NotificationAdmin)
admin.site.register(CancellationRequest, CancellationRequestAdmin)
admin.site.register(Location, LocationAdmin)
