from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('register/vendor/<uuid:pk>/', views.vendor_form, name='vendor_form'),
    path('ticket/<uuid:pk>/', views.ticket, name='ticket'),
]