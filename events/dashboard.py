"""
Staff-only management dashboard for Savannah Woodlands.

Every view here requires the logged-in user to be staff (is_staff=True).
This reuses Django's built-in auth system — staff accounts are created
the same way as your Django admin superuser/staff accounts (via
`python manage.py createsuperuser` or through /admin/).
"""
from functools import wraps

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Q

from .models import (
    Property, PropertyMedia, Registration, VendorApplication, ContactMessage,
)
from .forms import PropertyForm


def _sidebar_context(active_nav):
    """Shared context every dashboard page needs for the sidebar —
    which link is highlighted, and the pending/unread badge counts."""
    return {
        'active_nav': active_nav,
        'pending_count': Registration.objects.filter(payment_status='pending').count(),
        'unread_count': ContactMessage.objects.filter(is_read=False).count(),
    }


def staff_required(view_func):
    """Combines login_required + is_staff check, redirecting to the
    dashboard login page (not the public site or /admin/) on failure."""
    @wraps(view_func)
    def wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('dashboard_login')
        if not request.user.is_staff:
            messages.error(request, "You don't have permission to access the dashboard.")
            return redirect('dashboard_login')
        return view_func(request, *args, **kwargs)
    return wrapped


# ---------------------------------------------------------------------
# AUTH
# ---------------------------------------------------------------------

def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard_home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard_home')
        messages.error(request, 'Invalid credentials, or this account does not have dashboard access.')

    return render(request, 'events/dashboard/login.html')


def dashboard_logout(request):
    logout(request)
    return redirect('dashboard_login')


# ---------------------------------------------------------------------
# OVERVIEW
# ---------------------------------------------------------------------

@staff_required
def dashboard_home(request):
    stats = {
        'total_properties': Property.objects.count(),
        'active_properties': Property.objects.filter(is_active=True).count(),
        'featured_properties': Property.objects.filter(is_featured=True, is_active=True).count(),
        'total_registrations': Registration.objects.count(),
        'pending_payments': Registration.objects.filter(payment_status='pending').count(),
        'confirmed_payments': Registration.objects.filter(payment_status='confirmed').count(),
        'vendor_applications': VendorApplication.objects.count(),
        'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
    }
    recent_registrations = Registration.objects.order_by('-registered_at')[:6]
    recent_messages = ContactMessage.objects.filter(is_read=False).order_by('-submitted_at')[:5]

    return render(request, 'events/dashboard/home.html', {
        'stats': stats,
        'recent_registrations': recent_registrations,
        'recent_messages': recent_messages,
        **_sidebar_context('home'),
    })


# ---------------------------------------------------------------------
# PROPERTIES
# ---------------------------------------------------------------------

@staff_required
def dashboard_properties(request):
    properties = Property.objects.annotate(media_count=Count('media_files')).order_by('-created_at')

    q = request.GET.get('q', '').strip()
    if q:
        properties = properties.filter(Q(title__icontains=q) | Q(location__icontains=q))

    status_filter = request.GET.get('status')
    if status_filter == 'active':
        properties = properties.filter(is_active=True)
    elif status_filter == 'inactive':
        properties = properties.filter(is_active=False)
    elif status_filter == 'featured':
        properties = properties.filter(is_featured=True)

    return render(request, 'events/dashboard/properties_list.html', {
        'properties': properties,
        'q': q,
        'status_filter': status_filter,
        **_sidebar_context('properties'),
    })


