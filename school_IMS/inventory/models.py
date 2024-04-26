from django.db import models

# Create your models here.
class Equipment(models.Model):
    display_name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    quantity = models.IntegerField()
    instock_items = models.IntegerField(('zipcode'), null=True, blank=True)
    comments = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.display_name

STATUS_CHOICES = {
    ("on_loan", "On loan"),
    ("repairing", "Repairing"),
    ("available", "Available"),
    ("decommisioned", "Dicommisioned"),
}

class Equip_Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_type = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100)
    item_CPU = models.CharField(max_length=100, blank=True)
    item_GPU = models.CharField(max_length=100, blank=True)
    item_RAM = models.CharField(max_length=100, blank=True)
    status = models.CharField( 
        max_length = 20, 
        choices = STATUS_CHOICES, 
        default = 'available'
        ) 
    equipmentid = models.ForeignKey(Equipment, on_delete=models.CASCADE)

