from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from clients import api_views

urlpatterns = [
    url(r'^$', 'clients.views.index'),
    url(r'^([a-zA-Z]+?)/$', 'clients.views.contacts'),
]

router = routers.DefaultRouter()
router.register(r'subscriptions', api_views.SubscriptionViewSet)
router.register(r'contacts', api_views.ContactViewSet)

urlpatterns += [
    url(r'^v1/', include(router.urls)),
    url(r'^v1/commands/', 'clients.handler_views.accept'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
