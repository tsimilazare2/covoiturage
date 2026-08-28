from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('client', 'trip_offer', 'nombre_places', 'montant_total', 'statut', 'payment_method', 'created_at')
    list_filter = ('statut', 'payment_method', 'created_at')
    search_fields = ('client__username', 'trip_offer__route__point_depart', 'trip_offer__route__destination')
    readonly_fields = ('created_at', 'updated_at')
