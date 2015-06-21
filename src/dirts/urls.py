from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'dirts.views.index', name='dirts-landing-url'),
    url(r'^create/', 'dirts.views.create', name='create-dirt-url'),
]
