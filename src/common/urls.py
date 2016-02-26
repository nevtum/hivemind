from django.conf.urls import include, url
from common.handler_views import accept

urlpatterns = [
    url(r'^v1/command-handler/$', accept, name='commands'),
]
