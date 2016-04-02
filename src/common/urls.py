from django.conf.urls import include, url
from common.handler_views import accept
from .views import ProjectListView

urlpatterns = [
    url(r'^v1/command-handler/$', accept, name='commands'),
    url(r'^projects/$', ProjectListView.as_view(), name='projects'),
]
