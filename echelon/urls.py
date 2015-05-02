from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from clients import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'echelon.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clients/register/$', 'clients.views.create_company', name='newclient'),
    url(r'^clients/$', 'clients.views.index'),
    url(r'^clients/([a-zA-Z]+)/$', 'clients.views.contacts'),
]

router = routers.DefaultRouter()
router.register(r'Companies', views.CompanyViewSet)
router.register(r'Contacts', views.ContactViewSet)

urlpatterns += [
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
