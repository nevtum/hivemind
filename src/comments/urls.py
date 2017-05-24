from django.conf.urls import include, url
from .views import comments_for_defect

urlpatterns = [
    url(r'^$', comments_for_defect, name='list')
]