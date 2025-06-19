import hashlib

from django.db import models
from django.conf import settings
from django.utils import timezone

from uuid_extensions import uuid7

from .algorithm import generate_short_code

def id_uuid7():
    return uuid7()

class ShortUrl(models.Model):
    """
    Model for storing shortened URLs with automatic consecutive short_code generation.
    """
    description = models.TextField(
        blank=True,
        null=True,
        help_text="Optional description for the shortened URL"
    )
    original_url = models.URLField(
        max_length=2048,
        help_text="The original URL to be shortened"
    )
    short_code = models.CharField(
        max_length=40,
        unique=True,
        db_index=True,
        help_text="Generated short code using a-zA-Z0-9 characters in consecutive order"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the URL was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the URL was last updated"
    )

    class Meta:
        db_table = 'short_urls'
        ordering = ['-created_at']
        verbose_name = 'Short URL'
        verbose_name_plural = 'Short URLs'

    def __str__(self):
        return f"{self.short_code} -> {self.original_url[:50]}..."
    
    def save(self, *args, **kwargs):
        """
        Override save to auto-generate consecutive short_code if not provided.
        """
        # Get the last short code

        while True:
            code_attemp = generate_short_code(
                ShortUrl.objects.order_by('-short_code').values_list('short_code', flat=True).first()
            )

            forbidden_codes = (
                settings.HEALTH_URL.replace('/', ''),
                settings.ADMIN_URL.replace('/', ''),
            )

            if code_attemp not in forbidden_codes:
                self.short_code = generate_short_code(code_attemp)
                break

        super().save(*args, **kwargs)


class UrlVisit(models.Model):
    """
    Model for tracking visits to shortened URLs with unique visitor identification.
    """

    short_url = models.ForeignKey(
        ShortUrl,
        on_delete=models.CASCADE,
        related_name='visits',
        help_text="Reference to the shortened URL that was visited"
    )
    visited_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp when the URL was visited"
    )
    visitor_signature = models.CharField(
        max_length=64,
        db_index=True,
        help_text="SHA256 hash of visitor's browser fingerprint for unique visitor tracking"
    )

    class Meta:
        db_table = 'url_visits'
        ordering = ['-visited_at']
        verbose_name = 'URL Visit'
        verbose_name_plural = 'URL Visits'
        indexes = [
            models.Index(fields=['short_url', 'visitor_signature']),
            models.Index(fields=['visited_at']),
        ]

    def __str__(self):
        return f"Visit to {self.short_url.short_code} at {self.visited_at}"

    @classmethod
    def create_visit(cls, short_url, request):
        """
        Create a new visit record with generated visitor signature.
        """
        visitor_signature = cls._generate_visitor_signature(request)
        return cls.objects.create(
            short_url=short_url,
            visitor_signature=visitor_signature
        )

    @staticmethod
    def _generate_visitor_signature(request) -> str:
        """
        Generate a SHA256 signature based on visitor's browser and HTTP headers.
        This creates a fingerprint for unique visitor identification without storing personal data.
        """
        # Gather visitor information
        user_agent = request.META.get('HTTP_USER_AGENT', '')
        accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
        accept_encoding = request.META.get('HTTP_ACCEPT_ENCODING', '')
        
        # Get IP address (considering proxies)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        
        # Additional headers for fingerprinting
        connection = request.META.get('HTTP_CONNECTION', '')
        cache_control = request.META.get('HTTP_CACHE_CONTROL', '')
        
        # Combine all information into a single string
        fingerprint_data = f"{user_agent}|{accept_language}|{accept_encoding}|{ip}|{connection}|{cache_control}"
        
        # Generate SHA256 hash
        return hashlib.sha256(fingerprint_data.encode('utf-8')).hexdigest()

    @classmethod
    def get_unique_visitors_count(cls, short_url):
        """
        Get the count of unique visitors for a specific short URL.
        """
        return cls.objects.filter(short_url=short_url).values('visitor_signature').distinct().count()

    @classmethod
    def get_total_visits_count(cls, short_url):
        """
        Get the total number of visits for a specific short URL.
        """
        return cls.objects.filter(short_url=short_url).count()
