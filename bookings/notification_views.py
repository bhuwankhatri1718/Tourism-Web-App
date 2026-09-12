from django.contrib import admin
from django.db import transaction

from .models import Booking, BookingNotification


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "reference_number",
        "id",
        "tourist",
        "destination",
        "hotel",
        "visit_date",
        "number_of_visitors",
        "status",
        "payment_status",
        "advance_amount",
        "created_at",
    )

    search_fields = (
        "tourist__username",
        "destination__name",
    )

    list_filter = (
        "status",
        "payment_status",
        "destination",
    )

    actions = ["mark_confirmed", "mark_rejected"]

    @transaction.atomic
    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            old_status = (
                Booking.objects.select_for_update()
                .get(pk=obj.pk)
                .status
            )

        super().save_model(request, obj, form, change)

        if (
            change
            and old_status != obj.status
            and obj.status in ("CONFIRMED", "REJECTED")
        ):
            BookingNotification.objects.create(
                booking=obj,
                status=obj.status,
            )

    @transaction.atomic
    def record_decisions(self, request, queryset, status):
        count = 0

        for booking in (
            queryset.select_for_update()
            .filter(status="PENDING")
        ):
            booking.status = status
            booking.save()

            BookingNotification.objects.create(
                booking=booking,
                status=status,
            )
            count += 1

        self.message_user(
            request,
            f"{count} booking(s) updated and notification(s) sent.",
        )

    @admin.action(
        description="Mark selected bookings as Confirmed",
        permissions=["change"],
    )
    def mark_confirmed(self, request, queryset):
        self.record_decisions(request, queryset, "CONFIRMED")

    @admin.action(
        description="Mark selected bookings as Rejected",
        permissions=["change"],
    )
    def mark_rejected(self, request, queryset):
        self.record_decisions(request, queryset, "REJECTED")