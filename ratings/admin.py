from django.contrib import admin
from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('client', 'driver', 'score', 'created_at')
    list_filter = ('score', 'created_at')
    search_fields = ('client__username', 'driver__username')
    readonly_fields = ('created_at',)
