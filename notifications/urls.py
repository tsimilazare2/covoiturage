from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.notifications_list, name='list'),
    path('<int:pk>/lire/', views.mark_as_read, name='mark_as_read'),
    path('tout-lire/', views.mark_all_as_read, name='mark_all_as_read'),
]
