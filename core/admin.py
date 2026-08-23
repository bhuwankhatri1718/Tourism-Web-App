from django.contrib import admin
from .models import Guideline, Notice, Complaint


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


@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('subject', 'full_name', 'email', 'status', 'submitted_at')
    list_filter = ('status',)
    search_fields = ('full_name', 'email', 'subject')
    actions = ['mark_resolved']

    def mark_resolved(self, request, queryset):
        queryset.update(status='RESOLVED')
    mark_resolved.short_description = 'Mark selected complaints as Resolved'