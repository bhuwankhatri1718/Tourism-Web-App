from django.db import models


class Destination(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()

    best_time_to_visit = models.CharField(max_length=200, blank=True)
    entry_information = models.TextField(blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    image = models.ImageField(upload_to='destinations/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name






class Destination(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    description = models.TextField()

    best_time_to_visit = models.CharField(max_length=200, blank=True)
    entry_information = models.TextField(blank=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    image = models.ImageField(upload_to='destinations/', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='hotels'
    )
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    contact_number = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.destination.name})"