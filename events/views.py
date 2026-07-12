from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Registration, VendorApplication, VendorMedia
from .forms import RegistrationForm, VendorApplicationForm


def home(request):
    return render(request, 'events/home.html')


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