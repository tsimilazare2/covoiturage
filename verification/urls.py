from django.urls import path

from . import views

app_name = 'verification'

urlpatterns = [
    path('chauffeur/', views.driver_onboarding, name='driver_onboarding'),
]
