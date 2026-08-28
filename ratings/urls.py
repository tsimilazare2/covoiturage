from django.urls import path
from . import views

app_name = 'ratings'

urlpatterns = [
    path('noter/<int:booking_id>/', views.rate_driver, name='rate_driver'),
    path('recues/', views.ratings_received, name='ratings_received'),
]
