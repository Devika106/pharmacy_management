from django.contrib import admin
from .models import Medicine, Billing

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_number', 'price', 'quantity', 'expiry_date')
    search_fields = ('name', 'batch_number')
    list_filter = ('expiry_date',)

@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ('customer', 'medicine', 'quantity', 'total_price', 'date')
    search_fields = ('customer',)
    list_filter = ('date',)
