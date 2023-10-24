from django.contrib import admin
from django.urls import path
from django.shortcuts import render
import csv
from geopy.geocoders import Nominatim
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib import messages

from .models import Car, Booking, Review, UserProfile, Payment, CancellationRequest, ContactFormSubmission
from .forms import CsvImportForm

# Geolocator for updating car locations
def update_location(modeladmin, request, queryset):
    geolocator = Nominatim(user_agent="autoR5")
    for car in queryset:
        location = geolocator.reverse([car.latitude, car.longitude])
        car.location_city = location.raw['address']['city']
        car.location_address = location.address
        car.save()


update_location.short_description = 'Update Location'


class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'license_plate', 'daily_rate',
                    'is_available', 'latitude', 'longitude', 'location_city')
    list_filter = ('make', 'model', 'year', 'is_available', 'location_city')
    search_fields = ('make', 'model', 'year', 'location_city')
    actions = [update_location]

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path('import_csv/', self.import_csv, name='import_csv'),
            path('export_csv/', self.export_csv, name='export_csv'),
        ]

        return new_urls + urls

    def import_csv(self, request):
        if request.method == "POST":
            form = CsvImportForm(request.POST, request.FILES)

            if form.is_valid():
                csv_file = form.cleaned_data['csv_import']

                if not csv_file.name.endswith('.csv'):
                    messages.error(
                        request, 'Invalid file format. Please upload a CSV file.')
                else:
                    file_data = csv_file.read().decode("utf-8")
                    csv_data = file_data.split("\n")

                    for i, row in enumerate(csv_data):
                        # Skip the first row (header)
                        if i == 0:
                            continue

                        fields = row.split(",")
                        if len(fields) == 15:
                            make, model, year, license_plate, daily_rate, is_available, latitude, longitude, location_city, location_address, image, features, car_type, fuel_type, end, = [
                                field.strip(' "') for field in fields]

                            # Handle empty fields by converting them to None
                            if not image:
                                image = None

                            is_available = is_available.strip(' "') == "TRUE"

                            car, created = Car.objects.update_or_create(
                                license_plate=license_plate,
                                defaults={
                                    'make': make,
                                    'model': model,
                                    'year': year,
                                    'daily_rate': daily_rate,
                                    'is_available': is_available,
                                    'latitude': latitude,
                                    'longitude': longitude,
                                    'location_city': location_city,
                                    'location_address': location_address,
                                    'image': image,
                                    'features': features,
                                    'car_type': car_type,
                                    'fuel_type': fuel_type,
                                }
                            )

                    messages.success(
                        request, 'CSV data imported successfully.')
                    url = reverse('admin:autoR5_car_changelist')
                    return HttpResponseRedirect(url)

        form = CsvImportForm()
        data = {"form": form}
        return render(request, "admin/csv_import.html", data)

    import_csv.short_description = "Import CSV file"

    def export_csv(self, request):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="car_data.csv"'

        writer = csv.writer(response)
        writer.writerow([
            'Make', 'Model', 'Year', 'License Plate', 'Daily Rate', 'Available',
            'Latitude', 'Longitude', 'Location City', 'Location Address', 'Image', 'Features',
            'Car Type', 'Fuel Type'
        ])

        cars = Car.objects.all()
        for car in cars:
            writer.writerow([
                car.make, car.model, car.year, car.license_plate, car.daily_rate,
                'TRUE' if car.is_available else 'FALSE', car.latitude, car.longitude,
                car.location_city, car.location_address, car.image, car.features, car.car_type, car.fuel_type
            ])

        return response

    export_csv.short_description = "Export CSV"


class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'car', 'rental_date',
                    'return_date', 'total_cost', 'status')
    list_filter = ('user', 'car', 'rental_date', 'return_date', 'status')
    search_fields = ('user__username', 'car__make', 'car__model', 'car__year')
    pass


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'comment')
    list_filter = ('car', 'user', 'rating')
    search_fields = ('car__make', 'car__model', 'user__username')
    pass


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'email')
    search_fields = ('user__username', 'phone_number')
    pass


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'amount', 'payment_date',
                    'payment_method', 'payment_status')
    list_filter = ('user', 'payment_date', 'payment_method', 'payment_status')
    search_fields = ('user__username', 'booking__id')
    pass


class CancellationRequestAdmin(admin.ModelAdmin):
    list_display = ('booking', 'user', 'request_date', 'reason')
    list_filter = ('user', 'request_date')
    search_fields = ('user__username', 'booking__id', 'reason')
    pass


class ContactFormSubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'subject')
    pass


# Register admin classes for models
admin.site.register(Car, CarAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(CancellationRequest, CancellationRequestAdmin)
admin.site.register(ContactFormSubmission, ContactFormSubmissionAdmin)
