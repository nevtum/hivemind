from django.conf.urls import include, url
from .views import comments_for_defect, add_comment_for_defect

urlpatterns = [
    url(r'^$', comments_for_defect, name='list'),
    url(r'^post_comment/$', add_comment_for_defect, name='add')
]