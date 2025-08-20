from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.db import models
from shortener.models import ShortUrl


class Command(BaseCommand):
    help = 'Generate QR codes for existing URLs that do not have them'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be done without actually generating QR codes',
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force regeneration of QR codes even for URLs that already have them',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        force = options['force']
        
        # Check if QR codes are enabled
        if not getattr(settings, 'QR_CODES_ENABLE', True):
            self.stdout.write(
                self.style.ERROR('QR code generation is disabled in settings (QR_CODES_ENABLE=False)')
            )
            return
        
        self.stdout.write(
            self.style.SUCCESS(
                'Generating QR codes for URLs...'
            )
        )
        
        if force:
            urls_query = ShortUrl.objects.all()
            self.stdout.write(f'Found {urls_query.count()} URLs total (force mode)')
        else:
            # Filter URLs that have no QR code (empty string or null)
            urls_query = ShortUrl.objects.filter(
                models.Q(qr_code='') | models.Q(qr_code__isnull=True)
            )
            self.stdout.write(f'Found {urls_query.count()} URLs without QR codes')
        
        if urls_query.count() == 0:
            self.stdout.write(
                self.style.WARNING('No URLs found to process')
            )
            return
        
        if dry_run:
            self.stdout.write(
                self.style.WARNING('DRY RUN MODE - No QR codes will be generated')
            )
            for url in urls_query:
                self.stdout.write(f'  - Would generate QR for: {url.short_code} -> {url.original_url}')
            return
        
        # Generate QR codes
        success_count = 0
        error_count = 0
        
        for url in urls_query:
            try:
                self.stdout.write(f'Generating QR for {url.short_code}...', ending='')
                
                if force and url.qr_code:
                    # Delete existing QR code file
                    try:
                        url.qr_code.delete(save=False)
                    except Exception:
                        pass  # File might not exist
                
                url.generate_qr_code()
                url.save()
                
                if url.qr_code:
                    self.stdout.write(
                        self.style.SUCCESS(f' ✓ Generated: {url.qr_code.name}')
                    )
                    success_count += 1
                else:
                    self.stdout.write(
                        self.style.ERROR(' ✗ Failed to generate QR code')
                    )
                    error_count += 1
                    
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f' ✗ Error: {str(e)}')
                )
                error_count += 1
        
        # Summary
        self.stdout.write('\n' + '='*50)
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated: {success_count} QR codes')
        )
        if error_count > 0:
            self.stdout.write(
                self.style.ERROR(f'Errors: {error_count}')
            )
        
        self.stdout.write(
            self.style.SUCCESS('\nQR code generation completed!')
        )