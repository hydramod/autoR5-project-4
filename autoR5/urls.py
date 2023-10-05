from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('car/<int:car_id>/', views.car_detail, name='car_detail'),
    path('car/<int:car_id>/book/', views.book_car, name='book_car'),
    path('booking/<int:booking_id>/confirmation/', views.booking_confirmation, name='booking_confirmation'),
    path('car/<int:car_id>/review/', views.leave_review, name='leave_review'),
]
