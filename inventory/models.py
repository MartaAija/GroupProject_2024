#    WORKED ON FILE:
#       - NOEL VARGA (w1932378)
#       - Emina Asherbekova (w1830501)

from django.db import models

# OPTIONS OF ITEMS STATUS
REPORT_STATUS = {
    ("Available", "Available"),
    ("On-Loan", "On-Loan"),
    ("In-Repair", "In-Repair"),
    ("Decommisioned", "Decommisioned"),
}

# OPTIONS OF ONSITE 
ONSITE_CHOICES = {
    ("Yes", "Yes"),
    ("No", "No"),
}

#define a model for storing Equipment data
class Equipment(models.Model):
    display_name = models.CharField(max_length=100) #name of the product
    asset_type = models.CharField(max_length=100) #type of the product
    location = models.CharField(max_length=100) #location where the poduct is
    quantity = models.IntegerField() # quantity of products available to book
    instock_items = models.IntegerField(('zipcode'), null=True, blank=True) # quantity of products overall in stock
    comments = models.CharField(max_length=100, blank=True) # comments admin can make for the product
    onsite_only = models.CharField(max_length = 20,
                              choices = ONSITE_CHOICES,
                              default = "No")   #speicification if the product is only available to be used On-Site
    status = models.CharField(max_length = 20,
                              choices = REPORT_STATUS,
                              default = "Available") # status of the product

    def __str__(self):
        return self.display_name


# Define status choices for status of Equip_Item objects
STATUS_CHOICES = {
    ("on_loan", "On loan"),
    ("repairing", "Repairing"),
    ("available", "Available"),
    ("decommisioned", "Dicommisioned"),
}

#define a model for storing data about specific Equip items
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
    equipmentid = models.ForeignKey(Equipment, on_delete=models.CASCADE) # Link to the Equipment model

