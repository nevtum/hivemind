from django.conf.urls import include, url
from rest_framework import routers
from .api_views import DefectViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'dirts', DefectViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^$', views.index, name='dirts-landing-url'),
    url(r'^create/', views.create, name='create-dirt-url'),
    url(r'^(?P<dirt_id>\d+?)/create-similar/$', views.copy, name='create-similar-url'),
    url(r'^(?P<dirt_id>\d+?)/$', views.detail, name='dirt-detail-url'),
    url(r'^(?P<dirt_id>\d+?)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', views.time_travel, name='dirt-time-travel'),
    url(r'^(?P<dirt_id>\d+?)/amend/$', views.amend, name='dirt-amend-url'),
    url(r'^(?P<dirt_id>\d+?)/close/$', views.close, name='dirt-close-url'),
    url(r'^(?P<dirt_id>\d+?)/reopen/$', views.reopen, name='dirt-reopen-url'),
    url(r'^(?P<dirt_id>\d+?)/delete/$', views.delete, name='dirt-delete-url'),
]
