from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'dirts.views.index', name='dirts-landing-url'),
    url(r'^create/', 'dirts.views.create', name='create-dirt-url'),
    url(r'^detail/(?P<dirt_id>[0-9]+?)/$', 'dirts.views.detail', name='dirt-detail-url'),
    url(r'^amend/(?P<dirt_id>[0-9]+?)/$', 'dirts.views.amend', name='dirt-amend-url'),
    url(r'^close/(?P<dirt_id>[0-9]+?)/$', 'dirts.views.close', name='dirt-close-url'),
    url(r'^reopen/(?P<dirt_id>[0-9]+?)/$', 'dirts.views.reopen', name='dirt-reopen-url'),
    url(r'^delete/(?P<dirt_id>[0-9]+?)/$', 'dirts.views.delete', name='dirt-delete-url'),
]
