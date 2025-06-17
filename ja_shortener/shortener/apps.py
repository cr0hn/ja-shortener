"""
Configuration for the shortener app.
"""
from django.apps import AppConfig


class ShortenerConfig(AppConfig):
    """
    Configuration class for the shortener app.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'shortener'
    verbose_name = 'URL Shortener'
