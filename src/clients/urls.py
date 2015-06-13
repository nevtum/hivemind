from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from clients import views

urlpatterns = [
    url(r'^$', 'clients.views.index'),
    url(r'^register/$', 'clients.views.create_company', name='newclient'),
    url(r'^([a-zA-Z]{2,3})/$', 'clients.views.contacts'),
]

router = routers.DefaultRouter()
router.register(r'companies', views.CompanyViewSet)
router.register(r'contacts', views.ContactViewSet)
router.register(r'roles', views.WorkRoleViewSet)

urlpatterns += [
    url(r'^v1/', include(router.urls)),
    url(r'^v1/commands/', 'clients.handler_views.accept'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^(?P<code>[a-zA-Z]+)/contacts/$', views.CompanyContactList.as_view()),
]
