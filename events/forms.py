from django import forms
from .models import Registration, VendorApplication, ContactMessage, Property


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['full_name', 'email', 'phone', 'ticket_type']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': '+234 800 000 0000', 'class': 'form-input'}),
            'ticket_type': forms.RadioSelect(attrs={'class': 'ticket-radio'}),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'ticket_type': 'Participation Type',
        }


class VendorApplicationForm(forms.ModelForm):
    class Meta:
        model = VendorApplication
        fields = [
            'designation', 'company_name', 'property_type',
            'location', 'title', 'open_market_price',
            'event_only_price', 'additional_notes',
        ]
        widgets = {
            'designation': forms.RadioSelect(),
            'company_name': forms.TextInput(attrs={'placeholder': 'e.g. Greenfield Developers Ltd', 'class': 'form-input'}),
            'property_type': forms.TextInput(attrs={'placeholder': 'e.g. Residential Land, Commercial Plot, Duplex', 'class': 'form-input'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Gwarinpa, Abuja', 'class': 'form-input'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g. C of O, R of O, Deed of Assignment', 'class': 'form-input'}),
            'open_market_price': forms.TextInput(attrs={'placeholder': 'e.g. ₦45,000,000', 'class': 'form-input'}),
            'event_only_price': forms.TextInput(attrs={'placeholder': 'e.g. ₦38,000,000', 'class': 'form-input'}),
            'additional_notes': forms.Textarea(attrs={'placeholder': 'Any extra details about the property...', 'class': 'form-input', 'rows': 3}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['full_name', 'email', 'phone', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Enter your full name', 'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com', 'class': 'form-input'}),
            'phone': forms.TextInput(attrs={'placeholder': '+234 800 000 0000 (optional)', 'class': 'form-input'}),
            'message': forms.Textarea(attrs={'placeholder': 'How can we help?', 'class': 'form-input', 'rows': 5}),
        }
        labels = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone': 'Phone Number',
            'message': 'Message',
        }


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = [
            'title', 'property_type', 'status', 'location', 'description',
            'bedrooms', 'bathrooms', 'size', 'price', 'price_on_request',
            'main_image', 'is_featured', 'is_active',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g. Penthouse Apartment', 'class': 'dash-input'}),
            'property_type': forms.Select(attrs={'class': 'dash-input'}),
            'status': forms.Select(attrs={'class': 'dash-input'}),
            'location': forms.TextInput(attrs={'placeholder': 'e.g. Sangotedo, Lekki, Lagos', 'class': 'dash-input'}),
            'description': forms.Textarea(attrs={'placeholder': 'Describe the property...', 'class': 'dash-input', 'rows': 4}),
            'bedrooms': forms.NumberInput(attrs={'class': 'dash-input', 'min': 0}),
            'bathrooms': forms.NumberInput(attrs={'class': 'dash-input', 'min': 0}),
            'size': forms.TextInput(attrs={'placeholder': 'e.g. 650 sqm, 2 plots', 'class': 'dash-input'}),
            'price': forms.TextInput(attrs={'placeholder': 'e.g. ₦45,000,000', 'class': 'dash-input'}),
        }