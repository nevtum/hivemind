from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth

from .core.handler_views import accept
from .defects.urls import urlpatterns as defect_api_urls
from .customers.views import ProjectsViewSet, CustomerViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'projects', ProjectsViewSet)
router.register(r'customers', CustomerViewSet)

urlpatterns = [
    url(r'^defects/', include(defect_api_urls, namespace='defects')),
    url(r'^clients/', include(router.urls, namespace='clients')),
    url(r'^process_command/$', accept, name='commands'),
]