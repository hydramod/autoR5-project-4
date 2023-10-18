from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from .models import Car, Booking, Review, UserProfile, Payment, Notification, CancellationRequest, Location
from .forms import CsvImportForm
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import csv


class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'license_plate', 'daily_rate',
                    'is_available', 'latitude', 'longitude', 'location_name')
    list_filter = ('make', 'model', 'year', 'is_available', 'location_name')
    search_fields = ('make', 'model', 'year', 'location_name')

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
                        if len(fields) == 14:
                            make, model, year, license_plate, daily_rate, is_available, latitude, longitude, location_name, image, features, car_type, fuel_type, end, = [
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
                                    'location_name': location_name,
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
            'Latitude', 'Longitude', 'Location Name', 'Image', 'Features',
            'Car Type', 'Fuel Type'
        ])

        cars = Car.objects.all()
        for car in cars:
            writer.writerow([
                car.make, car.model, car.year, car.license_plate, car.daily_rate,
                'TRUE' if car.is_available else 'FALSE', car.latitude, car.longitude,
                car.location_name, car.image, car.features, car.car_type, car.fuel_type
            ])

        return response

    export_csv.short_description = "Export CSV"


class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'car', 'rental_date',
                    'return_date', 'total_cost', 'status')
    list_filter = ('user', 'car', 'rental_date', 'return_date', 'status')
    search_fields = ('user__username', 'car__make', 'car__model', 'car__year')


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('car', 'user', 'rating', 'comment')
    list_filter = ('car', 'user', 'rating')
    search_fields = ('car__make', 'car__model', 'user__username')


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number')
    search_fields = ('user__username', 'phone_number')


class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'booking', 'amount', 'payment_date',
                    'payment_method', 'payment_status')
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
