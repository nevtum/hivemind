from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth

from . import views

patterns = [
    url(r'^(?P<pk>\d+?)/edit/$', auth(views.CommentEditView.as_view()), name='edit'),
    url(r'^(?P<pk>\d+?)/delete/$', auth(views.CommentDeleteView.as_view()), name='delete')
]

urlpatterns = [
    url(r'^', include(patterns, namespace='comments')),
]