@staff_required
def dashboard_property_add(request):
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save()
            _save_uploaded_media(request, property_obj)
            messages.success(request, f'"{property_obj.title}" was created.')
            return redirect('dashboard_property_edit', pk=property_obj.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PropertyForm()

    return render(request, 'events/dashboard/property_form.html', {
        'form': form,
        'property_obj': None,
        'is_new': True,
        **_sidebar_context('properties'),
    })


@staff_required
def dashboard_property_edit(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            _save_uploaded_media(request, property_obj)
            messages.success(request, 'Property updated.')
            return redirect('dashboard_property_edit', pk=property_obj.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = PropertyForm(instance=property_obj)

    return render(request, 'events/dashboard/property_form.html', {
        'form': form,
        'property_obj': property_obj,
        'is_new': False,
        'media_files': property_obj.media_files.all(),
        **_sidebar_context('properties'),
    })


def _save_uploaded_media(request, property_obj):
    """Handle the multi-file gallery upload input shared by add/edit forms."""
    files = request.FILES.getlist('gallery_files')
    for f in files:
        media_type = 'video' if f.content_type.startswith('video') else 'image'
        PropertyMedia.objects.create(
            property=property_obj,
            file=f,
            media_type=media_type,
        )
    if files:
        messages.success(request, f'{len(files)} file(s) added to the gallery.')


@staff_required
def dashboard_property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk)
    if request.method == 'POST':
        title = property_obj.title
        property_obj.delete()
        messages.success(request, f'"{title}" was deleted.')
        return redirect('dashboard_properties')
    return render(request, 'events/dashboard/confirm_delete.html', {
        'object_label': property_obj.title,
        'cancel_url': 'dashboard_property_edit',
        'cancel_pk': property_obj.pk,
        **_sidebar_context('properties'),
    })


@staff_required
def dashboard_media_delete(request, pk, media_id):
    """Delete a single gallery photo/video from a property."""
    property_obj = get_object_or_404(Property, pk=pk)
    media = get_object_or_404(PropertyMedia, pk=media_id, property=property_obj)
    if request.method == 'POST':
        media.delete()
        messages.success(request, 'Media file removed.')
    return redirect('dashboard_property_edit', pk=property_obj.pk)


@staff_required
def dashboard_property_toggle(request, pk, field):
    """Quick toggle for is_active / is_featured from the list view."""
    property_obj = get_object_or_404(Property, pk=pk)
    if field == 'active':
        property_obj.is_active = not property_obj.is_active
    elif field == 'featured':
        property_obj.is_featured = not property_obj.is_featured
    property_obj.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_properties'))


# ---------------------------------------------------------------------
# REGISTRATIONS
# ---------------------------------------------------------------------

@staff_required
def dashboard_registrations(request):
    registrations = Registration.objects.order_by('-registered_at')

    status_filter = request.GET.get('status')
    if status_filter in ('pending', 'confirmed'):
        registrations = registrations.filter(payment_status=status_filter)

    type_filter = request.GET.get('type')
    if type_filter in ('ticket', 'vendor'):
        registrations = registrations.filter(ticket_type=type_filter)

    q = request.GET.get('q', '').strip()
    if q:
        registrations = registrations.filter(
            Q(full_name__icontains=q) | Q(email__icontains=q) | Q(ticket_number__icontains=q)
        )

    return render(request, 'events/dashboard/registrations_list.html', {
        'registrations': registrations,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'q': q,
        **_sidebar_context('registrations'),
    })


@staff_required
def dashboard_registration_confirm(request, pk):
    reg = get_object_or_404(Registration, pk=pk)
    if request.method == 'POST':
        reg.payment_status = 'confirmed'
        reg.save()
        messages.success(request, f'Payment confirmed for {reg.full_name}. QR ticket generated.')
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_registrations'))


# ---------------------------------------------------------------------
# VENDOR APPLICATIONS
# ---------------------------------------------------------------------

@staff_required
def dashboard_vendors(request):
    vendors = VendorApplication.objects.select_related('registration').order_by('-submitted_at')
    return render(request, 'events/dashboard/vendors_list.html', {
        'vendors': vendors,
        **_sidebar_context('vendors'),
    })


# ---------------------------------------------------------------------
# CONTACT MESSAGES
# ---------------------------------------------------------------------

@staff_required
def dashboard_messages(request):
    contact_messages = ContactMessage.objects.order_by('-submitted_at')
    return render(request, 'events/dashboard/messages_list.html', {
        'contact_messages': contact_messages,
        **_sidebar_context('messages'),
    })


@staff_required
def dashboard_message_toggle_read(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    msg.is_read = not msg.is_read
    msg.save()
    return redirect(request.META.get('HTTP_REFERER', 'dashboard_messages'))


@staff_required
def dashboard_message_delete(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message deleted.')
    return redirect('dashboard_messages')
