from django.db import models
from django.contrib.auth.models import User


class hostel_details(models.Model):
    cooling = models.CharField(max_length=10)
    block = models.CharField(max_length=1)
    sharing = models.IntegerField()
    bathroom = models.CharField(max_length=10)
    price = models.IntegerField()

    def __str__(self):
        return f"{self.block} {self.cooling}, sharing:{self.sharing}, Price:{self.price}"


class transactions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(hostel_details, on_delete=models.CASCADE)
    price = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} {self.room} paid:{self.price}"
