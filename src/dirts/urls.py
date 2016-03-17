from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth
from rest_framework import routers
from .api_views import DefectViewSet
from . import views

router = routers.DefaultRouter()
router.register(r'dirts', DefectViewSet)

urlpatterns = [
    url(r'^v1/', include(router.urls)),
    url(r'^$', views.DefectListView.as_view(), name='dirts-landing-url'),
    url(r'^active/$', views.ActiveDefectListView.as_view(), name='active-dirts'),
    url(r'^most-recent/$', views.RecentlyChangedDefectListView.as_view(), name='recent-dirts'),
    url(r'^create/', auth(views.DefectCreateView.as_view()), name='create-dirt-url'),
    url(r'^tags/$', auth(views.TagsListView.as_view()), name='tags-list'),
    url(r'^(?P<dirt_id>\d+?)/create-similar/$', auth(views.DefectCopyView.as_view()), name='create-similar-url'),
    url(r'^(?P<dirt_id>\d+?)/$', views.detail, name='dirt-detail-url'),
    url(r'^(?P<dirt_id>\d+?)/debug/$', views.debug, name='dirt-debug'),
    url(r'^(?P<dirt_id>\d+?)/(?P<day>\d{1,2})-(?P<month>\d{1,2})-(?P<year>\d{4})/$', views.time_travel, name='dirt-time-travel'),
    url(r'^(?P<dirt_id>\d+?)/amend/$', auth(views.DefectUpdateView.as_view()), name='dirt-amend-url'),
    url(r'^(?P<dirt_id>\d+?)/close/$', auth(views.DefectCloseView.as_view()), name='dirt-close-url'),
    url(r'^(?P<dirt_id>\d+?)/reopen/$', auth(views.DefectReopenView.as_view()), name='dirt-reopen-url'),
    url(r'^(?P<dirt_id>\d+?)/delete/$', views.delete, name='dirt-delete-url'),
    url(r'^(?P<dirt_id>\d+?)/tags/$', auth(views.EditTagsView.as_view()), name='tags'),
]
