from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Registration, VendorApplication, VendorMedia, Property
from .forms import RegistrationForm, VendorApplicationForm, ContactForm


def company_home(request):
    """Main Savannah Woodlands company homepage — introduces the company
    and surfaces upcoming events (e.g. Abuja Buy & Sell Property) plus
    a handful of featured properties pulled from the database."""
    featured_properties = Property.objects.filter(is_active=True, is_featured=True)[:6]
    return render(request, 'events/company_home.html', {
        'featured_properties': featured_properties,
    })


def event_home(request):
    """Dedicated landing page for the Abuja Buy & Sell Property event.
    This was previously served at the site root; content is unchanged,
    only the URL moved to /abuja-buy-and-sell-property/."""
    return render(request, 'events/home.html')


def about_us(request):
    return render(request, 'events/about_us.html')


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Thanks for reaching out! We'll get back to you shortly.")
            return redirect('contact_us')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = ContactForm()
    return render(request, 'events/contact_us.html', {'form': form})


def properties_list(request):
    """Public listing of all active properties, with optional filtering
    by property type via ?type=<value>."""
    properties = Property.objects.filter(is_active=True)

    selected_type = request.GET.get('type')
    if selected_type:
        properties = properties.filter(property_type=selected_type)

    return render(request, 'events/properties.html', {
        'properties': properties,
        'property_types': Property.PROPERTY_TYPES,
        'selected_type': selected_type,
    })


def property_detail(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, is_active=True)
    related_properties = Property.objects.filter(
        is_active=True, property_type=property_obj.property_type
    ).exclude(pk=property_obj.pk)[:3]
    return render(request, 'events/property_detail.html', {
        'property': property_obj,
        'related_properties': related_properties,
    })


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            reg = form.save()
            if reg.ticket_type == 'vendor':
                return redirect('vendor_form', pk=reg.pk)
            return redirect('ticket', pk=reg.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegistrationForm()
        # Pre-select ticket type from query param
        ticket_type = request.GET.get('type')
        if ticket_type in ['ticket', 'vendor']:
            form.initial['ticket_type'] = ticket_type
    return render(request, 'events/register.html', {'form': form})


def vendor_form(request, pk):
    reg = get_object_or_404(Registration, pk=pk, ticket_type='vendor')

    # If already submitted, go straight to ticket
    if hasattr(reg, 'vendor_application'):
        return redirect('ticket', pk=reg.pk)

    if request.method == 'POST':
        form = VendorApplicationForm(request.POST)
        files = request.FILES.getlist('media_files')

        if form.is_valid():
            vendor_app = form.save(commit=False)
            vendor_app.registration = reg
            vendor_app.save()

            # Save each uploaded file
            for f in files:
                media_type = 'video' if f.content_type.startswith('video') else 'image'
                VendorMedia.objects.create(
                    vendor_application=vendor_app,
                    file=f,
                    media_type=media_type,
                )

            return redirect('ticket', pk=reg.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = VendorApplicationForm()

    return render(request, 'events/vendor_form.html', {'form': form, 'reg': reg})


def ticket(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    return render(request, 'events/ticket.html', {'reg': reg})