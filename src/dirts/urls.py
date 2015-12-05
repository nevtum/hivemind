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
    url(r'^create-similar/(?P<dirt_id>[0-9]+?)/$', views.copy, name='create-similar-url'),
    url(r'^detail/(?P<dirt_id>[0-9]+?)/$', views.detail, name='dirt-detail-url'),
    url(r'^amend/(?P<dirt_id>[0-9]+?)/$', views.amend, name='dirt-amend-url'),
    url(r'^close/(?P<dirt_id>[0-9]+?)/$', views.close, name='dirt-close-url'),
    url(r'^reopen/(?P<dirt_id>[0-9]+?)/$', views.reopen, name='dirt-reopen-url'),
    url(r'^delete/(?P<dirt_id>[0-9]+?)/$', views.delete, name='dirt-delete-url'),
]
