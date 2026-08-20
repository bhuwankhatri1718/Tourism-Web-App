from django.db import models
from django.contrib.auth.models import User
from destinations.models import Destination


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('REJECTED', 'Rejected'),
    ]

    tourist = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings'
    )
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='bookings'
    )

    visit_date = models.DateField()
    number_of_visitors = models.PositiveIntegerField(default=1)
    remarks = models.TextField(blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.tourist.username} - {self.destination.name}"