from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth

from . import views


urlpatterns = [
    url(r'^$', views.comments_for_defect, name='list'),
    url(r'^post_comment/$', auth(views.add_comment_for_defect), name='add')
]