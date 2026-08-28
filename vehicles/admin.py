from django.contrib import admin
from .models import Vehicle, VehicleDocument


@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('owner', 'make', 'model', 'plate_number', 'seats', 'is_verified')
    list_filter = ('is_verified', 'make')
    search_fields = ('owner__username', 'plate_number', 'make', 'model')


@admin.register(VehicleDocument)
class VehicleDocumentAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'doc_type', 'number', 'expiry_date')
    search_fields = ('vehicle__plate_number', 'number', 'doc_type')
