from django.contrib import admin
from .models import Route


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('name', 'point_depart', 'destination', 'prix', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'point_depart', 'destination')
