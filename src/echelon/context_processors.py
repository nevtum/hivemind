from django.conf import settings

def app_version(request):
    """Context processor to take custom constants
    stored in django settings files to be applied
    to all templates """
    return { 'RELEASE_VERSION': settings.RELEASE_VERSION }

def app_links(request):
    """Context processor to enumerate and render
    all apps with title and url in the navbar"""
    return { 'APP_LINKS': settings.APP_LINKS }