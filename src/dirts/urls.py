from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth

from .imports import views as import_views
from .imports.urls import urlpatterns as import_urls
from .comments.urls import urlpatterns as defect_comment_urls
from .views import views
from .comments import views as comment_views

# defect detail/action urls
urlpatterns = [
    url(r'^import/', include(import_urls, namespace='imports')),
    url(r'^report/$', auth(views.report), name='report'),
    url(r'^create/', auth(views.DefectCreateView.as_view()), name='create'),
    url(r'^(?P<pk>\d+?)/create_similar/$', auth(views.DefectCopyView.as_view()), name='create-similar'),
    url(r'^(?P<pk>\d+?)/$', auth(views.DefectDetailView.as_view()), name='detail'),
    url(r'^(?P<pk>\d+?)/tags/$', auth(views.EditTagsView.as_view()), name='tags'),
    url(r'^(?P<pk>\d+?)/comments/', include(defect_comment_urls, namespace='defect-comments')),
    url(r'^(?P<pk>\d+?)/amend/$', auth(views.DefectUpdateView.as_view()), name='amend'),
    url(r'^(?P<pk>\d+?)/close/$', auth(views.DefectCloseView.as_view()), name='close'),
    url(r'^(?P<pk>\d+?)/reopen/$', auth(views.DefectReopenView.as_view()), name='reopen'),
    url(r'^(?P<pk>\d+?)/lock/$', auth(views.DefectLockView.as_view()), name='lock'),
    url(r'^(?P<pk>\d+?)/delete/$', auth(views.delete), name='delete'),
    url(r'^(?P<pk>\d+?)/debug/$', auth(views.debug)),
    url(r'^(?P<pk>\d+?)/(?P<day>\d{1,2})-(?P<month>\d{1,2})-(?P<year>\d{4})/$', auth(views.time_travel), name='dirt-time-travel'),
]

# tags urls
urlpatterns += [
    url(r'^tags/$', auth(views.TagsListView.as_view()), name='tags-list'),
    url(r'^tags/(?P<slug>[-\w\d]+)/$', auth(views.defects_by_tag), name='filter-by-tag'),
]

# defect list urls
urlpatterns += [
    url(r'^$', auth(views.DefectListView.as_view()), name='list'),
    url(r'^active/$', auth(views.ActiveDefectListView.as_view()), name='outstanding'),
    url(r'^most_recent/$', auth(views.RecentlyChangedDefectListView.as_view()), name='recent'),
    url(r'^(?P<slug>[-\w\d]+)/$', auth(views.CustomListView.as_view()), name='list'),
    url(r'^(?P<slug>[-\w\d]+)/active/$', auth(views.CustomActiveDefectListView.as_view()), name='outstanding'),
    url(r'^(?P<slug>[-\w\d]+)/most_recent/$', auth(views.CustomChangedDefectListView.as_view()), name='recent'),
]