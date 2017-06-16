from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth

from .handler_views import accept
from .views import CreateProjectView, EditProjectView, ProjectListView, ProjectsViewSet, CustomerViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', ProjectsViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^process_command/$', accept, name='commands'),
    url(r'^projects/$', ProjectListView.as_view(), name='projects'),
    url(r'^projects/new/$', auth(CreateProjectView.as_view()), name='create-project'),
    url(r'^projects/(?P<slug>[-\w\d]+)/$', auth(EditProjectView.as_view()), name='edit-project'),
]