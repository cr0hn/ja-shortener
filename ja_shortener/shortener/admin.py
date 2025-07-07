from django import forms
from django.contrib import admin
from django.urls import reverse
from django.conf import settings
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin

from .models import ShortUrl, UrlVisit


class ShortUrlAdminForm(forms.ModelForm):
    """
    ModelForm for ShortUrl admin to control short_code field behavior.
    """
    
    class Meta:
        model = ShortUrl
        fields = ['short_code', 'original_url', 'description']
        required_fields = ['original_url']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['short_code'].required = False


@admin.register(ShortUrl)
class ShortUrlAdmin(ModelAdmin):
    """
    Admin configuration for ShortUrl model.
    """
    form = ShortUrlAdminForm
    
    list_display = [
        'custom_short_code_display', 'shortened_url', 'original_url_truncated', 'description_truncated',
        'total_visits', 'unique_visitors', 'created_at'
    ]
    list_filter = ['created_at', 'updated_at']
    search_fields = ['short_code', 'original_url', 'description']
    readonly_fields = ['id', 'created_at', 'updated_at', 'shortened_url_display']
    ordering = ['-created_at']
    
    fieldsets = [
        (_('URL Information'), {
            'fields': ['short_code', 'original_url', 'description'],
            'description': _('Enter the original URL and optionally a custom short code. Leave short code empty for auto-generation.')
        })
    ]
    
    def _complete_short_url(self, obj):
        """Complete the short URL with the SHORTENER_HOST."""
        if obj.short_code:
            return f"{settings.SHORTENER_HOST}{obj.short_code}/"
        return None
    
    def shortened_url(self, obj):
        """Display shortened URL as a clickable link."""
        return self._complete_short_url(obj) or '-'
    
    shortened_url.short_description = _('Shortened URL')

    def custom_short_code_display(self, obj):
        """Display custom short code as a clickable link to edit the object."""
        short_url = self._complete_short_url(obj)
        if short_url:
            return format_html(
                '<a href="{}" target="_blank">{} &rarr;</a>',
                reverse('admin:shortener_shorturl_change', args=[obj.id]),
                short_url
            )
        return '-'
    
    custom_short_code_display.short_description = _('Short Code')

    def custom_short_code(self, obj):
        """Display custom short code if provided."""
        return obj.short_code or '-'
    custom_short_code.short_description = _('Custom Short Code')
    
    def shortened_url_display(self, obj):
        """Display shortened URL in detail view."""
        return self.shortened_url(obj)
    shortened_url_display.short_description = _('Shortened URL')
    
    def original_url_truncated(self, obj):
        """Display truncated original URL as a clickable link."""
        truncated_url = obj.original_url[:50] + "..." if len(obj.original_url) > 50 else obj.original_url
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.original_url,
            truncated_url
        )
    original_url_truncated.short_description = _('Original URL')
    
    def description_truncated(self, obj):
        """Display truncated description."""
        if obj.description and len(obj.description) > 30:
            return f"{obj.description[:30]}..."
        return obj.description or '-'
    description_truncated.short_description = _('Description')
    
    def total_visits(self, obj):
        """Display total visits count."""
        return UrlVisit.get_total_visits_count(obj)
    total_visits.short_description = _('Total Visits')
    
    def unique_visitors(self, obj):
        """Display unique visitors count."""
        return UrlVisit.get_unique_visitors_count(obj)
    unique_visitors.short_description = _('Unique Visitors')
