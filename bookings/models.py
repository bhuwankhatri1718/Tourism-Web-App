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
    is_seen_by_tourist = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # If an admin edits this booking directly in the admin detail form
        # (not the bulk action), detect the PENDING -> CONFIRMED/REJECTED
        # transition here so the tourist gets notified either way.
        if self.pk:
            old = Booking.objects.filter(pk=self.pk).first()
            if old and old.status == 'PENDING' and self.status in ('CONFIRMED', 'REJECTED'):
                self.is_seen_by_tourist = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tourist.username} - {self.destination.name}"