from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth

from . import views

urlpatterns = [
    url(r'^$', auth(views.begin_import), name='import-list'),
    url(r'^confirm/$', auth(views.complete_import), name='complete-import'),
]
