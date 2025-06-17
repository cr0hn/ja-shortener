from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import Count, Q, Avg, Sum, Max, Min
from django.db.models.functions import TruncDate

from shortener.models import ShortUrl, UrlVisit


def dashboard_callback(request, context: dict):
    """
    Dashboard callback for URL shortener statistics.
    Optimized queries to minimize database hits and improve performance.
    """
    
    # Get latest 15 shortened URLs with visit counts in a single optimized query
    latest_shortened_urls = {
        "headers": ["Short Code", "Original URL", "Total Visits", "Unique Visitors", "Created Date"],
        "rows": []
    }
    
    # Optimized query with annotations to get all data in one DB hit
    recent_urls = (
        ShortUrl.objects
        .annotate(
            total_visits=Count('visits', distinct=False),
            unique_visitors=Count('visits__visitor_signature', distinct=True)
        )
        .order_by('-created_at')
        .values(
            'short_code', 'original_url', 'created_at', 
            'total_visits', 'unique_visitors'
        )[:15]
    )
    
    # Process results efficiently without additional DB queries
    for url_data in recent_urls:
        # Truncate long URLs for display
        original_url_display = (
            url_data['original_url'][:50] + "..." 
            if len(url_data['original_url']) > 50 
            else url_data['original_url']
        )
        
        latest_shortened_urls["rows"].append([
            url_data['short_code'],
            original_url_display,
            url_data['total_visits'],
            url_data['unique_visitors'],
            url_data['created_at'].strftime("%Y-%m-%d")
        ])
    
    # Get most visited URLs with a single optimized query
    most_visited_urls = {
        "headers": ["Short Code", "Original URL", "Total Visits"],
        "rows": []
    }
    
    # Optimized query for top visited URLs
    top_visited = (
        ShortUrl.objects
        .annotate(total_visits=Count('visits'))
        .filter(total_visits__gt=0)
        .order_by('-total_visits')
        .values('short_code', 'original_url', 'total_visits')[:10]
    )
    
    for url_data in top_visited:
        original_url_display = (
            url_data['original_url'][:40] + "..." 
            if len(url_data['original_url']) > 40 
            else url_data['original_url']
        )
        
        most_visited_urls["rows"].append([
            url_data['short_code'],
            original_url_display,
            url_data['total_visits']
        ])
    
    # Get all statistics in optimized queries
    # Use exists() check to avoid division by zero and unnecessary queries
    url_stats = ShortUrl.objects.aggregate(
        total_urls=Count('id'),
        avg_visits_per_url=Avg('visits__id'),
        latest_creation=Max('created_at'),
        earliest_creation=Min('created_at')
    )
    
    visit_stats = UrlVisit.objects.aggregate(
        total_visits=Count('id'),
        unique_visitors=Count('visitor_signature', distinct=True)
    )
    
    # Calculate derived statistics
    total_urls = url_stats['total_urls'] or 0
    total_visits = visit_stats['total_visits'] or 0
    unique_visitors = visit_stats['unique_visitors'] or 0
    avg_visits_per_url = round(total_visits / total_urls, 2) if total_urls > 0 else 0
    
    # Get recent activity (last 7 days) with optimized query
    from django.utils import timezone
    from datetime import timedelta
    
    seven_days_ago = timezone.now() - timedelta(days=7)
    recent_activity = UrlVisit.objects.filter(
        visited_at__gte=seven_days_ago
    ).aggregate(
        recent_visits=Count('id'),
        recent_unique_visitors=Count('visitor_signature', distinct=True)
    )
    
    # Get daily visit trends for the last 7 days (optimized single query)
    daily_visits = (
        UrlVisit.objects
        .filter(visited_at__gte=seven_days_ago)
        .extra(select={'visit_date': 'DATE(visited_at)'})
        .values('visit_date')
        .annotate(
            daily_total=Count('id'),
            daily_unique=Count('visitor_signature', distinct=True)
        )
        .order_by('visit_date')
    )
    
    # Prepare daily trends data
    daily_trends = {
        "headers": ["Date", "Total Visits", "Unique Visitors"],
        "rows": [
            [
                day['visit_date'],
                day['daily_total'],
                day['daily_unique']
            ]
            for day in daily_visits
        ]
    }
    
    # Update context with all optimized statistics
    context.update({
        # Main data tables
        'latest_shortened_urls': latest_shortened_urls,
        'most_visited_urls': most_visited_urls,
        'daily_trends': daily_trends,
        
        # Core statistics
        'total_urls': total_urls,
        'total_visits': total_visits,
        'unique_visitors': unique_visitors,
        'avg_visits_per_url': avg_visits_per_url,
        
        # Recent activity (last 7 days)
        'recent_visits': recent_activity['recent_visits'] or 0,
        'recent_unique_visitors': recent_activity['recent_unique_visitors'] or 0,
        
        # Derived metrics
        'click_through_rate': round((total_visits / total_urls * 100), 2) if total_urls > 0 else 0,
        'unique_visitor_rate': round((unique_visitors / total_visits * 100), 2) if total_visits > 0 else 0,
        
        # Date ranges
        'earliest_url_date': url_stats['earliest_creation'],
        'latest_url_date': url_stats['latest_creation'],
    })

    return context


def environment_callback(request):
    """
    Callback to display current environment in Unfold admin.
    """
    return "Development" if settings.DEBUG else "Production"

