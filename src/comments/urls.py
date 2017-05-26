from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^(?P<pk>\d+?)/edit/$', views.edit_comment, name='comment-edit'),
    url(r'^(?P<pk>\d+?)/delete/$', views.delete_comment, name='comment-delete')
]