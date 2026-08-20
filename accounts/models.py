from django.db import models
from django.contrib.auth.models import User


class TouristProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='tourist_profile'
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.CharField(max_length=200, blank=True)
    nationality = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username