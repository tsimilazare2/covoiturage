from django.contrib import admin
from .models import ClientVerification, DriverProfile


@admin.register(ClientVerification)
class ClientVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'expiry_date', 'submitted_at', 'reviewed_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'user__email', 'cni_number')


@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'cni_expiry', 'license_expiry', 'submitted_at', 'reviewed_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'user__email', 'cni_number', 'license_number')
