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

#--------------------------------------------------------------------------------------------------
"""
# MODEL / TABLE CREATION FOR REPORTS
class ReportMgmt(models.Model):
    #admin = models.ForeignKey(Admin, on_delete=models.CASCADE)
    report = models.ForeignKey(reports, on_delete=models.CASCADE)
    approvalStatus = models.CharField(max_length=10, choices=(('Pending', 'Pending'),
                                                              ('Approved', 'Approved'),
                                                              ('Denied', 'Denied')),
                                                                default='Pending')
"""