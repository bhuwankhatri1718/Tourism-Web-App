from django.contrib import admin
from .models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'tourist', 'destination', 'visit_date',
        'number_of_visitors', 'status', 'created_at'
    )
    search_fields = ('tourist__username', 'destination__name')
    list_filter = ('status', 'destination')
    actions = ['mark_confirmed', 'mark_rejected']

    def mark_confirmed(self, request, queryset):
        queryset.update(status='CONFIRMED')
    mark_confirmed.short_description = 'Mark selected bookings as Confirmed'

    def mark_rejected(self, request, queryset):
        queryset.update(status='REJECTED')
    mark_rejected.short_description = 'Mark selected bookings as Rejected'