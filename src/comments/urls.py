from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth

from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+?)/edit/$', auth(views.CommentEditView.as_view()), name='comment-edit'),
    url(r'^(?P<pk>\d+?)/delete/$', auth(views.delete_comment), name='comment-delete')
]
