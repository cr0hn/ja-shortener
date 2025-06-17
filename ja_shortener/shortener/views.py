from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect

from .models import ShortUrl, UrlVisit



def redirect_short_url(request, short_code):
    """
    Redirect to the original URL and track the visit.
    
    GET /{URL_PREFIX}/{short_code}/
    
    This view handles the actual URL redirection. When someone visits a shortened URL,
    this view will:
    1. Look up the original URL by short_code
    2. Record the visit with a visitor signature
    3. Redirect to the original URL
    
    The URL prefix is configurable via the URL_PREFIX environment variable.
    """
    try:
        short_url = ShortUrl.objects.get(short_code=short_code)
    except ShortUrl.DoesNotExist:
        raise Http404("Short URL not found")
    
    # Record the visit
    if settings.ENABLE_VISITS_TRACKING:
        UrlVisit.create_visit(short_url, request)
    
    # Redirect to the original URL
    return redirect(short_url.original_url, permanent=False)

