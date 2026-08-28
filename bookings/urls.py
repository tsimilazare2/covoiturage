from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('create/<int:trip_id>/', views.create_booking, name='create_booking'),
    path('confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
]
