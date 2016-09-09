from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$', views.ActivityListView.as_view(), name='feed-url'),
]
