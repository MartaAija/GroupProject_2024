#   WORKED ON FILE:
#        - NOEL VARGA (w1932378)

from datetime import datetime
from django.db import models

# MODEL / TABLE CREATION FOR REPORTS
class reports(models.Model):
    totalItems = models.IntegerField()
    availableItems = models.IntegerField()
    onLoanItems = models.IntegerField()
    inRepairItems = models.IntegerField()
    decommissionedItems = models.IntegerField()
    generatedOn = models.DateField(default=datetime.now, blank=True)

    def __int__(self):
        return self.totalItems
