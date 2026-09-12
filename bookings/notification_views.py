from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET, require_POST

from .models import BookingNotification


@login_required
@never_cache
@require_GET
def notification_list(request):
    notifications = BookingNotification.objects.filter(
        booking__tourist=request.user
    )

    items = []

    for notification in notifications.select_related(
        "booking__destination"
    )[:30]:
        booking = notification.booking

        items.append({
            "id": notification.pk,
            "message": (
                f"Admin has {notification.status.lower()} your booking "
                f"{booking.reference_number} for "
                f"{booking.destination.name}."
            ),
            "is_read": notification.is_read,
            "created_at": notification.created_at.isoformat(),
            "open_url": reverse(
                "notification_open",
                args=[notification.pk],
            ),
        })

    return JsonResponse({
        "unread_count": notifications.filter(is_read=False).count(),
        "items": items,
    })


@login_required
@require_POST
def notification_open(request, pk):
    notification = get_object_or_404(
        BookingNotification,
        pk=pk,
        booking__tourist=request.user,
    )

    BookingNotification.objects.filter(
        pk=notification.pk
    ).update(is_read=True)

    return redirect(
        "booking_success",
        pk=notification.booking_id,
    )