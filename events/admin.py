from django.contrib import admin
from .models import (
    Registration, VendorApplication, VendorMedia, ContactMessage,
    Property, PropertyMedia,
)


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


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'is_read', 'submitted_at']
    list_filter = ['is_read', 'submitted_at']
    search_fields = ['full_name', 'email', 'message']
    readonly_fields = ['id', 'full_name', 'email', 'phone', 'message', 'submitted_at']
    ordering = ['-submitted_at']


class PropertyMediaInline(admin.TabularInline):
    model = PropertyMedia
    extra = 3
    fields = ['file', 'media_type', 'caption', 'order']
    help_text = 'Add as many photos or video clips as you like — media_type is auto-detected from the file if left blank.'


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'status', 'location', 'price', 'media_count', 'is_featured', 'is_active', 'created_at']
    list_filter = ['property_type', 'status', 'is_featured', 'is_active']
    search_fields = ['title', 'location', 'description']
    list_editable = ['is_featured', 'is_active']
    inlines = [PropertyMediaInline]
    fieldsets = (
        (None, {'fields': ('title', 'property_type', 'status', 'location', 'description')}),
        ('Details', {'fields': ('bedrooms', 'bathrooms', 'size')}),
        ('Pricing', {'fields': ('price', 'price_on_request')}),
        ('Cover Photo', {'fields': ('main_image',), 'description': 'This is the thumbnail shown on listing cards. Add extra photos/videos below in the gallery.'}),
        ('Visibility', {'fields': ('is_featured', 'is_active')}),
    )

    def media_count(self, obj):
        return obj.media_files.count()
    media_count.short_description = 'Gallery Items'