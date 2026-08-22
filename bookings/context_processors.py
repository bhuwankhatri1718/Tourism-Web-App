from .models import Booking


def notification_count(request):
    if request.user.is_authenticated:
        count = Booking.objects.filter(
            tourist=request.user, is_seen_by_tourist=False
        ).count()
        return {'unread_booking_count': count}
    return {'unread_booking_count': 0}