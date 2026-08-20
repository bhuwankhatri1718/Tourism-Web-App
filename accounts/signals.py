from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver

from .models import TouristProfile


@receiver(post_save, sender=User)
def create_tourist_profile(sender, instance, created, **kwargs):
    if created:
        TouristProfile.objects.create(user=instance)