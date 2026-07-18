from django.urls import path
from . import views
from . import dashboard

urlpatterns = [
    path('', views.company_home, name='home'),
    path('abuja-buy-and-sell-property/', views.event_home, name='event_home'),
    path('about/', views.about_us, name='about_us'),
    path('contact/', views.contact_us, name='contact_us'),
    path('properties/', views.properties_list, name='properties'),
    path('properties/<uuid:pk>/', views.property_detail, name='property_detail'),
    path('register/', views.register, name='register'),
    path('register/vendor/<uuid:pk>/', views.vendor_form, name='vendor_form'),
    path('ticket/<uuid:pk>/', views.ticket, name='ticket'),

    # --- Staff Dashboard ---
    path('dashboard/login/', dashboard.dashboard_login, name='dashboard_login'),
    path('dashboard/logout/', dashboard.dashboard_logout, name='dashboard_logout'),
    path('dashboard/', dashboard.dashboard_home, name='dashboard_home'),

    path('dashboard/properties/', dashboard.dashboard_properties, name='dashboard_properties'),
    path('dashboard/properties/add/', dashboard.dashboard_property_add, name='dashboard_property_add'),
    path('dashboard/properties/<uuid:pk>/edit/', dashboard.dashboard_property_edit, name='dashboard_property_edit'),
    path('dashboard/properties/<uuid:pk>/delete/', dashboard.dashboard_property_delete, name='dashboard_property_delete'),
    path('dashboard/properties/<uuid:pk>/toggle/<str:field>/', dashboard.dashboard_property_toggle, name='dashboard_property_toggle'),
    path('dashboard/properties/<uuid:pk>/media/<int:media_id>/delete/', dashboard.dashboard_media_delete, name='dashboard_media_delete'),

    path('dashboard/registrations/', dashboard.dashboard_registrations, name='dashboard_registrations'),
    path('dashboard/registrations/<uuid:pk>/confirm/', dashboard.dashboard_registration_confirm, name='dashboard_registration_confirm'),

    path('dashboard/vendors/', dashboard.dashboard_vendors, name='dashboard_vendors'),

    path('dashboard/messages/', dashboard.dashboard_messages, name='dashboard_messages'),
    path('dashboard/messages/<uuid:pk>/toggle-read/', dashboard.dashboard_message_toggle_read, name='dashboard_message_toggle_read'),
    path('dashboard/messages/<uuid:pk>/delete/', dashboard.dashboard_message_delete, name='dashboard_message_delete'),
]