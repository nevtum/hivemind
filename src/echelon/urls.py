from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rest_framework.authtoken import views

urlpatterns = [
    url(r'^$', 'echelon.views.index', name='home-url'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^clients/', include('clients.urls')),
    url(r'^dirts/', include('dirts.urls')),
    url(r'^auth-token/', views.obtain_auth_token),
    url(r'^login/', 'echelon.views.log_in', name='login-url'),
    url(r'^logout/', 'echelon.views.log_out', name='logout-url'),
]

urlpatterns += staticfiles_urlpatterns()
