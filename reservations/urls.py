# AUTHORSHIP: MARTA ZIGURE (w1888516)
#    WORKED ON FILE:
#       - NOEL VARGA (w1932378) (Added admin related links)

from django.urls import path
from . import views
from .views import manageBookings, editStatus, updateStatus

urlpatterns = [
    path('', views.reservations, name='reservations'),  # Homepage displaying reservations
    path('history/', views.reservation_history, name='reservation_history'),  # View reservation history
    path('status/', views.reservation_status, name='reservation_status'),  # View reservation status
    path('booking-cart/', views.view_booking_cart, name='view_booking_cart'),  # View booking cart
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),  # Add item to booking cart
    path('update_cart_item/<int:equipment_id>/', views.update_cart_item, name='update_cart_item'),  # Update item in booking cart
    path('remove/<int:equipment_id>/', views.remove_from_cart, name='remove_from_cart'),  # Remove item from booking cart
    path('cancel/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),  # Cancel a reservation
    path('remove-not-approved/<int:reservation_id>/', views.remove_not_approved, name='remove_not_approved'),  # Remove not approved reservation
    path('rebook/<int:reservation_id>/', views.rebook_item, name='rebook_item'),  # Rebook a reservation
    path('manageBookings/', manageBookings, name="manageBookings"),  # Manage bookings
    path('editStatus/<int:id>', editStatus, name="editStatus"),  # Edit status of a booking
    path('editStatus/updateStatus/<int:id>', updateStatus, name='updateStatus'),  # Update booking status
]

