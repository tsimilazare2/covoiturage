from django.contrib import admin
from .models import TripOffer


@admin.register(TripOffer)
class TripOfferAdmin(admin.ModelAdmin):
    list_display = ('driver', 'route', 'date_depart', 'heure_depart', 'places_disponibles', 'places_totales', 'prix_unitaire', 'statut')
    list_filter = ('statut', 'date_depart')
    search_fields = ('driver__username', 'route__point_depart', 'route__destination')
