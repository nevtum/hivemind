from django.conf.urls import include, url
from common.handler_views import accept
from .views import CreateProjectView, ProjectListView

urlpatterns = [
    url(r'^v1/command-handler/$', accept, name='commands'),
    url(r'^projects/$', ProjectListView.as_view(), name='projects'),
    url(r'^projects/new/$', CreateProjectView.as_view(), name='create-project'),
    
]
