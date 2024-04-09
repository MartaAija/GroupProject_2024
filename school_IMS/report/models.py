from django.db import models

# Create your models here.
class reports(models.Model):
    # MODEL / TABLE CREATION FOR REPORTS
    totalItems = models.IntegerField()
    availableItems = models.IntegerField()
    onLoanItems = models.IntegerField()
    inRepairItems = models.IntegerField()
    decommissionedItems = models.IntegerField()

    def __str__(self):
        return self.totalItems