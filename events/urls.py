from django.urls import path
from . import views

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
]