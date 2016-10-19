from django.conf import settings
from django.core.urlresolvers import reverse_lazy

def app_version(request):
    """Context processor to take custom constants
    stored in django settings files to be applied
    to all templates """
    return { 'RELEASE_VERSION': settings.RELEASE_VERSION }

def app_links(request):
    return { 'APP_LINKS': [
        {
            'title': 'Feed',
            'url': reverse_lazy('feed-url')
        },
        {
            'title': 'Projects',
            'url': reverse_lazy('projects')
        },
        {
            'title': 'DIRTs',
            'url': reverse_lazy('dirts-list')
        },
    ]}