from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('booking/<int:booking_id>/', views.payment_page, name='payment_page'),
]
