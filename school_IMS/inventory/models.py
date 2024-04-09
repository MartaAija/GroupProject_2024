from django.db import models

# Create your models here.
class Equipment(models.Model):
    display_name = models.CharField(max_length=100)
    asset_type = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def str(self):
        return self.display_name