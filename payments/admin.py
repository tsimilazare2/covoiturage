from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('booking', 'amount', 'method', 'status', 'phone_number', 'created_at')
    list_filter = ('method', 'status', 'created_at')
    search_fields = ('booking__client__username', 'phone_number', 'transaction_reference')
    readonly_fields = ('created_at', 'updated_at', 'transaction_reference')
