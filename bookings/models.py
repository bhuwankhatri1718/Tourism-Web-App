from django.db import models
from django.contrib.auth.models import User
from destinations.models import Destination, Hotel


class Booking(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('REJECTED', 'Rejected'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid'),
        ('PAID', 'Paid'),
    ]

    tourist = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='bookings'
    )
    destination = models.ForeignKey(
        Destination, on_delete=models.CASCADE, related_name='bookings'
    )
    hotel = models.ForeignKey(
        Hotel, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings'
    )

    visit_date = models.DateField()
    number_of_visitors = models.PositiveIntegerField(default=1)
    remarks = models.TextField(blank=True)

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='PENDING'
    )
    is_seen_by_tourist = models.BooleanField(default=True)

    advance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=10, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    payment_transaction_id = models.CharField(max_length=100, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def reference_number(self):
        return f"NTP-{self.created_at.year}-{self.id:06d}"

    def save(self, *args, **kwargs):
        if self.pk:
            old = Booking.objects.filter(pk=self.pk).first()
            if old and old.status == 'PENDING' and self.status in ('CONFIRMED', 'REJECTED'):
                self.is_seen_by_tourist = False
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.tourist.username} - {self.destination.name}"