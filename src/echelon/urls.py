from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clients/', include('clients.urls')),
    url(r'^dirts/', include('dirts.urls')),
    url(r'^login/', views.obtain_auth_token),
]

urlpatterns += staticfiles_urlpatterns()
