# AUTHORSHIP: MARTA ZIGURE (w1888516)
# Import necessary modules and classes from Django
from django.db import models
from django.utils import timezone
from datetime import timedelta
from inventory.models import Equipment  
from django.db.models.signals import post_save  
from django.dispatch import receiver 
from django.contrib.auth import get_user_model  
from django.core.exceptions import ValidationError

# Function to set a default return date for a reservation (14 days from the current time)
def default_return_date():
    return timezone.now() + timedelta(days=14)

# Define a model for storing reservation details
class ReservationDetails(models.Model):
    # Define fields for the reservation model
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)  # Link to the Equipment model
    quantity = models.PositiveIntegerField(default=1)  # Quantity of items reserved (default is 1)
    reserved_date = models.DateField(default=timezone.now)  # Date when the reservation was made
    return_date = models.DateField(default=default_return_date)  # Date by which the item should be returned
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=False, null=False)  # Associated user 

    # Define status choices for the reservation
    APPROVED = 'Approved'
    NOT_APPROVED = 'Not Approved'
    PENDING = 'Pending'
    CANCELLED = 'Cancelled'
    COMPLETED = 'Completed'

    STATUS_CHOICES = [
        (APPROVED, 'Approved'),
        (NOT_APPROVED, 'Not Approved'),
        (PENDING, 'Pending'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)  # Status of the reservation

    def __str__(self):
        return f"Reservation for {self.equipment.display_name}"  # String representation of the reservation object

    def clean(self):
        # Validate reservation details
        if self.quantity <= 0:
            raise ValidationError("Quantity must be a positive integer.")
        if self.reserved_date < timezone.now().date():
            raise ValidationError("Reserved date cannot be in the past.")
        if self.return_date < self.reserved_date:
            raise ValidationError("Return date cannot be before reserved date.")

    def save(self, *args, **kwargs):
        # Override the save method to handle additional logic
        if not self.user_id:
            self.user = kwargs.pop('user', None)  # Set the user associated with the reservation
        if not self.return_date:
            self.return_date = self.reserved_date + timedelta(days=14)  # Set default return date if not provided
        super().save(*args, **kwargs)  # Call the superclass's save method to save the reservation

    class Meta:
        # Define permissions for the ReservationDetails model
        permissions = [
            ("can_view_reservation", "Can view reservation"),
            ("can_modify_reservation", "Can modify reservation"),
            ("can_delete_reservation", "Can delete reservation"),
        ]

# Signal receiver function to update equipment quantity based on reservation status changes
@receiver(post_save, sender=ReservationDetails)
def update_equipment_quantity(sender, instance, created, **kwargs):
    if created:
        # Reduce the quantity of the booked equipment if a new reservation is created
        instance.equipment.quantity -= instance.quantity
    elif instance.status in [ReservationDetails.CANCELLED, ReservationDetails.COMPLETED, ReservationDetails.NOT_APPROVED]:
        # Increase the quantity of the returned equipment if reservation status changes to canceled, completed, or not approved
        instance.equipment.quantity += instance.quantity
    instance.equipment.save()  # Save the updated equipment quantity
