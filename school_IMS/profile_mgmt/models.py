from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.


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




#CUSTOMER PROFILE
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_modified = models.DateTimeField(User, auto_now=True)
    phone = models.CharField(max_length=20, blank=True)
    address1 = models.CharField(max_length=200, blank=True)
    address2 = models.CharField(max_length=200, blank=True)
    postcode = models.CharField(max_length=10, blank=True)
    city = models.CharField(max_length=50, blank=True)
    
    def _str_(self):
        return self.user.username
    
#CREATE USER PROFILE BY DEFAULT UPON SIGNUP
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        
#AUTOMATE  PROFILE CREATION
post_save.connect(create_profile,sender=User)