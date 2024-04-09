from django.db import models

# Create your models here.
from django.db import models

class Users(models.Model):
    # DEFINING THE CHOICES AND NAMES FOR EACH CHOICE FOR USER TYPE:
    STUDENT = "STU"
    STAFF = "STA"
    USER_TYPE_CHOICES = [
        (STUDENT, "Student"),
        (STAFF, "Staff"),
    ]

    # MODEL / TABLE CREATION FOR USER
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    userEmail = models.CharField(max_length=100)
    userName = models.CharField(max_length=100)
    userPassword = models.CharField(max_length=100)
    userType = models.CharField(
        max_length=3,
        choices=USER_TYPE_CHOICES,
        default=STUDENT,
    )

    def str(self):
        return self.userName