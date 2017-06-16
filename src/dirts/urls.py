from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth

from .api.urls import urlpatterns as api_urls
from .imports import views as import_views
from .imports.urls import urlpatterns as import_urls
from .comments.urls import urlpatterns as defect_comment_urls
from .views import views
from .comments import views as comment_views

urlpatterns = [
    url(r'^', include(import_urls, namespace='imports')),
    url(r'^api/', include(api_urls, namespace='api')),
    url(r'^(?P<pk>\d+?)/comments/', include(defect_comment_urls, namespace='defect-comments')),
    
    url(r'^report/$', views.report, name='report'),
    url(r'^$', views.DefectListView.as_view(), name='list'),
    url(r'^active/$', views.ActiveDefectListView.as_view(), name='outstanding'),
    url(r'^most-recent/$', views.RecentlyChangedDefectListView.as_view(), name='recent'),
    url(r'^create/', auth(views.DefectCreateView.as_view()), name='create'),
    url(r'^tags/$', views.TagsListView.as_view(), name='tags-list'),
    url(r'^tags/(?P<slug>[-\w\d]+)/$', views.defects_by_tag, name='filter-by-tag'),
    url(r'^(?P<pk>\d+?)/create-similar/$', auth(views.DefectCopyView.as_view()), name='create-similar'),
    url(r'^(?P<pk>\d+?)/$', views.DefectDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+?)/debug/$', views.debug),
    url(r'^(?P<pk>\d+?)/(?P<day>\d{1,2})-(?P<month>\d{1,2})-(?P<year>\d{4})/$', views.time_travel, name='dirt-time-travel'),
    url(r'^(?P<pk>\d+?)/amend/$', auth(views.DefectUpdateView.as_view()), name='amend'),
    url(r'^(?P<pk>\d+?)/close/$', auth(views.DefectCloseView.as_view()), name='close'),
    url(r'^(?P<pk>\d+?)/reopen/$', auth(views.DefectReopenView.as_view()), name='reopen'),
    url(r'^(?P<pk>\d+?)/lock/$', auth(views.DefectLockView.as_view()), name='lock'),
    url(r'^(?P<pk>\d+?)/delete/$', views.delete, name='delete'),
    url(r'^(?P<pk>\d+?)/tags/$', auth(views.EditTagsView.as_view()), name='tags'),
]
