from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from inventory.models import Equipment
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

def default_return_date():
    return timezone.now() + timedelta(days=14)

class ReservationDetails(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    reserved_date = models.DateField(default=timezone.now)
    return_date = models.DateField(default=default_return_date)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)

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

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"Reservation for {self.equipment.display_name}"

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError("Quantity must be a positive integer.")
        if self.reserved_date < timezone.now().date():
            raise ValidationError("Reserved date cannot be in the past.")
        if self.return_date < self.reserved_date:
            raise ValidationError("Return date cannot be before reserved date.")

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user = kwargs.pop('user', None)
        if not self.return_date:
            self.return_date = self.reserved_date + timedelta(days=14)
        super().save(*args, **kwargs)

    class Meta:
        permissions = [
            ("can_view_reservation", "Can view reservation"),
            ("can_modify_reservation", "Can modify reservation"),
            ("can_delete_reservation", "Can delete reservation"),
        ]

@receiver(post_save, sender=ReservationDetails)
def update_equipment_quantity(sender, instance, created, **kwargs):
    if created:
        # Reduce the quantity of the booked equipment if reservation is created
        instance.equipment.quantity -= instance.quantity
    elif instance.status in [ReservationDetails.CANCELLED, ReservationDetails.COMPLETED, ReservationDetails.NOT_APPROVED]:
        # Increase the quantity of the returned equipment if reservation status is canceled, completed, or not approved
        instance.equipment.quantity += instance.quantity
    instance.equipment.save()
