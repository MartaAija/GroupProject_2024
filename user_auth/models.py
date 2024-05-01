from django.db import models
from profile_mgmt.models import Users

# Create your models here.
class Admins(models.Model):
    # MODEL / TABLE CREATION FOR ADMIN
    user = models.ForeignKey(Users, on_delete=models.CASCADE);
    firstName = models.CharField(max_length = 100)
    lastName = models.CharField(max_length = 100)
    adminEmail = models.CharField(max_length = 100)
    adminPassword = models.CharField(max_length = 100)

    def __str__(self):
        return self.adminEmail