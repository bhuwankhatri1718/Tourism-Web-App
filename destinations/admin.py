from django.contrib import admin
from .models import Destination, Hotel


class HotelInline(admin.TabularInline):
    model = Hotel
    extra = 1


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'best_time_to_visit', 'is_active', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('is_active',)
    inlines = [HotelInline]


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'destination', 'price_per_night', 'contact_number', 'is_active')
    search_fields = ('name', 'destination__name')
    list_filter = ('is_active', 'destination')