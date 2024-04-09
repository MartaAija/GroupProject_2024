from django.db import models
from inventory.models import Equipment

# Create your models here.
class ReservationDetail(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    type = models.CharField(max_length=100)
    location = models.CharField(max_length=100, default='Unknown')

    def str(self):
        return f"{self.quantity} x {self.equipment.display_name}"
