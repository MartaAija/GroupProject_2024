from django.db import models

# Create your models here.
from django.db import models

class MyImage(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images/')