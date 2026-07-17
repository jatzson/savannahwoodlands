from django.db import models
from django.urls import reverse
import uuid


class Registration(models.Model):
    TICKET_TYPES = [
        ('ticket', 'Ticket - ₦35,000'),
        ('vendor', 'Vendorship Participation - ₦250,000'),
    ]
    PAYMENT_STATUS = [
        ('pending', 'Pending Payment'),
        ('confirmed', 'Payment Confirmed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPES, default='ticket')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    registered_at = models.DateTimeField(auto_now_add=True)
    ticket_number = models.CharField(max_length=20, unique=True, blank=True)
    qr_code = models.ImageField(upload_to='tickets/qr/', blank=True)

    def save(self, *args, **kwargs):
        if not self.ticket_number:
            prefix = 'VND' if self.ticket_type == 'vendor' else 'TKT'
            short = str(self.id).upper()[:8]
            self.ticket_number = f'SW-{prefix}-{short}'
        super().save(*args, **kwargs)
        # QR code is only generated once payment has been confirmed by staff,
        # so a scannable ticket never exists before the payment is verified.
        if self.payment_status == 'confirmed' and not self.qr_code:
            self._generate_qr()

    def _generate_qr(self):
        import qrcode
        import io
        from django.core.files.base import ContentFile

        data = (
            f"Savannah Woodlands\n"
            f"Abuja Buy and Sell Property Event\n"
            f"Ticket: {self.ticket_number}\n"
            f"Name: {self.full_name}\n"
            f"Type: {self.get_ticket_type_display()}\n"
            f"Date: 26th September 2026, 12pm\n"
            f"Venue: Chelsea Hotels, Mohammadu Buhari Way, Central Area Abuja"
        )
        qr = qrcode.QRCode(version=1, box_size=10, border=4)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color='#1a3a2e', back_color='white')
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        self.qr_code.save(f'{self.ticket_number}.png', ContentFile(buf.getvalue()), save=True)

    def get_ticket_price(self):
        return '₦250,000' if self.ticket_type == 'vendor' else '₦35,000'

    def __str__(self):
        return f'{self.ticket_number} - {self.full_name}'


class VendorApplication(models.Model):
    DESIGNATION_CHOICES = [
        ('owner', 'Owner'),
        ('mandate', 'Mandate'),
        ('developer', 'Developer'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE, related_name='vendor_application')
    designation = models.CharField(max_length=20, choices=DESIGNATION_CHOICES)
    company_name = models.CharField(max_length=200, verbose_name='Company / Owner / Developer Name')
    property_type = models.CharField(max_length=200, verbose_name='Type of Property')
    location = models.CharField(max_length=300, verbose_name='Property Location')
    title = models.CharField(max_length=200, verbose_name='Title / Document Type', help_text='e.g. C of O, R of O, Deed of Assignment')
    open_market_price = models.CharField(max_length=100, verbose_name='Open Market Price')
    event_only_price = models.CharField(max_length=100, verbose_name='Event Only Price')
    additional_notes = models.TextField(blank=True, verbose_name='Additional Notes')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Vendor: {self.registration.full_name} — {self.company_name}'


def vendor_media_path(instance, filename):
    return f'vendor_media/{instance.vendor_application.registration.ticket_number}/{filename}'


class VendorMedia(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    vendor_application = models.ForeignKey(VendorApplication, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to=vendor_media_path)
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.media_type} for {self.vendor_application}'


class ContactMessage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-submitted_at']

    def __str__(self):
        return f'{self.full_name} — {self.submitted_at:%d %b %Y}'


class Property(models.Model):
    PROPERTY_TYPES = [
        ('land', 'Land'),
        ('agricultural_land', 'Agricultural Land'),
        ('duplex', 'Duplex'),
        ('detached_house', 'Detached House'),
        ('bungalow', 'Bungalow'),
        ('terrace', 'Terrace House'),
        ('apartment', 'Apartment / Flat'),
        ('commercial', 'Commercial Property'),
    ]
    STATUS_CHOICES = [
        ('for_sale', 'For Sale'),
        ('new_development', 'New Development'),
        ('under_offer', 'Under Offer'),
        ('sold', 'Sold'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    property_type = models.CharField(max_length=30, choices=PROPERTY_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='for_sale')
    location = models.CharField(max_length=300)
    description = models.TextField(blank=True)
    bedrooms = models.PositiveIntegerField(blank=True, null=True)
    bathrooms = models.PositiveIntegerField(blank=True, null=True)
    size = models.CharField(max_length=100, blank=True, help_text='e.g. 650 sqm, 2 plots')
    price = models.CharField(max_length=100, blank=True, help_text='e.g. ₦45,000,000')
    price_on_request = models.BooleanField(default=False)
    main_image = models.ImageField(upload_to='properties/main/')
    is_featured = models.BooleanField(default=False, help_text='Show this property on the homepage')
    is_active = models.BooleanField(default=True, help_text='Uncheck to hide without deleting')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title

    def get_display_price(self):
        if self.price_on_request or not self.price:
            return 'Price on request'
        return self.price

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.pk})


def property_media_path(instance, filename):
    return f'properties/media/{instance.property.pk}/{filename}'


class PropertyMedia(models.Model):
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]
    VIDEO_EXTENSIONS = ('.mp4', '.mov', '.webm', '.avi', '.mkv', '.m4v')

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='media_files')
    file = models.FileField(upload_to=property_media_path, help_text='Upload a photo or a video clip')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPES, blank=True)
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0, help_text='Lower numbers appear first')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'uploaded_at']

    def save(self, *args, **kwargs):
        if not self.media_type and self.file:
            name = self.file.name.lower()
            self.media_type = 'video' if name.endswith(self.VIDEO_EXTENSIONS) else 'image'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.get_media_type_display()} for {self.property.title}'