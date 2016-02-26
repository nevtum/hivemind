from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from echelon.views import index, log_in, log_out
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^$', index, name='home-url'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^dirts/', include('dirts.urls')),
    url(r'^auth-token/', obtain_jwt_token),
    url(r'^login/', log_in, name='login-url'),
    url(r'^logout/', log_out, name='logout-url'),
    url(r'^common/', include('common.urls')),
]

urlpatterns += staticfiles_urlpatterns()
