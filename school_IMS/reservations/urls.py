from django.urls import path
from . import views
from .views import manageBookings, editStatus, updateStatus

urlpatterns = [
    path('', views.reservations, name='reservations'),
    path('history/', views.reservation_history, name='reservation_history'),
    path('status/', views.reservation_status, name='reservation_status'),
    path('booking-cart/', views.view_booking_cart, name='view_booking_cart'),  # Update the name here
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_item/<int:equipment_id>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:equipment_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    path('remove-not-approved/<int:reservation_id>/', views.remove_not_approved, name='remove_not_approved'),
    path('rebook/<int:reservation_id>/', views.rebook_item, name='rebook_item'),
    path('manageBookings/', manageBookings, name = "manageBookings"),
    path('editStatus/<int:id>', editStatus, name = "editStatus"),
    path('editStatus/updateStatus/<int:id>', updateStatus, name='updateStatus'),
]

