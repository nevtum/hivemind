from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from clients import api_views
from clients.views import contacts
from clients.handler_views import accept

urlpatterns = [
    url(r'^$', contacts, name='clients-landing-url'),
]

router = routers.DefaultRouter()
router.register(r'subscriptions', api_views.SubscriptionViewSet)
router.register(r'contacts', api_views.ContactViewSet)

urlpatterns += [
    url(r'^v1/', include(router.urls)),
    url(r'^v1/commands/', accept),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
