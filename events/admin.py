from django.contrib import admin
from .models import Registration, VendorApplication, VendorMedia


class VendorMediaInline(admin.TabularInline):
    model = VendorMedia
    extra = 0
    readonly_fields = ['file', 'media_type', 'uploaded_at']


@admin.register(VendorApplication)
class VendorApplicationAdmin(admin.ModelAdmin):
    list_display = ['get_name', 'designation', 'company_name', 'property_type', 'location', 'open_market_price', 'event_only_price', 'submitted_at']
    list_filter = ['designation', 'submitted_at']
    search_fields = ['company_name', 'location', 'registration__full_name']
    inlines = [VendorMediaInline]

    def get_name(self, obj):
        return obj.registration.full_name
    get_name.short_description = 'Registrant'


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'full_name', 'email', 'phone', 'ticket_type', 'registered_at']
    list_filter = ['ticket_type', 'registered_at']
    search_fields = ['full_name', 'email', 'ticket_number', 'phone']
    readonly_fields = ['id', 'ticket_number', 'qr_code', 'registered_at']
    ordering = ['-registered_at']