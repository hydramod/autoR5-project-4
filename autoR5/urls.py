"""
URL patterns and view imports for the 'autoR5' Django
web application.

This import statement includes the necessary modules and views
for defining URL patterns in the 'autoR5' Django web application.

- 'django.urls.path' is used to define URL patterns.
- '.views' refers to the views module within the 'autoR5'
application.

Usage:
This import statement is typically used within the Django 'urls.py'
file to define the URL patterns for the 'autoR5' application. The
URL patterns connect specific URLs to views that handle the
corresponding web pages or functionality of the application.
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/book/', views.book_car, name='book_car'),
    path('booking/<int:booking_id>/confirmation/',
         views.booking_confirmation, name='booking_confirmation'),
    path('car/<int:car_id>/review/', views.leave_review, name='leave_review'),
    path('cars_list/', views.cars_list, name='cars_list'),
    path('contact/', views.contact, name='contact'),
    path('dashboard/', views.dashboard,
         name='dashboard'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('get_car_makes/', views.get_car_makes, name='get_car_makes'),
    path('get_car_models/', views.get_car_models, name='get_car_models'),
    path('get_car_years/', views.get_car_years, name='get_car_years'),
    path('get_car_locations/', views.get_car_locations,
         name='get_car_locations'),
    path('get_car_types/', views.get_car_types, name='get_car_types'),
    path('get_fuel_types/', views.get_fuel_types, name='get_fuel_types'),
    path('car/<int:car_id>/book/<int:booking_id>/checkout/',
         views.checkout, name='checkout'),
    path('delete_booking/<int:booking_id>/',
         views.delete_booking, name='delete_booking'),
    path('approve_reject_cancellation_request/<int:request_id>/<str:action>/',
         views.approve_reject_cancellation_request,
         name='approve_reject_cancellation_request'),
]
