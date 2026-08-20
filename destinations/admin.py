from django.contrib import admin
from .models import Destination


@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'best_time_to_visit', 'is_active', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('is_active',)