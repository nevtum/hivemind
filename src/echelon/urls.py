from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from echelon.views import index
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    url(r'^$', index, name='home-url'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^auth-token/', obtain_jwt_token),
    url(r'^login/', login, {'template_name': 'login.html'}, name='login-url'),
    url(r'^logout/', logout, {'next_page': 'home-url'}, name='logout-url'),
]

for app in settings.ECHELON_APPS:
    regex = r'^{}/'.format(app)
    context_name = '{}.urls'.format(app)
    urlpatterns.append(url(regex, include(context_name)))

urlpatterns += staticfiles_urlpatterns()
