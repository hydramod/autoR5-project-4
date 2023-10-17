from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/book/', views.book_car, name='book_car'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('car/<int:car_id>/review/', views.leave_review, name='leave_review'),
    path('cars_list/', views.cars_list, name='cars_list'),
    path('contact/', views.contact, name='contact'),
    path('customer_dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('get_car_makes/', views.get_car_makes, name='get_car_makes'),
    path('get_car_models/', views.get_car_models, name='get_car_models'),
    path('get_car_years/', views.get_car_years, name='get_car_years'),
    path('get_car_locations/', views.get_car_locations, name='get_car_locations'),
    path('get_car_types/', views.get_car_types, name='get_car_types'),
    path('get_fuel_types/', views.get_fuel_types, name='get_fuel_types'),
]