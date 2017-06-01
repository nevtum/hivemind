from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth
from rest_framework import routers

from .views import api_views, views, import_views
# from comments import urls as comments_urls

router = routers.DefaultRouter()
router.register(r'all', api_views.DefectBaseViewSet, 'all')
router.register(r'active', api_views.DefectActiveViewSet, 'active')
router.register(r'recent', api_views.RecentlyChangedDefectViewSet, 'recent')
router.register(r'suggest_defects', api_views.AutoCompleteDefectTitles, 'suggest')
router.register(r'suggest_projects', api_views.AutoCompleteProjects, 'project-suggest')

defect_comment_urls = [
    url(r'^$', views.comments_for_defect, name='list'),
    url(r'^post_comment/$', auth(views.add_comment_for_defect), name='add')
]

urlpatterns = [
    url(r'^api/', include(router.urls, namespace='dirts')),
    url(r'^(?P<pk>\d+?)/comments/', include(defect_comment_urls, namespace='comments')),
    url(r'^api/more-like-this/(?P<pk>\d+?)/$', api_views.more_like_this_defect, name='similar-defects'),
    url(r'^import/$', import_views.begin_import, name='import-list'),
    url(r'^import-confirm/$', import_views.complete_import, name='complete-import'),
    url(r'^report/$', views.report, name='report'),
    url(r'^$', views.DefectListView.as_view(), name='dirts-list'),
    url(r'^active/$', views.ActiveDefectListView.as_view(), name='active-dirts'),
    url(r'^most-recent/$', views.RecentlyChangedDefectListView.as_view(), name='recent-dirts'),
    url(r'^create/', auth(views.DefectCreateView.as_view()), name='create-dirt-url'),
    url(r'^tags/$', views.TagsListView.as_view(), name='tags-list'),
    url(r'^tags/(?P<slug>[-\w\d]+)/$', views.dirts_by_tag, name='dirts-by-tag'),
    url(r'^(?P<pk>\d+?)/create-similar/$', auth(views.DefectCopyView.as_view()), name='create-similar-url'),
    url(r'^(?P<pk>\d+?)/$', views.DefectDetailView.as_view(), name='dirt-detail-url'),
    url(r'^(?P<pk>\d+?)/debug/$', views.debug, name='dirt-debug'),
    url(r'^(?P<pk>\d+?)/(?P<day>\d{1,2})-(?P<month>\d{1,2})-(?P<year>\d{4})/$', views.time_travel, name='dirt-time-travel'),
    url(r'^(?P<pk>\d+?)/amend/$', auth(views.DefectUpdateView.as_view()), name='dirt-amend-url'),
    url(r'^(?P<pk>\d+?)/close/$', auth(views.DefectCloseView.as_view()), name='dirt-close-url'),
    url(r'^(?P<pk>\d+?)/reopen/$', auth(views.DefectReopenView.as_view()), name='dirt-reopen-url'),
    url(r'^(?P<pk>\d+?)/delete/$', views.delete, name='dirt-delete-url'),
    url(r'^(?P<pk>\d+?)/tags/$', auth(views.EditTagsView.as_view()), name='tags'),
]
