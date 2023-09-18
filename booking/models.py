from django.db import models


class hostel_details(models.Model):
    cooling = models.CharField(max_length=10)
    block = models.CharField(max_length=1)
    sharing = models.IntegerField()
    bathroom = models.CharField(max_length=10)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.block} {self.cooling} Price:{self.price}"

