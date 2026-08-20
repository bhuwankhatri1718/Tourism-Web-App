from django.contrib import admin
from .models import Guideline, Notice


@admin.register(Guideline)
class GuidelineAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'created_at')
    search_fields = ('title',)
    list_filter = ('is_active',)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'published_date', 'is_active', 'created_at')
    search_fields = ('title',)
    list_filter = ('is_active', 'published_date')