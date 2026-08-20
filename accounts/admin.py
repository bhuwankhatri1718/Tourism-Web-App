from django.contrib import admin
from .models import TouristProfile


@admin.register(TouristProfile)
class TouristProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address', 'nationality')
    search_fields = ('user__username', 'user__email', 'phone')