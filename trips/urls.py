from django.urls import path
from . import views

app_name = 'trips'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('.', views.dashboard, name='dashboard_legacy'),
    path('publish/', views.publish_trip, name='publish'),
]
