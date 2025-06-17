from django.contrib import admin
from django.utils.html import format_html

from unfold.admin import ModelAdmin

from .models import ShortUrl, UrlVisit


@admin.register(ShortUrl)
class ShortUrlAdmin(ModelAdmin):
    """
    Admin configuration for ShortUrl model.
    """
    list_display = [
        'short_code', 'original_url_truncated', 'description_truncated',
        'total_visits', 'unique_visitors'
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['short_code', 'original_url', 'description']
    readonly_fields = ['id', 'short_code', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    fieldsets = [
        ('URL Information', {
            'fields': ['original_url', 'description']
        })
    ]
    
    def original_url_truncated(self, obj):
        """Display truncated original URL as a clickable link."""
        truncated_url = obj.original_url[:50] + "..." if len(obj.original_url) > 50 else obj.original_url
        return format_html(
            '<a href="{}" target="_blank">{} &rarr;</a>',
            obj.original_url,
            truncated_url
        )
    original_url_truncated.short_description = 'Original URL'
    
    def description_truncated(self, obj):
        """Display truncated description."""
        if obj.description and len(obj.description) > 30:
            return f"{obj.description[:30]}..."
        return obj.description or '-'
    description_truncated.short_description = 'Description'
    
    def total_visits(self, obj):
        """Display total visits count."""
        return UrlVisit.get_total_visits_count(obj)
    total_visits.short_description = 'Total Visits'
    
    def unique_visitors(self, obj):
        """Display unique visitors count."""
        return UrlVisit.get_unique_visitors_count(obj)
    unique_visitors.short_description = 'Unique Visitors'
    