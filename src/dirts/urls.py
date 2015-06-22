from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'dirts.views.index', name='dirts-landing-url'),
    url(r'^create/', 'dirts.views.create', name='create-dirt-url'),
    url(r'^detail/(?P<dirt_id>[0-9]+?)/$', 'dirts.views.detail', name='dirt-detail-url')
]
